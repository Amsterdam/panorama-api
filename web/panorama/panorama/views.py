# Packages
import math

from datapunt_api import rest
from django.contrib.gis.db.models import GeometryField
from django.contrib.gis.geos import GEOSGeometry, Polygon
from django.contrib.gis.measure import D
from django.db import models
from django.db.models import Q, Exists, OuterRef, Func, F, Expression, Value
from django.db.models.expressions import CombinedExpression
from django_filters import widgets
from django_filters.rest_framework import DjangoFilterBackend
from django_filters.rest_framework import filters
from django_filters.rest_framework.filterset import FilterSet
from rest_framework import serializers as rest_serializers
from rest_framework.decorators import action
from rest_framework.response import Response

# Project
from datasets.panoramas.serialize.hal_serializer import (
    HALPaginationEmbedded,
    simple_hal_embed,
)
from datasets.panoramas.models import Panorama, Adjacencies
from datasets.panoramas.serialize.serializers import (
    PanoSerializer,
    AdjacentPanoSerializer,
)

MISSION_TYPE_CHOICES = (("bi", "bi"), ("woz", "woz"))

SURFACE_TYPE_CHOICES = (
    ("L", "land"),
    ("W", "water"),
)

SRID_CHOICES = (("4326", "4326"), ("28992", "28992"))


# https://stackoverflow.com/questions/47094982/django-subquery-and-annotations-with-outerref
class RawCol(Expression):
    def __init__(self, model, field_name, output_field=None):
        field = model._meta.get_field(field_name)
        self.table = model._meta.db_table
        self.column = field.column
        super().__init__(output_field=output_field)

    def as_sql(self, compiler, connection):
        sql = f'"{self.table}"."{self.column}"'
        return sql, []


class PanoramaFilter(FilterSet):

    MAX_RADIUS = 100000  # meters

    DEFAULT_SRID = 4326

    # the size of a map tile on https://data.amsterdam.nl/ on zoom
    # level 11 is approximately 500 square meters.
    # Panorama photos are displayed on zoom level 11 and up.
    MAX_NEWEST_IN_RANGE_RADIUS = 250  # meters

    timestamp = filters.DateTimeFromToRangeFilter(
        label="Timestamp", widget=widgets.DateRangeWidget()
    )

    near = filters.CharFilter(method="near_filter", label="Near point")
    radius = filters.NumberFilter(method="radius_filter", label="Radius")
    bbox = filters.CharFilter(method="bbox_filter", label="Bounding box")
    srid = filters.ChoiceFilter(
        method="srid_filter", choices=SRID_CHOICES, label="Projection (SRID)"
    )

    newest_in_range = filters.BooleanFilter(
        method="newest_in_range_filter", label="Only return newest in range"
    )
    limit_results = filters.NumberFilter(
        method="limit_results_filter", label="Limit of the results"
    )

    tags = filters.CharFilter(method="tags_filter", label="Tags")

    class Meta(object):
        model = Panorama

        # when adding new filter-fields remember to add them as well to the inner-query `exists` in
        #   the method `newest_in_range_filter`
        fields = (
            "timestamp",
            "near",
            "radius",
            "bbox",
            "srid",
            "newest_in_range",
            "tags",
            "limit_results",
        )

    def _get_radius_query(self, queryset, radius):
        if not self._is_filter_enabled("near"):
            raise rest_serializers.ValidationError(
                "near parameter must be set to use radius filter"
            )

        near = self._get_filter_string("near")
        try:
            srid = self._get_srid_parameter()
            point = self._coordinates_from_string("near", near, 2)
        except ValueError as e:
            rest_serializers.ValidationError(str(e))

        postgis_point = Func(
            Value(point[0]),
            Value(point[1]),
            function="ST_MakePoint",
            output_field=GeometryField(),
        )
        srid_point = Func(postgis_point, srid, function="ST_SetSRID", output_field=GeometryField())
        transformed_point = Func(
            srid_point, 28992, function="ST_Transform", output_field=GeometryField()
        )

        queryset = queryset.filter(_geolocation_2d_rd__dwithin=(transformed_point, D(m=radius)))

        # Sort by indexed KNN distance, see https://postgis.net/docs/geometry_distance_knn.html
        order_by_distance = CombinedExpression(F("_geolocation_2d_rd"), "<->", transformed_point)
        return queryset.order_by(order_by_distance)

    def _coordinates_from_string(self, name, value, expected_coordinates):
        try:
            coordinates = list(map(lambda coordinate: float(coordinate), value.split(",")))
        except ValueError:
            raise ValueError("%s coordinates must be numbers, separated by commas" % name)

        if len(coordinates) != expected_coordinates:
            raise ValueError(
                "%s coordinates must consist of %s numbers" % (name, expected_coordinates)
            )

        return coordinates

    def _bbox_from_string(self, value):
        coordinates = self._coordinates_from_string("bbox", value, 4)

        return {
            "x1": coordinates[0],
            "y1": coordinates[1],
            "x2": coordinates[2],
            "y2": coordinates[3],
        }

    def _get_srid_parameter(self):
        if self._is_filter_enabled("srid"):
            try:
                srid = int(self._get_filter_string("srid"))
            except ValueError:
                raise ValueError("srid must be a number")
            return srid
        else:
            return self.DEFAULT_SRID

    def _get_bbox_query(self, queryset, value):
        try:
            bbox = self._bbox_from_string(value)
            srid = self._get_srid_parameter()
        except ValueError as e:
            rest_serializers.ValidationError(str(e))

        envelope = Func(
            Value(bbox["x1"]),
            Value(bbox["y1"]),
            Value(bbox["x2"]),
            Value(bbox["y2"]),
            srid,
            function="ST_MakeEnvelope",
            output_field=GeometryField(),
        )
        transformed_envelope = Func(
            envelope, 28992, function="ST_Transform", output_field=GeometryField()
        )
        return queryset.filter(_geolocation_2d_rd__bboverlaps=(transformed_envelope))

    def _get_filter_string(self, name):
        return name in self.data and self.data[name]

    def _is_filter_enabled(self, name):
        filter = self._get_filter_string(name)
        return filter and len(filter)

    def radius_filter(self, queryset, name, value):
        if self._is_filter_enabled("bbox"):
            raise rest_serializers.ValidationError(
                "near/radius and bbox filters cannot be used at the same time"
            )

        return self._get_radius_query(queryset, value)

    def _get_skip_not_exists(self):
        pass

    def filter_queryset(self, queryset):
        if self._is_filter_enabled("limit_results"):
            limit_results = int(self._get_filter_string("limit_results"))
            return super().filter_queryset(queryset)[0:limit_results]
        return super().filter_queryset(queryset)

    def newest_in_range_filter(self, queryset, name, value):
        if not (self._is_filter_enabled("bbox") or self._is_filter_enabled("radius")):
            raise rest_serializers.ValidationError(
                "bbox or near/radius filter must be enabled to use newest in radius"
            )

        mission_distance_margin = 0.7

        exists = (
            queryset.model.objects.values("id")
            .filter(status="done")
            .filter(surface_type=OuterRef("surface_type"))
            .filter(timestamp__gt=OuterRef("timestamp"))
            .annotate(
                within=Func(
                    RawCol(queryset.model, "_geolocation_2d_rd"),
                    F("_geolocation_2d_rd"),
                    RawCol(queryset.model, "mission_distance") - mission_distance_margin,
                    function="ST_DWithin",
                    output_field=models.BooleanField(),
                )
            )
            .filter(within=True)
        )

        # The exists subquery which selects panoramas only if they are the newest
        # within a range of meters performs much faster if we include the radius or
        # bounding box filter from the outer query:
        if self._is_filter_enabled("radius"):
            try:
                radius = float(self.data["radius"])
            except ValueError:
                raise rest_serializers.ValidationError("radius parameter must be a number")

            if radius > self.MAX_NEWEST_IN_RANGE_RADIUS:
                raise rest_serializers.ValidationError(
                    "radius for newest_in_range filter can be at most %s meters"
                    % self.MAX_NEWEST_IN_RANGE_RADIUS
                )

            # TODO: add padding to radius with newest_in_range radius
            exists = self._get_radius_query(exists, radius)
        elif self._is_filter_enabled("bbox"):
            # Square that fits circle with radius = MAX_NEWEST_IN_RANGE_RADIUS
            # has area of:
            max_area = math.pow(self.MAX_NEWEST_IN_RANGE_RADIUS * 2, 2)

            bbox_string = self.data["bbox"]

            try:
                bbox = self._bbox_from_string(bbox_string)
            except ValueError as e:
                rest_serializers.ValidationError(str(e))

            try:
                srid = self._get_srid_parameter()
            except ValueError as e:
                rest_serializers.ValidationError(str(e))

            polygon = Polygon.from_bbox((bbox["x1"], bbox["y1"], bbox["x2"], bbox["y2"]))
            geometry = GEOSGeometry(polygon, srid=srid).transform(28992, clone=True)

            if geometry.area > max_area:
                raise rest_serializers.ValidationError(
                    "area for newest_in_range filter can be at most %s square meters" % max_area
                )

            # TODO: add padding to bbox with newest_in_range radius
            exists = self._get_bbox_query(exists, bbox_string)

        # there is no guarantee on the order of application of filters, therefore the exists might be
        # copied from the queryset before all filters are applied, making the inner exists subquery not
        # match the outer subset. So we manually apply the other filters from outer as well:
        if self._is_filter_enabled("mission_type"):
            exists = exists.filter(mission_type=OuterRef("mission_type"))
        if self._is_filter_enabled("mission_year"):
            exists = exists.filter(mission_year=OuterRef("mission_year"))
        if self._is_filter_enabled("timestamp_before"):
            exists = exists.filter(timestamp__lte=self._get_filter_string("timestamp_before"))
        if self._is_filter_enabled("timestamp_after"):
            exists = exists.filter(timestamp__gte=self._get_filter_string("timestamp_after"))
        if self._is_filter_enabled("tags"):
            tags = self._get_filter_string("tags")
            exists = exists.filter(tags__contains=tags.split(","))

        not_exists_filter = Q(not_exists=True)

        if self._get_skip_not_exists():
            not_exists_filter = self._get_skip_not_exists() | not_exists_filter

        return queryset.annotate(
            not_exists=~Exists(exists, output_field=models.BooleanField())
        ).filter(not_exists_filter)

    def tags_filter(self, queryset, name, value):
        return queryset.filter(tags__contains=value.split(","))

    def srid_filter(self, queryset, name, value):
        # Don't do anything, SRID parameter is used
        # in bbox and radius filters
        return queryset

    def limit_results_filter(self, queryset, name, value):
        # Don't do anything, is used to slice filter_queryset
        return queryset

    def near_filter(self, queryset, name, value):
        if not self._is_filter_enabled("radius"):
            raise rest_serializers.ValidationError(
                "radius parameter must be set to use near filter"
            )

        # Don't do anything, near parameter is used
        # in radius filter
        return queryset

    def bbox_filter(self, queryset, name, value):
        if self._is_filter_enabled("radius"):
            raise rest_serializers.ValidationError(
                "radius and bbox filters are mutually exclusive"
            )

        return self._get_bbox_query(queryset, value)


class PanoramaFilterAdjacent(PanoramaFilter):
    DEFAULT_ADJACENT_RADIUS = 21

    def __init__(self, data=None, queryset=None, request=None, prefix=None, pano_id=None):
        self.pano_id = pano_id

        if not ("radius" in data and data["radius"]):
            data = request.GET.copy()
            data["radius"] = str(self.DEFAULT_ADJACENT_RADIUS)

        super().__init__(data=data, queryset=queryset, request=request, prefix=prefix)

    def _get_skip_not_exists(self):
        if self.pano_id:
            return Q(pano_id=self.pano_id)

        return super()._get_skip_not_exists()

    def _get_radius_query(self, queryset, radius):
        return queryset.annotate(
            within=Func(
                F("from_geolocation_2d_rd"),
                F("_geolocation_2d_rd"),
                Value(radius),
                function="ST_DWithin",
                output_field=models.BooleanField(),
            )
        ).filter(within=True)


class PanoramaViewSet(rest.DatapuntViewSet):
    """
    Parameters:

    - newest_in_range: (boolean) only return photos that are the newest within their distance interval
    - srid: (integer) projection of coordinates, either 4326 or 28992
    - near: (string) two-dimensional point, separated by a comma; "<lon>,<lat>" when "srid=4326", "<x>,<y>" when "srid=28992"
    - radius: (number) search radius in meters from point "near"
    - bbox: (string) only return photos contained by bounding box, two two-dimensional points "<northwest>,<southeast>", same as point "near"
    - timestamp_before: (string) ISO date format (yyyy-mm-dd)
    - timestamp_after: (string) ISO date format (yyyy-mm-dd)
    - tags: (string) a comma-seperated list of tags to filter on, for example: "mission-bi,mission2017"
    - limit_results: (integer) limit on the returned results (impacts count and pagination: if more results are available, they don't show up in counts). Can be used for performance reasons
    """

    lookup_field = "pano_id"
    queryset = Panorama.done.all()
    serializer_detail_class = PanoSerializer
    serializer_class = PanoSerializer
    pagination_class = HALPaginationEmbedded

    filter_backends = (DjangoFilterBackend,)
    filterset_class = PanoramaFilter

    @action(detail=True)
    def adjacencies(self, request, pano_id):
        queryset = Adjacencies.objects.filter(from_pano_id=pano_id)
        adjacency_filter = PanoramaFilterAdjacent(
            request=request,
            queryset=queryset,
            data=request.query_params,
            pano_id=pano_id,
        )

        if adjacency_filter._is_filter_enabled("bbox"):
            raise rest_serializers.ValidationError(
                "bbox filter not allowed for adjacent panoramas"
            )

        if adjacency_filter._is_filter_enabled("near"):
            raise rest_serializers.ValidationError(
                "near filter not allowed for adjacent panoramas"
            )

        queryset = adjacency_filter.qs.extra(order_by=["relative_distance"])

        serializer = AdjacentPanoSerializer(
            instance=queryset, many=True, context={"request": request}
        )

        return Response(simple_hal_embed(serializer.data, self.request))

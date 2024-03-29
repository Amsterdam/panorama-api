import logging

# Packages
from rest_framework import serializers
from rest_framework_gis import fields

# Project
from datasets.panoramas.serialize.hal_serializer import (
    HALSerializer,
    HyperLinksField,
    IdentityLinksField,
    HALListSerializer,
)
from datasets.panoramas.models import Panorama, Adjacencies

log = logging.getLogger(__name__)

MAX_ADJACENCY = 21


class PanoLinksField(IdentityLinksField):
    lookup_field = "pano_id"


class PanoSerializer(HALSerializer):

    # Content for _links in HAL-json:
    serializer_url_field = PanoLinksField
    equirectangular_full = HyperLinksField()
    equirectangular_medium = HyperLinksField()
    equirectangular_small = HyperLinksField()
    cubic_img_preview = HyperLinksField()
    thumbnail = IdentityLinksField(
        view_name="thumbnail-detail",
        lookup_field="pano_id",
        format="html",
        read_only=True,
    )
    adjacencies = IdentityLinksField(
        view_name="panorama-adjacencies",
        lookup_field="pano_id",
        format="html",
        read_only=True,
    )

    # Additional regular attributes:
    cubic_img_baseurl = serializers.ReadOnlyField()
    cubic_img_pattern = serializers.ReadOnlyField()
    geometry = fields.GeometryField(source="geolocation")

    class Meta(HALSerializer.Meta):
        model = Panorama
        listresults_field = "panoramas"
        list_serializer_class = HALListSerializer
        exclude = (
            "path",
            "geolocation",
            "_geolocation_2d",
            "_geolocation_2d_rd",
            "status",
            "status_changed",
        )


class AdjacentLink(PanoLinksField):
    """For sake of HAL-compliancy the self link of an adjacency is constructed,
    allthough there is no endpoint listening in (therefore Django couldn't construct it for us.)
    """

    def to_representation(self, value):
        request = self.context.get("request")
        href = f"{request.build_absolute_uri(request.path)}{value.from_pano_id}/"
        return dict(href=href)


class AdjacentPanoSerializer(PanoSerializer):
    # Content for _links:
    serializer_url_field = AdjacentLink
    adjacencies = None
    adjacent = IdentityLinksField(
        view_name="panorama-detail",
        lookup_field="pano_id",
        format="html",
        read_only=True,
    )
    transitive_adjacencies = IdentityLinksField(
        view_name="panorama-adjacencies",
        lookup_field="pano_id",
        format="html",
        read_only=True,
    )

    # Additional regular attributes:
    distance = serializers.DecimalField(
        max_digits=20, decimal_places=2, source="relative_distance"
    )
    direction = serializers.DecimalField(
        max_digits=20, decimal_places=2, source="relative_heading"
    )
    angle = serializers.DecimalField(
        max_digits=20, decimal_places=2, source="relative_pitch"
    )
    elevation = serializers.DecimalField(
        max_digits=20, decimal_places=2, source="relative_elevation"
    )

    class Meta(PanoSerializer.Meta):
        model = Adjacencies
        listresults_field = "adjacencies"


class ThumbnailSerializer(serializers.ModelSerializer):
    heading = serializers.DecimalField(max_digits=20, decimal_places=2)
    pano_id = serializers.ReadOnlyField()
    url = serializers.ReadOnlyField()

    class Meta:
        model = Panorama
        fields = ("url", "heading", "pano_id")

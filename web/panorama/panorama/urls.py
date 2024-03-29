# Packages
from django.conf import settings
from django.urls import include, re_path
from rest_framework import renderers
from rest_framework import response
from rest_framework import routers
from rest_framework import schemas
from rest_framework.decorators import api_view, renderer_classes
from rest_framework_swagger.renderers import OpenAPIRenderer
from rest_framework_swagger.renderers import SwaggerUIRenderer

from .view_imgs import ThumbnailViewSet
from .views import PanoramaViewSet


class PanoramaView(routers.APIRootView):
    """
    De panoramas van de stad worden in een lijst getoond

    - panorama's
    - thumbnails
    - recente panorama's
    """


class PanoramaRouter(routers.DefaultRouter):
    """
    Panoramabeelden Amsterdam

    Deze api geeft toegang tot de panorama beelden van de Gemeente Amsterdam en omstreken.
    """

    APIRootView = PanoramaView


panorama = PanoramaRouter()
panorama.register("thumbnail", ThumbnailViewSet, basename="thumbnail")
panorama.register("panoramas", PanoramaViewSet, basename="panorama")

APIS = [re_path(r"^panorama/", include(panorama.urls))]


@api_view()
@renderer_classes([SwaggerUIRenderer, OpenAPIRenderer, renderers.CoreJSONRenderer])
def swagger_schema_view(request):
    generator = schemas.SchemaGenerator(
        title="Panoramabeelden Amsterdam API", patterns=APIS
    )
    return response.Response(generator.get_schema(request=request))


urlpatterns = APIS + [
    re_path(r"^status/", include("health.urls")),
    re_path("^panorama/docs/$", swagger_schema_view),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        re_path(r"^__debug__/", include(debug_toolbar.urls)),
    ]

from rest_framework.routers import DefaultRouter
from voto.api.views import VotoApiViewSet

router_voto = DefaultRouter()

router_voto.register(
    prefix='voto',
    basename='voto',
    viewset=VotoApiViewSet
)
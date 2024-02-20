from rest_framework.routers import DefaultRouter
from etapaRango.api.views import EtapaRangoViewSet

router_etapaRango = DefaultRouter()

router_etapaRango.register(
    prefix='etapaRango',
    basename='etapaRango',
    viewset=EtapaRangoViewSet
)
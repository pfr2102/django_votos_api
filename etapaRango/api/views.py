from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from etapaRango.models import EtapaRango
from etapaRango.api.serializers import EtapaRangoSerializer

class EtapaRangoViewSet(ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = EtapaRangoSerializer
    queryset = EtapaRango.objects.all()


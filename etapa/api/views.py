from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from etapa.models import Etapa
from etapa.api.serializers import EtapaSerializer


class EtapaApiViewSet(ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Etapa.objects.all().order_by('id')
    serializer_class = EtapaSerializer
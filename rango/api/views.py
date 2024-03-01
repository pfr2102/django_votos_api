from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rango.models import Rango
from rango.api.serializers import RangoSerializer


class RangoApiViewSet(ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Rango.objects.all().order_by('id')
    serializer_class = RangoSerializer
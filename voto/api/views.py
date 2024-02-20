from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from voto.models import Voto
from voto.api.serializers import VotoSerializer


class VotoApiViewSet(ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Voto.objects.all()
    serializer_class = VotoSerializer
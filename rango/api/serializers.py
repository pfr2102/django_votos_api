from rest_framework.serializers import ModelSerializer
from rango.models import Rango


class RangoSerializer(ModelSerializer):
    class Meta:
        model = Rango
        fields = ['id', 'name']
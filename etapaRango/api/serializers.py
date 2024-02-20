from rest_framework.serializers import ModelSerializer
from etapaRango.models import EtapaRango

class EtapaRangoSerializer(ModelSerializer):
    class Meta:
        model = EtapaRango
        fields = ['id', 'id_etapa', 'id_rango', 'tot_ganadores']

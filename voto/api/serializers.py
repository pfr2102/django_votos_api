from rest_framework.serializers import ListSerializer
from rest_framework.serializers import ModelSerializer
from voto.models import Voto

class VotoSerializer(ModelSerializer):
    class Meta:
        model = Voto
        fields = ['id_voto', 'id_emp_votante_fk', 'id_emp_candidato_fk', 'id_rango_fk', 'id_etapa_fk', 'fecha_voto', 'estatus_revocacion']


class VotoListSerializer(ListSerializer):
    def create(self, validated_data):
        votos = [Voto(**item) for item in validated_data]
        return Voto.objects.bulk_create(votos)
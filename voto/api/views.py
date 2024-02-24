from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from voto.models import Voto
from voto.api.serializers import VotoSerializer

#Otras importaciones para las consultas
from rest_framework.decorators import action
from django.db.models import Count, F, Value
from django.db.models.functions import Concat, TruncYear
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class VotoApiViewSet(ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Voto.objects.all()
    serializer_class = VotoSerializer

    #Peticion para crear votos de forma masiva
    @action(detail=False, methods=['POST'])
    def create_votosM(self, request, *args, **kwargs):
        # Utiliza el serializador VotoSerializer en lugar de VotoListSerializer
        serializer = self.get_serializer(data=request.data, many=isinstance(request.data, list))
        if serializer.is_valid():
            # Itera sobre los datos y crea un objeto Voto para cada conjunto de datos
            for data in serializer.validated_data:
                Voto.objects.create(**data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    #Peticion para obtener el total de votos
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('id_etapa_fk', openapi.IN_QUERY, description="Número de etapa", type=openapi.TYPE_STRING),
            openapi.Parameter('id_rango_fk', openapi.IN_QUERY, description="Número de rango", type=openapi.TYPE_STRING),
            openapi.Parameter('fecha_voto', openapi.IN_QUERY, description="Fecha de voto (opcional)", type=openapi.TYPE_STRING, format='date'),
        ],
        responses={200: VotoSerializer(many=True)},
    )
    @action(detail=False, methods=['GET'])
    def count_votes(self, request):
        id_etapa_fk = request.query_params.get('id_etapa_fk')
        id_rango_fk = request.query_params.get('id_rango_fk')
        fecha_voto_str = request.query_params.get('fecha_voto')

        filters = {'estatus_revocacion': False}

        if id_etapa_fk:
            filters['id_etapa_fk'] = id_etapa_fk

        if id_rango_fk:
            filters['id_rango_fk'] = id_rango_fk

        if fecha_voto_str:
            filters['fecha_voto__year'] = fecha_voto_str

        counts = (
            Voto.objects
            .filter(**filters)
            .values(
                    'id_etapa_fk',
                    'id_rango_fk', 
                    'id_emp_candidato_fk', 
                    image=F('id_emp_candidato_fk__image'), 
                    workstation=F('id_emp_candidato_fk__workstation'),
                    dependency=F('id_emp_candidato_fk__dependency'),
                    num_empleado=F('id_emp_candidato_fk__username') 
                 ) 
            .annotate( 
                    full_name=Concat('id_emp_candidato_fk__first_name', Value(' '), 'id_emp_candidato_fk__last_name'),                 
                    year=TruncYear('fecha_voto'), 
                    total=Count('id_voto')
                )   
            .order_by('-total')
        )


        return Response(counts, status=status.HTTP_200_OK)

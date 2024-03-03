from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from voto.models import Voto
from voto.api.serializers import VotoSerializer

#Otras importaciones para las consultas
from rest_framework.decorators import action
from django.db import models
from django.db.models import Count, F, Value, CharField
from django.db.models.functions import Concat, TruncYear, TruncDate
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class VotoApiViewSet(ModelViewSet):
    #para usar todas las funcionalidades de esta view en todas las rutas se necesita mandar el
    # token de autenticación en el header la de solicitud http
    permission_classes = [IsAuthenticated] #es por eso que se indica el IsAuthenticated
    queryset = Voto.objects.all()
    serializer_class = VotoSerializer


#-------------------------------------------------------------------------------------------------------------------
    #Peticion para crear votos de forma masiva
    @action(detail=False, methods=['POST'])
    def create_votosM(self, request, *args, **kwargs):
        """
        Crea votos de forma masiva.

        Permite crear votos en grandes cantidades proporcionando una lista de datos de votos.
        ---
        # Parámetros
        - Se espera una solicitud POST con una lista de datos de votos.
        - Cada dato de voto debe tener el formato requerido por el serializador VotoSerializer.

        # Retorna
        - En caso de éxito, retorna una respuesta con los datos de los votos creados y el código de estado 201 (Created).
        - En caso de error, retorna los errores de validación con el código de estado 400 (Bad Request).
        """
        # Utiliza el serializador VotoSerializer en lugar de VotoListSerializer
        serializer = self.get_serializer(data=request.data, many=isinstance(request.data, list))
        if serializer.is_valid():
            # Itera sobre los datos y crea un objeto Voto para cada conjunto de datos
            for data in serializer.validated_data:
                Voto.objects.create(**data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#-------------------------------------------------------------------------------------------------------------------
    #Peticion para obtener el total de votos por rango , etapa y fecha (fecha es el año)
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('id_etapa_fk', openapi.IN_QUERY, description="Número de etapa", type=openapi.TYPE_STRING),
            openapi.Parameter('id_rango_fk', openapi.IN_QUERY, description="Número de rango", type=openapi.TYPE_STRING),
            openapi.Parameter('fecha_voto', openapi.IN_QUERY, description="Año voto", type=openapi.TYPE_STRING, format='date'),
        ],
        responses={200: VotoSerializer(many=True)},
    )
    @action(detail=False, methods=['GET'])
    def count_votes(self, request):
        """
        Obtiene el total de votos por rango, etapa y fecha.

        ---
        # Parámetros:
        - id_etapa_fk: Número de etapa.
        - id_rango_fk: Número de rango.
        - fecha_voto: Fecha de voto en formato de año.
    
        # Retorna:
        - una lista de la cantidad de votos por electo con información detallada de mayor a menor.
        """
        # Obtener la URL base para concatenarlo con la url de la imagen
        base_url = request.build_absolute_uri('/uploads/')

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
                    workstation=F('id_emp_candidato_fk__workstation'),
                    dependency=F('id_emp_candidato_fk__dependency'),
                    num_empleado=F('id_emp_candidato_fk__username') 
                 ) 
            .annotate( 
                    image=Concat( Value(base_url),'id_emp_candidato_fk__image',output_field=CharField() ), 
                    full_name=Concat('id_emp_candidato_fk__first_name', Value(' '), 'id_emp_candidato_fk__last_name'),                 
                    year=TruncYear('fecha_voto'), 
                    total=Count('id_voto')
                )   
            .order_by('-total')
        )

        return Response(counts, status=status.HTTP_200_OK)
        

#-------------------------------------------------------------------------------------------------------------------
     # Peticion para obtener el total de votos por rango, etapa y fecha (fecha es el año)
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('id_etapa_fk', openapi.IN_QUERY, description="Número de etapa", type=openapi.TYPE_STRING),
            openapi.Parameter('id_rango_fk', openapi.IN_QUERY, description="Número de rango", type=openapi.TYPE_STRING),
            openapi.Parameter('fecha_voto', openapi.IN_QUERY, description="Año voto", type=openapi.TYPE_STRING, format='date'),
            openapi.Parameter('top', openapi.IN_QUERY, description="Número de registros a retornar", type=openapi.TYPE_INTEGER),
        ],
        responses={200: VotoSerializer(many=True)},
    )
    @action(detail=False, methods=['GET'])
    def count_votesTop(self, request):
        """
        Obtiene el total de votos por rango, etapa y año, limitado por un Tope de registros.

        # Parámetros:
        - id_etapa_fk: Número de etapa.
        - id_rango_fk: Número de rango.
        - fecha_voto: Año de voto.
        - top: Número de registros a retornar (opcional).

        # Retorna:
        - Lista de votos con información detallada, ordenada por el total de votos de mayor a menor.
        """
        # Obtener la URL base para concatenarlo con la url de la imagen
        base_url = request.build_absolute_uri('/uploads/')

        id_etapa_fk = request.query_params.get('id_etapa_fk')
        id_rango_fk = request.query_params.get('id_rango_fk')
        fecha_voto_str = request.query_params.get('fecha_voto')
        top_count = request.query_params.get('top')  # Obtener el parámetro "top"

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
                    #image=F('id_emp_candidato_fk__image'), 
                    workstation=F('id_emp_candidato_fk__workstation'),
                    dependency=F('id_emp_candidato_fk__dependency'),
                    num_empleado=F('id_emp_candidato_fk__username') 
                 ) 
            .annotate( 
                    image=Concat( Value(base_url),'id_emp_candidato_fk__image',output_field=CharField() ), 
                    full_name=Concat('id_emp_candidato_fk__first_name', Value(' '), 'id_emp_candidato_fk__last_name'),                 
                    year=TruncYear('fecha_voto'), 
                    total=Count('id_voto')
                )   
            .order_by('-total')[:int(top_count)] if top_count else None  # Aplicar el recuento superior si se proporciona
        )

        return Response(counts, status=status.HTTP_200_OK)


    
#-------------------------------------------------------------------------------------------------------------------
# Peticion para obtener todos los votos sin contabilizar por rango, etapa y fecha
    @swagger_auto_schema(
    manual_parameters=[
        openapi.Parameter('id_etapa_fk', openapi.IN_QUERY, description="Número de etapa", type=openapi.TYPE_STRING),
        openapi.Parameter('id_rango_fk', openapi.IN_QUERY, description="Número de rango", type=openapi.TYPE_STRING),
        openapi.Parameter('fecha_voto', openapi.IN_QUERY, description="Año voto", type=openapi.TYPE_STRING, format='date'),
    ],
    responses={200: VotoSerializer(many=True)},
    )
    @action(detail=False, methods=['GET'])
    def get_all_votes(self, request):
        """
        Obtiene todos los registros de la tabla votos filtrandolos por rango, etapa y fecha, (sin contabilizar) .

        ---
        # Parámetros:
        - id_etapa_fk: Número de etapa.
        - id_rango_fk: Número de rango.
        - fecha_voto: Fecha de voto en formato de año.
        
        # Retorna:
        - una lista de todos los registros de votos sin contabilizar.
        """
        id_etapa_fk = request.query_params.get('id_etapa_fk')
        id_rango_fk = request.query_params.get('id_rango_fk')
        fecha_voto_str = request.query_params.get('fecha_voto')

        filters = {}
        #filters = {'estatus_revocacion': False}

        if id_etapa_fk:
            filters['id_etapa_fk'] = id_etapa_fk

        if id_rango_fk:
            filters['id_rango_fk'] = id_rango_fk

        if fecha_voto_str:
            filters['fecha_voto__year'] = fecha_voto_str
            
        votes = (
            Voto.objects
            .filter(**filters)
            .values(
                'id_etapa_fk',
                'id_rango_fk',
                'id_emp_candidato_fk',
                nombre_candidato=Concat('id_emp_candidato_fk__first_name' , Value(' '), 'id_emp_candidato_fk__last_name'),
                fecha_voto_trunc=TruncDate('fecha_voto'),                                
            )
        )
        
        return Response(votes, status=status.HTTP_200_OK)


#-------------------------------------------------------------------------------------------------------------------
    # Acción para verificar la existencia de registros con la fk, la etapa y el año proporcionados
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('id_emp_votante_fk', openapi.IN_QUERY, description="Número de empleado del votante", type=openapi.TYPE_STRING),
            openapi.Parameter('id_etapa_fk', openapi.IN_QUERY, description="Número de etapa", type=openapi.TYPE_STRING),
            openapi.Parameter('fecha_voto', openapi.IN_QUERY, description="Año voto", type=openapi.TYPE_STRING, format='date'),
        ],
        responses={200: openapi.TYPE_BOOLEAN},  # Cambiado a openapi.TYPE_BOOLEAN
    )
    @action(detail=False, methods=['GET'])
    def check_vote_exists(self, request):
        """
        Verifica la existencia de un voto basado en el número de empleado del votante, el número de etapa y el año de voto.

        # Parámetros:
        - id_emp_votante_fk: Número de empleado del votante.
        - id_etapa_fk: Número de etapa.
        - fecha_voto: Año de voto.

        # Retorna:
        - True si existe un voto con las condiciones dadas, False de lo contrario.
        """
        id_emp_votante_fk = request.query_params.get('id_emp_votante_fk')
        id_etapa_fk = request.query_params.get('id_etapa_fk')
        fecha_voto_str = request.query_params.get('fecha_voto')

        filters = {'id_emp_votante_fk': id_emp_votante_fk, 'id_etapa_fk': id_etapa_fk, 'fecha_voto__year': fecha_voto_str}

        exists = Voto.objects.filter(**filters).exists()

        return Response(exists, status=status.HTTP_200_OK)
    


#-------------------------------------------------------------------------------------------------------------------
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('id_emp_candidato_fk', openapi.IN_QUERY, description="ID del candidato a actualizar", type=openapi.TYPE_INTEGER),
        ],
        responses={
            status.HTTP_200_OK: openapi.Response("Se actualizaron registros", example={'message': 'Se actualizaron registros.'}),
            status.HTTP_404_NOT_FOUND: openapi.Response("No se encontraron registros", example={'message': 'No se encontraron registros para actualizar.'}),
            status.HTTP_500_INTERNAL_SERVER_ERROR: openapi.Response("Error interno del servidor", example={'error': 'Mensaje de error.'}),
        },
    )
    @action(detail=False, methods=['GET'])
    def update_votes_revocation(self, request):
        """
        Actualiza el campo estatus_revocacion a True para los registros específicos de votos.

        Actualiza el campo estatus_revocacion a True para los registros específicos de un candidato para ya no contabilizarlos en caso de una revocatoría.
        
        # Parámetros:
        - id_emp_candidato_fk (int): ID del candidato a actualizar.

        # Retorna:
        - 200 OK: Se actualizaron registros. Ejemplo: {'message': 'Se actualizaron registros.'}
        - 404 Not Found: No se encontraron registros para actualizar. Ejemplo: {'message': 'No se encontraron registros para actualizar.'}
        - 500 Internal Server Error: Error interno del servidor. Ejemplo: {'error': 'Mensaje de error.'}
        """
        try:
            id_emp_candidato_fk = request.query_params.get('id_emp_candidato_fk')

            current_year = timezone.now().year
            print(id_emp_candidato_fk)
            print(current_year)
            # Actualizar el campo estatus_revocacion a True para los registros específicos
            filters = {'id_emp_candidato_fk': id_emp_candidato_fk}    

            updated_rows = (
                 Voto.objects
                 .filter(**filters)
                 .update(estatus_revocacion=True)
             )

            if updated_rows > 0:
                 return Response({'message': f'Se actualizaron {updated_rows} registros.'}, status=status.HTTP_200_OK)
            else:
                 return Response({'message': 'No se encontraron registros para actualizar.'}, status=status.HTTP_404_NOT_FOUND) 
        

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
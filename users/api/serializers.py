from rest_framework import serializers
from users.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username', 'first_name', 
                  'last_name', 'password', 'is_active', 'is_staff', 'nombre', 'dependencia', 'puesto', 'edad', 'antiguedad', 'rango' ]
        #nota: el username se usa para numero_empleado

        
        """ fields = ['id', 'username', 'email', 'first_name', 
                  'last_name', 'password', 'is_active', 'is_staff'] """
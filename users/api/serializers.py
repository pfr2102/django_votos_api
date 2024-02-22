from rest_framework import serializers
from users.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username', 'first_name', 
                  'last_name', 'password', 'is_active', 'is_staff', 'dependency', 'workstation', 'antiquity', 'id_rank_fk', 'image' ]
        #nota: rank se usa para rango
        #nota: el username se usa para numero_empleado

        
        """ fields = ['id', 'username', 'email', 'first_name', 
                  'last_name', 'password', 'is_active', 'is_staff'] """
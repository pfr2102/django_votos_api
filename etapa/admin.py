from django.contrib import admin
from etapa.models import Etapa

@admin.register(Etapa)
class EtapaAdmin(admin.ModelAdmin):
    pass
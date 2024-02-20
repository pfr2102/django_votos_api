from django.contrib import admin
from etapaRango.models import EtapaRango

@admin.register(EtapaRango)
class EtapaRangoAdmin(admin.ModelAdmin):
    pass
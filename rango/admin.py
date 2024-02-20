from django.contrib import admin
from rango.models import Rango

@admin.register(Rango)
class RangoAdmin(admin.ModelAdmin):
    pass
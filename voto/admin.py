from django.contrib import admin
from voto.models import Voto

@admin.register(Voto)
class VotoAdmin(admin.ModelAdmin):
    pass
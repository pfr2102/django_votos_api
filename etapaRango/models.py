from django.db import models

class EtapaRango(models.Model):
    id = models.AutoField(primary_key=True)    
    id_etapa = models.ForeignKey('etapa.Etapa', on_delete=models.SET_NULL, null=True, blank=True)
    id_rango = models.ForeignKey('rango.Rango', on_delete=models.SET_NULL, null=True, blank=True)
    tot_ganadores = models.IntegerField(null=True, blank=True)


from django.db import models

class Voto(models.Model):
    id_voto = models.AutoField(primary_key=True)        
    id_emp_votante_fk = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='votos_como_votante')
    id_emp_candidato_fk = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='votos_como_candidato')
    id_rango_fk = models.ForeignKey('rango.Rango', on_delete=models.SET_NULL, null=True, blank=True)
    id_etapa_fk = models.ForeignKey('etapa.Etapa', on_delete=models.SET_NULL, null=True, blank=True)
    fecha_voto = models.DateTimeField(auto_now=True)
    estatus_revocacion = models.BooleanField(default=False, null=True, blank=True)


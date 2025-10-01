from django.db import models
from datetime import timedelta

class Estadia(models.Model):
    idEstadia = models.AutoField(primary_key=True, verbose_name='ID Estadia')
    entrada = models.DateTimeField('Entrada', help_text='Data e hora de entrada')
    saida = models.DateTimeField('Saída',  blank= True, null= True, help_text='Data e hora de saída')

    class Meta:
        verbose_name = 'Estadia'
        verbose_name_plural = 'Estadias'

    def __str__(self):
        return f'Estadia {self.idEstadia} - Entrada: {self.entrada.strftime("%d/%m/%Y %H:%M")}'

    @property
    def permanencia(self):
        if self.entrada and self.saida:
            delta = self.saida - self.entrada
            horas, resto = divmod(delta.total_seconds(), 3600)
            minutos, segundos = divmod(resto, 60)
            return f"{int(horas)}h {int(minutos)}m"
        return "Em andamento"

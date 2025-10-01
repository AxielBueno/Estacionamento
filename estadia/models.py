from django.db import models
from datetime import timedelta

class Estadia(models.Model):
    idEstadia = models.AutoField(primary_key=True, verbose_name='ID Estadia')
    entrada = models.DateTimeField('Entrada', help_text='Data e hora de entrada')
    saida = models.DateTimeField('Saída', help_text='Data e hora de saída')

    class Meta:
        verbose_name = 'Estadia'
        verbose_name_plural = 'Estadias'

    def __str__(self):
        return f'Estadia {self.idEstadia} - Entrada: {self.entrada.strftime("%d/%m/%Y %H:%M")}'

    @property
    def permanencia(self):
        if self.entrada and self.saida:
            return self.saida - self.entrada
        return timedelta(0)

from django.core.exceptions import ValidationError
from django.db import models
from datetime import timedelta

class Estadia(models.Model):
    idEstadia = models.AutoField(primary_key=True, verbose_name='ID Estadia')
    entrada = models.DateTimeField('Entrada', help_text='Data e hora de entrada')
    saida = models.DateTimeField('Saída',  blank= True, null= True, help_text='Data e hora de saída')

    vaga = models.ForeignKey(
        'vaga.Vaga',
        on_delete=models.CASCADE,
        related_name='estadias',
        verbose_name='Vaga',
        help_text='Vaga que será ocupada',
        blank=True,
        null=True,
    )

    veiculo = models.ForeignKey(
        'veiculo.Veiculo',
        on_delete=models.CASCADE,
        related_name='estadias',
        verbose_name='Veículo',
        help_text='Veiculo para ser estacionado',
        blank=True,
        null=True,
    )


    class Meta:
        verbose_name = 'Estadia'
        verbose_name_plural = 'Estadias'

        constraints = [
            models.UniqueConstraint(
                fields=['vaga'],
                condition=models.Q(saida__isnull=True),
                name='unique_vaga_ativa'
            ),
            models.UniqueConstraint(
                fields=['veiculo'],
                condition=models.Q(saida__isnull=True),
                name='unique_veiculo_ativo'
            ),
        ]

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

    def clean(self):
        errors = {}

        if self.vaga and Estadia.objects.filter(vaga=self.vaga, saida__isnull=True).exclude(pk=self.pk).exists():
            errors['vaga'] = "Vaga já está ocupada"

        if self.veiculo and Estadia.objects.filter(veiculo=self.veiculo, saida__isnull=True).exclude(
                pk=self.pk).exists():
            errors['veiculo'] = "Veículo já está estacionado"

        if errors:
            raise ValidationError(errors)


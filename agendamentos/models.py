from django.db import models
from django.utils import timezone
from datetime import timedelta


class Agendamento(models.Model):
    placa = models.ForeignKey(
        'veiculo.Veiculo',
        on_delete=models.CASCADE,
        related_name='agendamentos',
        verbose_name='Placa'
    )

    dono = models.ForeignKey(
        'pessoa.Pessoa',
        on_delete=models.CASCADE,
        related_name='agendamentos',
        verbose_name='Dono'
    )

    funcionario = models.ForeignKey(
        'funcionarios.Funcionario',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='agendamentos',
        verbose_name='Funcionário Responsável'
    )

    entrada = models.DateTimeField('Entrada', help_text='Data e hora de entrada')
    saida_prevista = models.DateTimeField('Saída Prevista', help_text='Data e hora prevista de saída')
    saida = models.DateTimeField('Saída Real', null=True, blank=True, help_text='Data e hora real de saída')

    valor = models.DecimalField('Valor', max_digits=8, decimal_places=2, editable=False, default=0.00)

    class Meta:
        verbose_name = 'Agendamento'
        verbose_name_plural = 'Agendamentos'
        ordering = ['-entrada']

    def __str__(self):
        return f'Agendamento {self.placa} - {self.dono.nome}'

    def save(self, *args, **kwargs):
        if self.saida_prevista and self.entrada:
            tempo = self.saida_prevista - self.entrada
            horas = tempo.total_seconds() / 3600
            self.valor = round(horas * 5, 2)
        super().save(*args, **kwargs)

    def clean(self):
        from django.core.exceptions import ValidationError
        if self.saida_prevista and self.entrada and self.saida_prevista < self.entrada:
            raise ValidationError({'saida_prevista': 'A saída prevista não pode ser menor que a entrada.'})

from django.db import models
from django.utils import timezone


class ValorHora(models.Model):
    valor_vigente = models.DecimalField(
        'Valor da Hora (R$)',
        max_digits=6,
        decimal_places=2,
        help_text='Valor atual da hora de estacionamento'
    )

    data_alteracao = models.DateTimeField(
        'Data da Alteração',
        default=timezone.now,
        help_text='Momento em que o valor foi atualizado'
    )

    class Meta:
        verbose_name = 'Valor da Hora'
        verbose_name_plural = 'Valores da Hora'
        ordering = ['-data_alteracao']  # mais recente primeiro

    def __str__(self):
        return f"R$ {self.valor_vigente} (alterado em {self.data_alteracao.strftime('%d/%m/%Y %H:%M')})"

from django.db import models
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal
from funcionarios.models import Funcionario
from pessoa.models import Cliente
from veiculo.models import Veiculo


class Agendamento(models.Model):

    placa = models.ForeignKey(Veiculo, on_delete=models.CASCADE, related_name='agendamentos', verbose_name='Placa')
    dono = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='agendamentos',verbose_name='Dono')
    funcionario = models.ForeignKey(Funcionario, on_delete=models.CASCADE, related_name='agendamentos',verbose_name='Funcionario')

    entrada = models.DateTimeField('Entrada', help_text='Data e hora de entrada')
    saida_prevista = models.DateTimeField('Saída Prevista', help_text='Data e hora prevista de saída')
    saida = models.DateTimeField('Saída Real', null=True, blank=True, help_text='Data e hora real de saída')

    valor = models.DecimalField('Valor', max_digits=8, decimal_places=2, editable=False, default=0.00)

    STATUS_CHOICES = [
        ('andamento', 'Em Andamento'),
        ('finalizado', 'Finalizado'),
        ('cancelado', 'Cancelado'),
    ]

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='andamento', verbose_name='Status')

    class Meta:
        verbose_name = 'Agendamento'
        verbose_name_plural = 'Agendamentos'
        ordering = ['-entrada']

    def __str__(self):
        return f'Agendamento {self.placa} - {self.dono.nome}'

    def save(self, *args, **kwargs):
        if self.entrada:
            fim = self.saida if self.saida else self.saida_prevista
            if fim:
                tempo = fim - self.entrada
                horas = tempo.total_seconds() / 3600
                self.valor = Decimal(horas) * Decimal('5.00')
            else:
                self.valor = Decimal('0.00')
        else:
            self.valor = Decimal('0.00')
        super().save(*args, **kwargs)

    def clean(self):
        from django.core.exceptions import ValidationError
        if self.saida_prevista and self.entrada and self.saida_prevista < self.entrada:
            raise ValidationError({'saida_prevista': 'A saída prevista não pode ser menor que a entrada.'})

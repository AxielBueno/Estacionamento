from django.db import models
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal
from funcionarios.models import Funcionario
from pessoa.models import Cliente
from veiculo.models import Veiculo

class Agendamento(models.Model):

    placa = models.OneToOneField(Veiculo, on_delete=models.CASCADE, related_name='agendamentos', verbose_name='Placa')
    dono = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='agendamentos',verbose_name='Responsavel')
    funcionario = models.ForeignKey(Funcionario, on_delete=models.CASCADE, related_name='agendamentos',verbose_name='Funcionario')
    entrada = models.DateTimeField('Entrada', help_text='Data e hora de entrada')
    saida_prevista = models.DateTimeField('Saída Prevista', help_text='Data e hora prevista de saída (Saida não pode ser antes da ENTRADA)')
    saida = models.DateTimeField('Saída Real', null=True, blank=True, help_text='Data e hora real de saída')
    valor = models.DecimalField('Valor', max_digits=8, decimal_places=2, editable=False, default=0.00)
    pago = models.BooleanField(default=False)
    metodo_pagamento = models.CharField(max_length=20, null=True, blank=True)
    valor_desconto = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    valor_final = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    STATUS_CHOICES = [
        ('andamento', 'Em Andamento'),
        ('finalizado', 'Finalizado'),
        ('cancelado', 'Cancelado'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='andamento', verbose_name='Status')

    class Meta:
        permissions = (('fechar_agendamento', 'Permite fazer o fechamento de um agendamento'),)
        verbose_name = 'Agendamento'
        verbose_name_plural = 'Agendamentos'
        ordering = ['-entrada']

    def __str__(self):
        return f'Agendamento {self.placa} - {self.dono.nome}'

    # Calcula valor com base na duração
    def save(self, *args, **kwargs):
        from valor.models import ValorHora  # evitar ciclos

        valor_hora_obj = ValorHora.objects.first()
        valor_hora = valor_hora_obj.valor_vigente if valor_hora_obj else 5

        if self.entrada:
            fim = self.saida if self.saida else self.saida_prevista
            if fim:
                tempo = fim - self.entrada
                horas = tempo.total_seconds() / 3600
                self.valor = Decimal(horas) * Decimal(valor_hora)
            else:
                self.valor = Decimal('0.00')
        else:
            self.valor = Decimal('0.00')

        super().save(*args, **kwargs)

    # Valida saída prevista
    def clean(self):
        from django.core.exceptions import ValidationError
        if self.saida_prevista and self.entrada and self.saida_prevista < self.entrada:
            raise ValidationError({'saida_prevista': 'A saída prevista não pode ser menor que a entrada.'})

    # ==== NOVO: propriedades de cálculo ====

    @property
    def valor_base(self):
        """Valor base calculado pelo tempo/hora."""
        return round(self.valor, 2)

    @property
    def desconto_juridico(self):
        """20% de desconto para clientes jurídicos (exemplo: empresa cadastrada)."""
        if hasattr(self.dono, 'empresa') and self.dono.empresa.exists():
            return round(self.valor_base * Decimal('0.20'), 2)
        return Decimal('0.00')

    def desconto_pix_debito(self):
        """10% de desconto para pagamento via PIX ou débito."""
        if self.metodo_pagamento and self.metodo_pagamento.lower() in ['pix', 'debito']:
            return round(self.valor_base * Decimal('0.10'), 2)
        return Decimal('0.00')

    @property
    def valor_final(self):
        """Valor final após aplicar todos os descontos."""
        return self.valor_base - self.desconto_juridico - self.desconto_pix_debito()

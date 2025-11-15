from django.db import models
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal
from funcionarios.models import Funcionario
from pessoa.models import Cliente
from veiculo.models import Veiculo


class Agendamento(models.Model):

    placa = models.OneToOneField(Veiculo, on_delete=models.CASCADE, related_name='agendamentos', verbose_name='Placa')
    dono = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='agendamentos', verbose_name='Responsavel')
    funcionario = models.ForeignKey(Funcionario, on_delete=models.CASCADE, related_name='agendamentos', verbose_name='Funcionario')
    entrada = models.DateTimeField('Entrada', help_text='Data e hora de entrada')
    saida_prevista = models.DateTimeField('Saída Prevista', help_text='Data e hora prevista de saída (Saida não pode ser antes da ENTRADA)')
    saida = models.DateTimeField('Saída Real', null=True, blank=True, help_text='Data e hora real de saída')
    valor = models.DecimalField('Valor', max_digits=8, decimal_places=2, editable=False, default=0.00)
    pago = models.BooleanField(default=False)
    valor_final = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    metodo_pagamento = models.CharField(max_length=20, null=True, blank=True)
    valor_desconto = models.DecimalField(max_digits=10, decimal_places=2, default=0)

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

    # ======================
    # CÁLCULO DO VALOR BASE
    # ======================
    def save(self, *args, **kwargs):
        from valor.models import ValorHora

        valor_hora_obj = ValorHora.objects.first()
        valor_hora = Decimal(valor_hora_obj.valor_vigente) if valor_hora_obj else Decimal('5.00')

        if self.entrada:
            fim = self.saida if self.saida else self.saida_prevista
            if fim:
                tempo = fim - self.entrada
                horas = Decimal(tempo.total_seconds()) / Decimal('3600')

                # mínimo de 1 hora
                if horas < Decimal('1.0'):
                    horas = Decimal('1.0')

                self.valor = (horas * valor_hora).quantize(Decimal('0.01'))
            else:
                self.valor = Decimal('0.00')
        else:
            self.valor = Decimal('0.00')

        super().save(*args, **kwargs)

    # ======================
    # VALIDAÇÃO
    # ======================
    def clean(self):
        from django.core.exceptions import ValidationError
        if self.saida_prevista and self.entrada and self.saida_prevista < self.entrada:
            raise ValidationError({'saida_prevista': 'A saída prevista não pode ser menor que a entrada.'})

    # ======================
    #   PROPRIEDADES
    # ======================
    @property
    def valor_base(self):
        return Decimal(self.valor).quantize(Decimal('0.01'))

    @property
    def desconto_juridico(self):
        """20% de desconto para clientes jurídicos — retorno apenas, NÃO aplica."""
        if hasattr(self.dono, 'empresa') and self.dono.empresa.exists():
            return (self.valor_base * Decimal('0.20')).quantize(Decimal('0.01'))
        return Decimal('0.00')

    def desconto_pix_debito(self):
        """10% só após salvar metodo_pagamento."""
        if self.metodo_pagamento and self.metodo_pagamento.lower() in ['pix', 'debito']:
            return (self.valor_base * Decimal('0.10')).quantize(Decimal('0.01'))
        return Decimal('0.00')

    # ========================================
    #  CÁLCULO P/ EXIBIÇÃO NA PÁGINA DE PAGAR
    # ========================================
    def calcular_valor_final(self, aplicar_pix_debito=False):
        """
        Usa APENAS para exibir na tela.
        NÃO grava nada no banco.
        """
        total_desconto = self.desconto_juridico

        if aplicar_pix_debito:
            total_desconto += (self.valor_base * Decimal('0.10')).quantize(Decimal('0.01'))

        return (self.valor_base - total_desconto).quantize(Decimal('0.01'))

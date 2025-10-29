from django.db import models
from django.core.exceptions import ValidationError
from decimal import Decimal
from pessoa.models import Cliente  # importando o dono
from estadia.models import Estadia  # para pegar a permanência / tempo de estadia


class Pagamento(models.Model):
    METODO_CHOICES = [
        ('D', 'Débito'),
        ('C', 'Crédito'),
        ('P', 'Pix'),
    ]

    idPagamento = models.AutoField(primary_key=True, verbose_name='ID Pagamento')

    valorHora = models.DecimalField('Valor Hora', max_digits=6, decimal_places=2, default=Decimal('5.00'))
    multa = models.DecimalField('Multa (%)', max_digits=4, decimal_places=2, default=Decimal('10.00'))

    metodo = models.CharField(
        'Método de Pagamento',
        max_length=1,
        choices=METODO_CHOICES,
        help_text='Selecione o método de pagamento (Débito, Crédito ou Pix)'
    )

    estadia = models.OneToOneField(
        Estadia,
        on_delete=models.CASCADE,
        related_name='pagamento',
        verbose_name='Estadia',
        help_text='Estadia associada ao pagamento'
    )

    dono = models.ForeignKey(
        Cliente,
        on_delete=models.CASCADE,
        related_name='pagamentos',
        verbose_name='Dono',
        help_text='Cliente responsável pelo pagamento'
    )

    placa = models.CharField('Placa', max_length=10, help_text='Placa do veículo')

    valorFinal = models.DecimalField('Valor Final', max_digits=8, decimal_places=2, default=Decimal('0.00'))

    data_pagamento = models.DateTimeField('Data do Pagamento', auto_now_add=True)

    multa_aplicada = models.BooleanField('Aplicar Multa?', default=False)

    class Meta:
        verbose_name = 'Pagamento'
        verbose_name_plural = 'Pagamentos'

    def __str__(self):
        return f'Pagamento {self.idPagamento} - {self.dono.nome}'

    def calcular_valor_final(self):
        """
        Calcula o valor final com base na estadia, método de pagamento e multa.
        """
        if not self.estadia.entrada or not self.estadia.saida:
            raise ValidationError("A estadia deve possuir entrada e saída para calcular o valor final.")

        # Calcula a diferença de tempo em horas
        delta = self.estadia.saida - self.estadia.entrada
        horas = Decimal(delta.total_seconds() / 3600)
        horas = horas.quantize(Decimal('1.00'))  # arredonda para 2 casas

        valor_base = horas * self.valorHora
        valor_final = valor_base

        # Aplica desconto de 10% se for Débito ou Crédito
        if self.metodo in ['D', 'C']:
            valor_final *= Decimal('0.90')

        # Aplica multa de 10% se marcada
        if self.multa_aplicada:
            valor_final *= Decimal('1.10')

        self.valorFinal = valor_final.quantize(Decimal('0.01'))

    def save(self, *args, **kwargs):
        # Recalcula o valor sempre que salvar
        self.calcular_valor_final()
        super().save(*args, **kwargs)

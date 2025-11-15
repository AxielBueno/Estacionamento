from django.db import models
from django.core.exceptions import ValidationError
from decimal import Decimal
from pessoa.models import Cliente  # importando o dono
from estadia.models import Estadia  # para pegar a permanência / tempo de estadia
from valor.models import ValorHora


class Pagamento(models.Model):
    METODO_CHOICES = [
        ('D', 'Débito'),
        ('C', 'Crédito'),
        ('P', 'Pix'),
    ]

    STATUS_CHOICES = [
        ('P', 'Pendente'),
        ('C', 'Concluído'),
    ]

    idPagamento = models.AutoField(primary_key=True, verbose_name='ID Pagamento')

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
    valor_multa = models.DecimalField('Valor da Multa (R$)', max_digits=8, decimal_places=2, default=Decimal('0.00'))
    valor_desconto = models.DecimalField('Desconto (R$)', max_digits=8, decimal_places=2, default=Decimal('0.00'))
    status = models.CharField('Status do pagamento', max_length=1, choices=STATUS_CHOICES, default='P')

    class Meta:
        verbose_name = 'Pagamento'
        verbose_name_plural = 'Pagamentos'

    def __str__(self):
        return f'Pagamento {self.idPagamento} - {self.dono.nome}'


    def get_valor_hora_vigente(self):
        ultimo = ValorHora.objects.order_by('-data_alteracao').first()
        if not ultimo:
            raise ValidationError("Nenhum valor de hora vigente cadastrado.")
        return ultimo.valor_vigente


    def calcular_valor_final(self):
        if not self.estadia.entrada or not self.estadia.saida:
            raise ValidationError("A estadia deve ter entrada e saída.")

        delta = self.estadia.saida - self.estadia.entrada
        horas = Decimal(delta.total_seconds() / 3600).quantize(Decimal('1.00'))

        # mínima de 1h
        if horas < 1:
            horas = Decimal('1.00')

        valor_hora = self.get_valor_hora_vigente()
        valor_base = horas * valor_hora
        valor_final = valor_base

        self.valor_desconto = Decimal('0.00')
        self.valor_multa = Decimal('0.00')

        # Desconto por método
        if self.metodo in ['D', 'P']:
            desconto = valor_base * Decimal('0.10')
            valor_final -= desconto
            self.valor_desconto = desconto.quantize(Decimal('0.01'))

        # Desconto por empresa
        if self.dono.empresa.exists():
            desconto_empresa = valor_final * Decimal('0.20')
            valor_final -= desconto_empresa
            self.valor_desconto += desconto_empresa.quantize(Decimal('0.01'))

        # Multa
        if self.multa_aplicada:
            multa_valor = valor_final * Decimal('0.10')
            valor_final += multa_valor
            self.valor_multa = multa_valor.quantize(Decimal('0.01'))

        self.valorFinal = valor_final.quantize(Decimal('0.01'))

    def save(self, *args, **kwargs):
        # Só o treco pra recalcular
        self.calcular_valor_final()
        super().save(*args, **kwargs)

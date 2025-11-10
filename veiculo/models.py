from django.db import models
from pessoa.models import Cliente

TIPO_VEICULO = [
    ('Carro', 'Carro'),
    ('Moto', 'Moto'),
    ('Caminhão', 'Caminhão'),
]

class Veiculo(models.Model):
    placa = models.CharField('Placa', max_length=5, unique=True, help_text='Placa do veículo')
    tipo = models.CharField('Tipo de Veículo', max_length=20, choices=TIPO_VEICULO)
    dono = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='veiculos', default=1)

    class Meta:
        verbose_name = 'Veículo'
        verbose_name_plural = 'Veículos'

    def __str__(self):
        return f"{self.placa}"
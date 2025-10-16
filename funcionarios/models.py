from django.db import models
from stdimage import StdImageField

CARGO_CHOICES = [
    ('Gerente', 'Gerente'),
    ('Atendente', 'Atendente'),
]

class Funcionario(models.Model):
    idFuncionario = models.AutoField(primary_key=True, verbose_name='ID Estadia')
    nome = models.CharField('Nome', max_length=50, help_text='Nome completo')
    cpf = models.CharField('CPF', max_length=11, help_text='CPF completo', unique=True)
    fone = models.CharField('Fone', max_length=11, help_text='Número de telefone', unique=True)
    cargo = models.CharField('Cargo', max_length=20, choices=CARGO_CHOICES)
    salario = models.DecimalField('Salário', max_digits=10, decimal_places=2, help_text='Salário do funcionário')
    foto = StdImageField(upload_to='media/', variations={'thumb': {'width': 150, 'height': 150, 'crop': True}}, blank=True, null=True, verbose_name="Foto")

    class Meta:
        verbose_name = 'Funcionário'
        verbose_name_plural = 'Funcionários'

    def __str__(self):
        return f"{self.nome} - {self.cargo}"
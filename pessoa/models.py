from django.db import models
from django.db.models.functions import Upper


class Pessoa(models.Model):
    nome = models.CharField('Nome', max_length=50, help_text='Nome completo')
    cpf = models.CharField('CPF', max_length=11, help_text='CPF completo', unique=True)
    fone = models.CharField('Fone', max_length=11, help_text='Número de telefone', unique=True)
    #veiculo = modes.

    class Meta:
        abstract = True

        def __str__(self):
            return self.nome

class Cliente(Pessoa):
    endereco = models.CharField('Endereço', max_length=100, help_text='Endereço Completo')

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'

    def __str__(self):
        return super().nome

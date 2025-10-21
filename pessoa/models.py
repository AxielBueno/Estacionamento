from django.db import models
from django.db.models.functions import Upper
from juridico.models import Juridico


class Pessoa(models.Model):
    nome = models.CharField('Nome', max_length=50, help_text='Nome completo')
    cpf = models.CharField('CPF', max_length=11, help_text='CPF completo', unique=True)
    fone = models.CharField('Fone', max_length=11, help_text='Número de telefone', unique=True)
    email = models.EmailField('Email', max_length=100, unique=True, null=True, blank=True)
    class Meta:
        abstract = True

        def __str__(self):
            return self.nome

class Cliente(Pessoa):
    endereco = models.CharField('Endereço', max_length=100, help_text='Endereço Completo')
    empresa = models.ManyToManyField(Juridico, blank=True, related_name='clientes')

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'

    def __str__(self):
        return super().nome

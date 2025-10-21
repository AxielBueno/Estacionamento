from django.db import models


class Juridico(models.Model):
    nome = models.CharField('Nome', max_length=50, help_text='Nome da Empresa', unique=True)
    cnpj = models.CharField(max_length=18, unique=True, help_text='CNPJ da Empresa')
    email = models.EmailField('Email', max_length=100, help_text='Email da Empresa', unique=True, blank=True, null=True)
    fone = models.CharField('Fone', max_length=20, help_text='Fone da Empresa', unique=True)

    class Meta:
        verbose_name = 'Juridico'
        verbose_name_plural = 'Juridicos'

    def __str__(self):
        return f"{self.nome} - {self.cnpj}"

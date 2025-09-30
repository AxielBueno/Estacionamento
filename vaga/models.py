from django.db import models

class Vaga(models.Model):
    ANDAR_CHOICES = [
        ('A', '1º Andar'),
        ('B', '2º Andar'),
        ('C', '3º Andar'),
    ]

    numero = models.CharField('Número', max_length=10, help_text='Número da vaga', unique=True)
    tamanho = models.CharField('Tamanho', max_length=20, help_text='Tamanho da vaga (ex: Pequena, Média, Grande)')
    andar = models.CharField('Andar', max_length=1, choices=ANDAR_CHOICES, help_text='Andar da vaga')

    class Meta:
        verbose_name = 'Vaga'
        verbose_name_plural = 'Vagas'

    def __str__(self):
        return f'Vaga {self.numero} - {self.get_andar_display()}'
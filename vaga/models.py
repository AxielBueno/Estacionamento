from django.db import models

class Vaga(models.Model):
    ANDAR_CHOICES = [
        ('A', '1º Andar'),
        ('B', '2º Andar'),
        ('C', '3º Andar'),
    ]

    TAMANHO_CHOICES = [
        ('Pequeno', 'Pequeno'),
        ('Médio', 'Medio'),
        ('Grande', 'Grande'),
    ]

    STATUS_CHOICES = [
        ('Livre', 'Livre'),
        ('Ocupada', 'Ocupada'),
    ]

    numero = models.CharField('Número', max_length=10, help_text='Número da vaga')
    tamanho = models.CharField('Tamanho', max_length=20, choices=TAMANHO_CHOICES, help_text='Tamanho da vaga (ex: Pequena, Média, Grande)')
    andar = models.CharField('Andar', max_length=1, choices=ANDAR_CHOICES, help_text='Andar da vaga')
    status = models.CharField('Status', max_length=10, choices=STATUS_CHOICES, default='Livre', help_text='Status atual da vaga')


    class Meta:
        verbose_name = 'Vaga'
        verbose_name_plural = 'Vagas'
        constraints = [
            models.UniqueConstraint(fields=['numero', 'andar'], name='unique_numero_andar')
        ]

    def __str__(self):
        return f'Vaga {self.numero} - {self.andar}'
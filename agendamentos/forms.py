from django import forms
from .models import Agendamento
from django.utils import timezone
from django.core.exceptions import ValidationError


class AgendamentoModelForm(forms.ModelForm):
    class Meta:
        model = Agendamento
        fields = ['placa', 'dono', 'funcionario', 'entrada', 'saida_prevista',]

        widgets = {
            'entrada': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'saida_prevista': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'saida': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

        error_messages = {
            'placa': {
                'required': 'Selecione a placa do veículo.',
            },
            'dono': {
                'required': 'Selecione o dono do veículo.',
            },
            'entrada': {
                'required': 'Informe a data e hora de entrada.',
            },
            'saida_prevista': {
                'required': 'Informe a data e hora prevista de saída.',
            },
        }

    def clean(self):
        cleaned_data = super().clean()
        entrada = cleaned_data.get('entrada')
        saida_prevista = cleaned_data.get('saida_prevista')

        if entrada and saida_prevista and saida_prevista < entrada:
            self.add_error('saida_prevista', 'A saída prevista não pode ser menor que a entrada.')

        return cleaned_data

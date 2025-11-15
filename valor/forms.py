from django import forms
from .models import ValorHora

class ValorHoraModelForm(forms.ModelForm):
    class Meta:
        model = ValorHora
        fields = ['valor_vigente', 'data_alteracao']

        error_messages = {
            'valor_vigente': {
                'required': 'O valor vigente é um campo obrigatório',
            },
            'data_alteracao': {
                'required': 'A data e hora da alteração é um campo obrigatório',
            }
        }

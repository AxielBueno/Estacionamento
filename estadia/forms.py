from django import forms
from .models import Estadia


class EstadiaModelForm(forms.ModelForm):
    class Meta:
        model = Estadia
        fields = ['entrada', 'saida', 'vaga', 'veiculo']

        error_messages = {
            'entrada': {
                'required': 'A data e hora de entrada são obrigatórias'
            },
            'saida': {
                'required': 'A data e hora de saída são obrigatórias'
            },
            'vaga': {
                'required': 'A vaga já está ocupada'
            },
            'veiculo': {
                'required': 'Veiculo já se encontra em uma vaga'
            },
        }
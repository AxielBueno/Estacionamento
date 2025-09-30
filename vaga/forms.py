from django import forms
from .models import Vaga

class VagaModelForm(forms.ModelForm):
    class Meta:
        model = Vaga
        fields = ['numero', 'tamanho', 'andar']

        error_messages = {
            'numero': {
                'required': 'O número da vaga é obrigatório',
                'unique': 'Número da vaga já cadastrado'
            },
            'tamanho': {
                'required': 'O tamanho da vaga é obrigatório'
            },
            'andar': {
                'required': 'O andar da vaga é obrigatório'
            }
        }
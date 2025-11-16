from django import forms
from .models import Vaga

class VagaModelForm(forms.ModelForm):
    class Meta:
        model = Vaga
        fields = ['numero', 'andar']

        error_messages = {
            'numero': {
                'required': 'O número da vaga é obrigatório',
                'unique': 'Número da vaga já cadastrado'
            },
            'andar': {
                'required': 'O andar da vaga é obrigatório'
            }
        }
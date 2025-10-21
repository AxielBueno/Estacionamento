from django import forms
from .models import Juridico

class JuridicoModelForm(forms.ModelForm):
    class Meta:
        model = Juridico
        fields = ['nome', 'fone', 'email', 'cnpj']

        error_messages = {
            'nome': {'required': 'O nome da empresa é um campo obrigatório'},
            'fone': {'required': 'O número de telefone é um campo obrigatório'},
            'email': {'required': 'Email é um campo obrigatório'},
            'cnpj': {
                'required': 'O CNPJ é um campo obrigatório',
                'unique': 'CNPJ já cadastrado'
            }
        }
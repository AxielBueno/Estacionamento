from django import forms
from .models import Cliente

class ClienteModelForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nome', 'endereco', 'fone', 'cpf']

        error_messages = {
            'nome': {'required': 'O nome do cliente é um campo obrigatório'},
            'endereco': {'required': 'O endereço do cliente é um campo obrigatório'},
            'fone': {'required': 'O número de telefone é um campo obrigatório'},
            'cpf': {
                'required': 'O CPF é um campo obrigatório',
                'unique': 'CPF já cadastrado'
            }
        }
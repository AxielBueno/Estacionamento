from django import forms
from .models import Funcionario

class FuncionarioModelForm(forms.ModelForm):
    class Meta:
        model = Funcionario
        fields = ['nome', 'cpf', 'fone', 'cargo', 'salario', 'foto']

        error_messages = {
            'nome': {'required': 'O nome do funcionário é obrigatório'},
            'cpf': {
                'required': 'O CPF é obrigatório',
                'unique': 'CPF já cadastrado'
            },
            'fone': {'required': 'O número de telefone é obrigatório'},
            'cargo': {'required': 'O cargo é obrigatório'},
            'salario': {'required': 'O salário é obrigatório'},
        }
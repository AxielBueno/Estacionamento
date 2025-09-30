from django import forms
from .models import Veiculo

class VeiculoModelForm(forms.ModelForm):
    class Meta:
        model = Veiculo
        fields = ['placa', 'tipo', 'dono']

        error_messages = {
            'placa': {
                'required': 'A placa do veículo é obrigatória',
                'unique': 'Esta placa já está cadastrada'
            },
            'tipo': {
                'required': 'O tipo do veículo é obrigatório'
            },
            'dono': {
                'required': 'O dono do veículo é obrigatório'
            }
        }
from django import forms
from .models import Pagamento

class PagamentoModelForm(forms.ModelForm):
    class Meta:
        model = Pagamento
        fields = [
            'estadia',
            'dono',
            'placa',
            'metodo',
            'multa_aplicada',
        ]

        error_messages = {
            'estadia': {'required': 'A estadia é um campo obrigatório'},
            'dono': {'required': 'O dono do veículo é um campo obrigatório'},
            'placa': {'required': 'A placa do veículo é um campo obrigatório'},
            'metodo': {'required': 'O método de pagamento é um campo obrigatório'},
        }

    def clean(self):
        cleaned_data = super().clean()
        estadia = cleaned_data.get('estadia')

        if estadia and not estadia.saida:
            self.add_error('estadia', 'A estadia precisa ter data de saída para calcular o pagamento.')

        return cleaned_data

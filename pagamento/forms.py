from django import forms
from .models import Pagamento
from estadia.models import Estadia

class PagamentoModelForm(forms.ModelForm):
    class Meta:
        model = Pagamento
        fields = ['estadia', 'metodo', 'multa_aplicada', 'multa']
        widgets = {
            'estadia': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Aqui não deixo aparecer estadias que ainda não acabaram
        self.fields['estadia'].queryset = Estadia.objects.filter(status='Finalizada')

        # Campos que devem ficar travados
        self.fields['multa'].disabled = True

    def clean(self):
        cleaned_data = super().clean()
        estadia = cleaned_data.get('estadia')

        if estadia and not estadia.saida:
            self.add_error('estadia', 'A estadia precisa ter data de saída para calcular o pagamento.')

        return cleaned_data

    # Aqui eu pego o dono e o veículo
    def save(self, commit=True):
        pagamento = super().save(commit=False)

        if pagamento.estadia:
            pagamento.dono = pagamento.estadia.veiculo.dono
            pagamento.placa = pagamento.estadia.veiculo.placa

        if commit:
            pagamento.save()

        return pagamento

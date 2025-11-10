from django import forms
from .models import Estadia
from vaga.models import Vaga
from veiculo.models import Veiculo
from django.utils import timezone

class EstadiaModelForm(forms.ModelForm):
    class Meta:
        model = Estadia
        fields = ['entrada', 'vaga', 'veiculo']

        error_messages = {
            'entrada': {
                'required': 'A data e hora de entrada são obrigatórias'
            },
            'vaga': {
                'required': 'A vaga já está ocupada'
            },
            'veiculo': {
                'required': 'Veículo já se encontra em uma vaga'
            },
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # isso bloqueia o campo da entrada, basicamente deixando ele ali só pra mostrar a entrada
        self.fields['entrada'].disabled = True
        if not self.instance.pk:
            self.fields['entrada'].initial = timezone.now()

        # Aqui mostra as vagas libres, aribaaa!!!
        self.fields['vaga'].queryset = Vaga.objects.filter(status='Livre')

        # Já aqui é usado para mostrar apenas veiculos livres q não estão numa estadia
        veiculos_ocupados = Estadia.objects.filter(saida__isnull=True).values_list('veiculo_id', flat=True)
        self.fields['veiculo'].queryset = Veiculo.objects.exclude(id__in=veiculos_ocupados)

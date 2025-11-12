from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.core.paginator import Paginator
from django.urls import reverse_lazy
from .models import Veiculo
from .forms import VeiculoModelForm
from django.db.models import Q


class VeiculoView(ListView):
    model = Veiculo
    template_name = 'veiculos.html'

    def get_queryset(self):
        buscar = self.request.GET.get('buscar')
        qs = super(VeiculoView, self).get_queryset()

        if buscar:
            qs = qs.filter(
                Q(placa__icontains=buscar) |
                Q(dono__nome__icontains=buscar)
            )

        if qs.count() > 0:
            paginator = Paginator(qs, 10)
            listagem = paginator.get_page(self.request.GET.get('page'))
            return listagem
        else:
            return messages.info(self.request, 'Não existem veículos cadastrados.')

class VeiculoAddView(SuccessMessageMixin, CreateView):
    model = Veiculo
    form_class = VeiculoModelForm
    template_name = 'veiculo_forms.html'
    success_url = reverse_lazy('veiculo')
    success_message = 'Veículo cadastrado com sucesso.'

class VeiculoUpdateView(SuccessMessageMixin, UpdateView):
    model = Veiculo
    form_class = VeiculoModelForm
    template_name = 'veiculo_forms.html'
    success_url = reverse_lazy('veiculo')
    success_message = 'Veículo atualizado com sucesso.'

class VeiculoDeleteView(SuccessMessageMixin, DeleteView):
    model = Veiculo
    template_name = 'veiculo_apagar.html'
    success_url = reverse_lazy('veiculo')
from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.core.paginator import Paginator
from django.urls import reverse_lazy
from .models import Vaga
from .forms import VagaModelForm

class VagaView(ListView):
    model = Vaga
    template_name = 'vaga.html'

    def get_queryset(self):
        buscar = self.request.GET.get('buscar')
        qs = super(VagaView, self).get_queryset()

        if buscar:
            qs = qs.filter(numero__icontains=buscar)

        if qs.count() > 0:
            paginator = Paginator(qs, 10)
            listagem = paginator.get_page(self.request.GET.get('page'))
            return listagem
        else:
            return messages.info(self.request, 'Não existem vagas cadastradas.')

class VagaAddView(SuccessMessageMixin, CreateView):
    model = Vaga
    form_class = VagaModelForm
    template_name = 'vaga_form.html'
    success_url = reverse_lazy('vagas')
    success_message = 'Vaga cadastrada com sucesso.'

class VagaUpdateView(SuccessMessageMixin, UpdateView):
    model = Vaga
    form_class = VagaModelForm
    template_name = 'vaga_form.html'
    success_url = reverse_lazy('vagas')
    success_message = 'Vaga atualizada com sucesso.'

class VagaDeleteView(SuccessMessageMixin, DeleteView):
    model = Vaga
    template_name = 'vaga_apagar.html'
    success_url = reverse_lazy('vagas')
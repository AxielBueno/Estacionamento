from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.core.paginator import Paginator
from django.urls import reverse_lazy
from .models import Juridico
from .forms import JuridicoModelForm

class JuridicoView(ListView):
    model = Juridico
    template_name = 'juridico.html'

    def get_queryset(self):
        buscar = self.request.GET.get('buscar')
        qs = super(JuridicoView, self).get_queryset()

        if buscar:
            qs = qs.filter(nome__icontains=buscar)

        if qs.count() > 0:
            paginator = Paginator(qs, 10)
            listagem = paginator.get_page(self.request.GET.get('page'))
            return listagem
        else:
            messages.info(self.request, 'Não existem empresas jurídicas cadastradas.')
            return qs.none()

class JuridicoAddView(SuccessMessageMixin, CreateView):
    model = Juridico
    form_class = JuridicoModelForm
    template_name = 'juridico_form.html'
    success_url = reverse_lazy('juridicos')
    success_message = 'Empresa jurídica cadastrada com sucesso.'

class JuridicoUpdateView(SuccessMessageMixin, UpdateView):
    model = Juridico
    form_class = JuridicoModelForm
    template_name = 'juridico_form.html'
    success_url = reverse_lazy('juridicos')
    success_message = 'Empresa jurídica atualizada com sucesso.'

class JuridicoDeleteView(SuccessMessageMixin, DeleteView):
    model = Juridico
    template_name = 'juridico_apagar.html'
    success_url = reverse_lazy('juridicos')

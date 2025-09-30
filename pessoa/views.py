from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.core.paginator import Paginator
from django.urls import reverse_lazy
from .models import Cliente
from .forms import ClienteModelForm

class ClienteView(ListView):
    model = Cliente
    template_name ='pessoas.html'

    def get_queryset(self):
        buscar = self.request.GET.get('buscar')
        qs = super(ClienteView, self).get_queryset()

        if buscar:
            qs = qs.filter(nome__icontains=buscar)

        if qs.count() > 0:
            paginator = Paginator(qs, 10)
            listagem = paginator.get_page(self.request.GET.get('page'))
            return listagem
        else:
            return messages.info(self.request, 'Não existem clientes cadastrados.')

class ClienteAddView(SuccessMessageMixin, CreateView):
    model = Cliente
    form_class = ClienteModelForm
    template_name = 'pessoa_form.html'
    success_url = reverse_lazy('clientes')
    success_message = 'Cliente cadastrado com sucesso.'

class ClienteUpdateView(SuccessMessageMixin, UpdateView):
    model = Cliente
    form_class = ClienteModelForm
    template_name = 'pessoa_form.html'
    success_url = reverse_lazy('clientes')
    success_message = 'Cliente atualizado com sucesso.'

class ClienteDeleteView(SuccessMessageMixin, DeleteView):
    model = Cliente
    template_name ='pessoa_apagar.html'
    success_url = reverse_lazy('clientes')
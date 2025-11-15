from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib import messages
from django.core.paginator import Paginator
from django.urls import reverse_lazy
from .models import ValorHora
from .forms import ValorHoraModelForm


class ValorHoraView(PermissionRequiredMixin, ListView):
    permission_required = 'valor.view_valorhora'
    permission_denied_message = 'Visualizar valores'
    model = ValorHora
    template_name = 'valorhora.html'

    def get_queryset(self):
        buscar = self.request.GET.get('buscar')
        qs = super(ValorHoraView, self).get_queryset()

        if buscar:
            qs = qs.filter(valor__icontains=buscar)

        if qs.count() > 0:
            paginator = Paginator(qs, 10)
            listagem = paginator.get_page(self.request.GET.get('page'))
            return listagem
        else:
            return messages.info(self.request, 'Não existem valores cadastrados.')


class ValorHoraAddView(PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    permission_required = 'valor.add_valorhora'
    permission_denied_message = 'Cadastrar valor'
    model = ValorHora
    form_class = ValorHoraModelForm
    template_name = 'valorhora_forms.html'
    success_url = reverse_lazy('valorhora')
    success_message = 'Valor cadastrado com sucesso.'


class ValorHoraUpdateView(PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    permission_required = 'valor.update_valorhora'
    permission_denied_message = 'Editar valor'
    model = ValorHora
    form_class = ValorHoraModelForm
    template_name = 'valorhora_forms.html'
    success_url = reverse_lazy('valorhora')
    success_message = 'Valor atualizado com sucesso.'


class ValorHoraDeleteView(PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    permission_required = 'valor.delete_valorhora'
    permission_denied_message = 'Excluir valor'
    model = ValorHora
    template_name = 'valorhora_apagar.html'
    success_url = reverse_lazy('valorhora')

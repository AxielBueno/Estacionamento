from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.core.paginator import Paginator
from django.urls import reverse_lazy
from .models import Pagamento
from .forms import PagamentoModelForm


class PagamentoView(ListView):
    model = Pagamento
    template_name = 'pagamento.html'

    def get_queryset(self):
        buscar = self.request.GET.get('buscar')
        qs = super(PagamentoView, self).get_queryset().select_related('dono', 'estadia')

        if buscar:
            qs = qs.filter(dono__nome__icontains=buscar)

        if qs.exists():
            paginator = Paginator(qs, 10)
            listagem = paginator.get_page(self.request.GET.get('page'))
            return listagem
        else:
            messages.info(self.request, 'Não existem pagamentos cadastrados.')
            return qs.none()


class PagamentoAddView(SuccessMessageMixin, CreateView):
    model = Pagamento
    form_class = PagamentoModelForm
    template_name = 'pagamento_forms.html'
    success_url = reverse_lazy('pagamentos')
    success_message = 'Pagamento cadastrado com sucesso.'


class PagamentoUpdateView(SuccessMessageMixin, UpdateView):
    model = Pagamento
    form_class = PagamentoModelForm
    template_name = 'pagamento_forms.html'
    success_url = reverse_lazy('pagamentos')
    success_message = 'Pagamento atualizado com sucesso.'


class PagamentoDeleteView(SuccessMessageMixin, DeleteView):
    model = Pagamento
    template_name = 'pagamento_apagar.html'
    success_url = reverse_lazy('pagamentos')

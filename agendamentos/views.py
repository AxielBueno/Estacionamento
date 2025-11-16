from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.core.paginator import Paginator
from django.urls import reverse_lazy
from django.utils import timezone
from django.db.models import Q
from .forms import *
from decimal import Decimal
from .models import Agendamento


# ============================
#   TELA PAGAR
# ============================
def agendamento_pagar(request, pk):
    agendamento = get_object_or_404(Agendamento, pk=pk)

    valor_base = agendamento.valor_base
    desconto_juridico = agendamento.desconto_juridico

    desconto_pix_debito_calc = (valor_base * Decimal('0.10')).quantize(Decimal('0.01'))
    aplicar_pix_debito = False

    metodo_get = request.GET.get('metodo')
    if metodo_get and metodo_get.lower() in ['pix', 'debito']:
        aplicar_pix_debito = True

    desconto_total = desconto_juridico + (desconto_pix_debito_calc if aplicar_pix_debito else Decimal('0.00'))
    valor_final = (valor_base - desconto_total).quantize(Decimal('0.01'))

    context = {
        'agendamento': agendamento,
        'valor_base': valor_base,
        'desconto_juridico': desconto_juridico,
        'desconto_pix_debito_calc': desconto_pix_debito_calc,
        'aplicar_pix_debito': aplicar_pix_debito,
        'desconto_total': desconto_total,
        'valor_final': valor_final,
    }

    return render(request, 'agendamento_pagar.html', context)


# ============================
#   CONCLUI PAGAMENTO (SEM EMAIL)
# ============================
def concluir_agendamento(request, pk):
    agendamento = get_object_or_404(Agendamento, pk=pk)

    # Pega os dados da URL
    modalidade = request.GET.get('modalidade')
    desconto_str = request.GET.get('desconto', '0').replace(',', '.')

    try:
        desconto = Decimal(desconto_str)
    except:
        desconto = Decimal('0')

    # Atualiza dados do pagamento
    agendamento.metodo_pagamento = modalidade
    agendamento.valor_desconto = desconto
    agendamento.status = 'finalizado'
    agendamento.saida = timezone.now()
    agendamento.pago = True
    agendamento.save()

    messages.success(request, f'O pagamento do agendamento #{agendamento.id} foi concluído com sucesso.')

    # Redireciona para a lista
    return redirect('agendamentos')

# ============================
#   FINALIZAR (SEM PAGAMENTO)
# ============================
def finalizar_agendamento(request, pk):
    agendamento = get_object_or_404(Agendamento, pk=pk)
    if agendamento.status != 'finalizado':
        agendamento.status = 'finalizado'
        if not agendamento.saida:
            agendamento.saida = timezone.now()
        agendamento.save()
        messages.success(request, 'Agendamento finalizado com sucesso.')
    else:
        messages.info(request, 'Agendamento já está finalizado.')
    return redirect('agendamentos')


# ============================
#   LISTAGEM
# ============================
class AgendamentoView(LoginRequiredMixin, ListView):
    model = Agendamento
    template_name = 'agendamento.html'

    def get_queryset(self):
        buscar = self.request.GET.get('buscar')
        qs = super().get_queryset()

        if buscar:
            qs = qs.filter(
                Q(placa__placa__icontains=buscar) |
                Q(dono__nome__icontains=buscar)
            )

        if qs.exists():
            paginator = Paginator(qs, 10)
            return paginator.get_page(self.request.GET.get('page'))
        else:
            messages.info(self.request, 'Não existem agendamentos cadastrados.')
            return Agendamento.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context


class AgendamentoAddView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Agendamento
    form_class = AgendamentoModelForm
    template_name = 'agendamento_forms.html'
    success_url = reverse_lazy('agendamentos')
    success_message = 'Agendamento cadastrado com sucesso.'


class AgendamentoUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Agendamento
    form_class = AgendamentoModelForm
    template_name = 'agendamento_forms.html'
    success_url = reverse_lazy('agendamentos')
    success_message = 'Agendamento atualizado com sucesso.'


class AgendamentoDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Agendamento
    template_name = 'agendamento_apagar.html'
    success_url = reverse_lazy('agendamentos')

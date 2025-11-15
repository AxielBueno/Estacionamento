from django.shortcuts import get_object_or_404, redirect
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
from django.template.loader import render_to_string
from django.core.mail import send_mail
from .models import Agendamento


# Finaliza pagamento e envia email
def concluir_agendamento(request, pk):
    agendamento = get_object_or_404(Agendamento, pk=pk)

    modalidade = request.GET.get('modalidade')
    desconto_str = request.GET.get('desconto', '0').replace(',', '.')
    try:
        desconto = Decimal(str(desconto_str))
    except:
        desconto = Decimal('0')

    # Usa o valor_final do model diretamente
    agendamento.metodo_pagamento = modalidade
    agendamento.valor_desconto = desconto
    # garante que valor_final nunca será recalculado
    agendamento.status = 'finalizado'
    agendamento.saida = timezone.now()
    agendamento.pago = True
    agendamento.save()

    email = [agendamento.dono.email] if getattr(agendamento.dono, 'email', None) else []

    if email:
        dados = {
            'cliente': agendamento.dono.nome,
            'responsavel': getattr(agendamento.placa.dono, 'nome', agendamento.dono.nome)
            if hasattr(agendamento.placa, 'dono') else agendamento.dono.nome,
            'veiculo': getattr(agendamento.placa, 'placa', 'N/A'),
            'entrada': agendamento.entrada.strftime("%d/%m/%Y %H:%M") if agendamento.entrada else 'N/A',
            'saida_prevista': agendamento.saida_prevista.strftime("%d/%m/%Y %H:%M") if agendamento.saida_prevista else 'N/A',
            'saida': agendamento.saida.strftime("%d/%m/%Y %H:%M") if agendamento.saida else 'N/A',
            'pagamento': agendamento.metodo_pagamento.capitalize() if agendamento.metodo_pagamento else 'N/A',
            'desconto': f"R$ {agendamento.valor_desconto:.2f}",
            'valor_final': f"R$ {agendamento.valor_final:.2f}",
        }

        texto_email = render_to_string('emails/agendamento_email.txt', dados)
        html_email = render_to_string('emails/agendamento_email.html', dados)

        send_mail(
            subject='Estacionamento Edens - Pagamento Concluído',
            message=texto_email,
            from_email='axiel.bueno@acad.ufsm.br',
            recipient_list=email,
            html_message=html_email,
            fail_silently=True,
        )

        messages.success(request, f'O pagamento do agendamento #{agendamento.id} foi concluído e o e-mail enviado!')
    else:
        messages.success(request,
                         f'O pagamento do agendamento #{agendamento.id} foi concluído com sucesso (sem e-mail enviado).')

    return redirect('agendamentos')


# Finaliza agendamento (marca como finalizado)
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


# Lista de agendamentos
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

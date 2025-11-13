from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.core.paginator import Paginator
from django.urls import reverse_lazy
from django.contrib.auth.mixins import PermissionRequiredMixin
from .models import Pagamento
from django.core.mail import send_mail
from django.template.loader import render_to_string
from .forms import PagamentoModelForm


def concluir_pagamento(request, pk):
    pagamento = get_object_or_404(Pagamento, pk=pk)
    pagamento.status = 'C'
    pagamento.save()

    email = [pagamento.dono.email] if pagamento.dono.email else []

    if email:
        dados = {
            'cliente': pagamento.dono.nome,
            'responsavel': pagamento.estadia.vaga.funcionario.nome if hasattr(pagamento.estadia.vaga, 'funcionario') and pagamento.estadia.vaga.funcionario else pagamento.dono.nome,
            'veiculo': pagamento.estadia.veiculo.placa if pagamento.estadia.veiculo else 'N/A',
            'entrada': pagamento.estadia.entrada.strftime("%d/%m/%Y %H:%M") if pagamento.estadia.entrada else 'N/A',
            'saida': pagamento.estadia.saida.strftime("%d/%m/%Y %H:%M") if pagamento.estadia.saida else 'N/A',
            'permanencia': pagamento.estadia.permanencia,
            'multa': f"R$ {pagamento.valor_multa}",
            'pagamento': pagamento.get_metodo_display(),
            'desconto': f"R$ {pagamento.valor_desconto}",
            'valor_final': f"R$ {pagamento.valorFinal}",
        }

        texto_email = render_to_string('emails/texto_email.txt', dados)
        html_email = render_to_string('emails/texto_email.html', dados)

        send_mail(
            subject='Estacionamento Edens - Pagamento Concluído',
            message=texto_email,
            from_email='axiel.bueno@acad.ufsm.br.com',
            recipient_list=email,
            html_message=html_email,
            fail_silently=False,
        )

        messages.success(request,
                         f'O pagamento #{pagamento.idPagamento} foi concluído e o e-mail foi enviado com sucesso!')
    else:
        messages.warning(request,
                         f'O pagamento #{pagamento.idPagamento} foi concluído, mas o cliente não possui e-mail cadastrado.')

    return redirect('pagamentos')


class PagamentoView(PermissionRequiredMixin, ListView):
    model = Pagamento
    template_name = 'pagamento.html'
    permission_required = 'pagamento.view_pagamento'
    permission_denied_message = 'Você não tem permissão para visualizar pagamentos.'

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


class PagamentoAddView(PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = Pagamento
    form_class = PagamentoModelForm
    template_name = 'pagamento_forms.html'
    success_url = reverse_lazy('pagamentos')
    success_message = 'Pagamento cadastrado com sucesso.'
    permission_required = 'pagamento.add_pagamento'
    permission_denied_message = 'Você não tem permissão para cadastrar pagamentos.'


class PagamentoUpdateView(PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Pagamento
    form_class = PagamentoModelForm
    template_name = 'pagamento_forms.html'
    success_url = reverse_lazy('pagamentos')
    success_message = 'Pagamento atualizado com sucesso.'
    permission_required = 'pagamento.change_pagamento'
    permission_denied_message = 'Você não tem permissão para editar pagamentos.'


class PagamentoDeleteView(PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Pagamento
    template_name = 'pagamento_apagar.html'
    success_url = reverse_lazy('pagamentos')
    permission_required = 'pagamento.delete_pagamento'
    permission_denied_message = 'Você não tem permissão para excluir pagamentos.'

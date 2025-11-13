from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib import messages
from django.core.paginator import Paginator
from django.urls import reverse_lazy
from .forms import EstadiaModelForm
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone
from .models import Estadia
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.shortcuts import redirect
from django.db.models import Q


# DEF só pra pegar o tempo atual e registrar
def registrar_saida(request, pk):
    estadia = get_object_or_404(Estadia, pk=pk)
    estadia.saida = timezone.now()
    estadia.save()
    return redirect('estadias')


class EstadiaView(PermissionRequiredMixin, ListView):
    permission_required = 'estadia.view_estadia'
    permission_denied_message = 'Visualizar estadia'
    model = Estadia
    template_name = 'estadia.html'

    def get_queryset(self):
        buscar = self.request.GET.get('buscar')
        qs = super().get_queryset()

        if buscar:
            qs = qs.filter(
                Q(veiculo__placa__icontains=buscar)
            )

        if qs.exists():
            paginator = Paginator(qs, 10)
            listagem = paginator.get_page(self.request.GET.get('page'))
            return listagem
        else:
            messages.info(self.request, 'Não existem estadias cadastradas.')
            return Estadia.objects.none()


class EstadiaAddView(PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    permission_required = 'estadia.add_estadia'
    permission_denied_message = 'Cadastrar estadia'
    model = Estadia
    form_class = EstadiaModelForm
    template_name = 'estadia_forms.html'
    success_url = reverse_lazy('estadias')
    success_message = 'Estadia cadastrada com sucesso.'

    def form_valid(self, form):
        response = super().form_valid(form)

        vaga = self.object.vaga
        vaga.status = 'Ocupada'
        vaga.save()

        return response


class EstadiaUpdateView(PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    permission_required = 'estadia.update_estadia'
    permission_denied_message = 'Editar estadia'
    model = Estadia
    form_class = EstadiaModelForm
    template_name = 'estadia_forms.html'
    success_url = reverse_lazy('estadias')
    success_message = 'Estadia atualizada com sucesso.'


class EstadiaDeleteView(PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    permission_required = 'estadia.delete_estadia'
    permission_denied_message = 'Excluir estadia'
    model = Estadia
    template_name = 'estadia_apagar.html'
    success_url = reverse_lazy('estadias')


def finalizar_estadia(request, pk):
    estadia = get_object_or_404(Estadia, pk=pk)

    if estadia.status == 'Finalizada':
        messages.info(request, "Esta estadia já foi finalizada.")
        return redirect('estadias')

    estadia.saida = timezone.now()
    estadia.status = 'Finalizada'
    estadia.save()

    vaga = estadia.vaga
    vaga.status = 'Livre'
    vaga.save()

    if estadia.vaga:
        estadia.vaga.status = 'Livre'
        estadia.vaga.save()

    messages.success(request, f'Estadia {estadia.idEstadia} finalizada com sucesso!')
    return redirect('estadias')



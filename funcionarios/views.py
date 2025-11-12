from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Funcionario
from .forms import FuncionarioModelForm
from django.core.paginator import Paginator
from django.contrib import messages
from django.db.models import Q

class FuncionarioView(ListView):
    model = Funcionario
    template_name = 'funcionarios.html'

    def get_queryset(self):
        buscar = self.request.GET.get('buscar')
        qs = super(FuncionarioView, self).get_queryset()

        if buscar:
            qs = qs.filter(
                Q(nome__icontains=buscar) |
                Q(cpf__icontains=buscar)
            )

        if qs.count() > 0:
            paginator = Paginator(qs, 10)
            listagem = paginator.get_page(self.request.GET.get('page'))
            return listagem
        else:
            return messages.info(self.request, 'Não existem funcionarios cadastrados.')



class FuncionarioAddView(CreateView):
    model = Funcionario
    form_class = FuncionarioModelForm
    template_name = 'funcionario_forms.html'
    success_url = reverse_lazy('funcionarios')


class FuncionarioUpdateView(UpdateView):
    model = Funcionario
    form_class = FuncionarioModelForm
    template_name = 'funcionario_forms.html'
    success_url = reverse_lazy('funcionarios')


class FuncionarioDeleteView(DeleteView):
    model = Funcionario
    template_name = 'funcionario_apagar.html'
    success_url = reverse_lazy('funcionarios')

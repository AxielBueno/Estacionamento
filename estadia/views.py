from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.core.paginator import Paginator
from django.urls import reverse_lazy
from .forms import EstadiaModelForm
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone
from .models import Estadia

def registrar_saida(request, pk):
    estadia = get_object_or_404(Estadia, pk=pk)
    estadia.saida = timezone.now()
    estadia.save()
    return redirect('estadias')

class EstadiaView(ListView):
    model = Estadia
    template_name = 'estadia.html'

    def get_queryset(self):
        buscar = self.request.GET.get('buscar')
        qs = super().get_queryset()

        if buscar:
            qs = qs.filter(idEstadia__icontains=buscar) | qs.filter(entrada__icontains=buscar)

        if qs.exists():
            paginator = Paginator(qs, 10)
            listagem = paginator.get_page(self.request.GET.get('page'))
            return listagem
        else:
            messages.info(self.request, 'Não existem estadias cadastradas.')
            return Estadia.objects.none()

class EstadiaAddView(SuccessMessageMixin, CreateView):
    model = Estadia
    form_class = EstadiaModelForm
    template_name = 'estadia_forms.html'
    success_url = reverse_lazy('estadias')
    success_message = 'Estadia cadastrada com sucesso.'

class EstadiaUpdateView(SuccessMessageMixin, UpdateView):
    model = Estadia
    form_class = EstadiaModelForm
    template_name = 'estadia_forms.html'
    success_url = reverse_lazy('estadias')
    success_message = 'Estadia atualizada com sucesso.'

class EstadiaDeleteView(SuccessMessageMixin, DeleteView):
    model = Estadia
    template_name = 'estadia_apagar.html'
    success_url = reverse_lazy('estadias')
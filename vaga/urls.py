from django.urls import path
from .views import *

urlpatterns = [
    path('vagas/', VagaView.as_view(), name='vagas'),
    path('vaga/adicionar', VagaAddView.as_view(), name='vaga_adicionar'),
    path('<int:pk>/vaga/editar', VagaUpdateView.as_view(), name='vaga_editar'),
    path('<int:pk>/vaga/apagar', VagaDeleteView.as_view(), name='vaga_apagar'),
]
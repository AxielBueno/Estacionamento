from django.urls import path

from .views import *

urlpatterns = [
    path('veiculos/', VeiculoView.as_view(), name='veiculo'),
    path('veiculos/adicionar', VeiculoAddView.as_view(), name='veiculo_adicionar'),
    path('<int:pk>/veiculos/editar', VeiculoUpdateView.as_view(), name='veiculo_editar'),
    path('<int:pk>/veiculos/apagar', VeiculoDeleteView.as_view(), name='veiculo_apagar'),
]
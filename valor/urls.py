from django.urls import path
from .views import *

urlpatterns = [
    path('valor-hora/', ValorHoraView.as_view(), name='valorhora'),
    path('valor-hora/adicionar', ValorHoraAddView.as_view(), name='valorhora_adicionar'),
    path('<int:pk>/valor-hora/editar', ValorHoraUpdateView.as_view(), name='valorhora_editar'),
    path('<int:pk>/valor-hora/apagar', ValorHoraDeleteView.as_view(), name='valorhora_apagar'),
]

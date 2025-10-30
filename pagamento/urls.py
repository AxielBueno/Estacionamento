from django.urls import path
from .views import *

urlpatterns = [
    path('pagamentos/', PagamentoView.as_view(), name='pagamentos'),
    path('pagamento/adicionar', PagamentoAddView.as_view(), name='pagamento_adicionar'),
    path('<int:pk>/pagamento/editar', PagamentoUpdateView.as_view(), name='pagamento_editar'),
    path('<int:pk>/pagamento/apagar', PagamentoDeleteView.as_view(), name='pagamento_apagar'),
    path('<int:pk>/pagamento/concluir', concluir_pagamento, name='pagamento_concluir'),
]

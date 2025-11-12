from django.urls import path
from .views import (AgendamentoView, AgendamentoAddView, AgendamentoUpdateView, AgendamentoDeleteView, finalizar_agendamento, concluir_agendamento, )

urlpatterns = [
    path('agendamentos/', AgendamentoView.as_view(), name='agendamentos'),
    path('agendamentos/novo/', AgendamentoAddView.as_view(), name='agendamentos_adicionar'),
    path('agendamentos/editar/<int:pk>/', AgendamentoUpdateView.as_view(), name='agendamentos_editar'),
    path('agendamentos/apagar/<int:pk>/', AgendamentoDeleteView.as_view(), name='agendamentos_apagar'),
    path('agendamentos/finalizar/<int:pk>/', finalizar_agendamento, name='agendamentos_finalizar'),
    path('<int:pk>/agendamento/concluir', concluir_agendamento, name='pagamento_concluir'),
]

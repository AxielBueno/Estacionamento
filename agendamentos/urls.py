from django.urls import path
from . import views

urlpatterns = [
    path('agendamentos/', views.AgendamentoView.as_view(), name='agendamentos'),
    path('agendamentos/novo/', views.AgendamentoAddView.as_view(), name='agendamentos_add'),
    path('agendamentos/editar/<int:pk>/', views.AgendamentoUpdateView.as_view(), name='agendamentos_edit'),
    path('agendamentos/apagar/<int:pk>/', views.AgendamentoDeleteView.as_view(), name='agendamentos_delete'),
    path('agendamentos/saida/<int:pk>/', views.registrar_saida, name='agendamentos_saida'),
]

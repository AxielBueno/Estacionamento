from django.urls import path
from .views import *

urlpatterns = [
    path('funcionarios/', FuncionarioView.as_view(), name='funcionarios'),
    path('funcionario/adicionar/', FuncionarioAddView.as_view(), name='funcionario_adicionar'),
    path('funcionario/<int:pk>/editar/', FuncionarioUpdateView.as_view(), name='funcionario_editar'),
    path('funcionario/<int:pk>/apagar/', FuncionarioDeleteView.as_view(), name='funcionario_apagar'),
]
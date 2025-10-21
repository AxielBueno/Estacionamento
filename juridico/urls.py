from django.urls import path
from .views import *

urlpatterns = [
    path('juridicos/', JuridicoView.as_view(), name='juridicos'),
    path('juridico/adicionar', JuridicoAddView.as_view(), name='juridico_adicionar'),
    path('<int:pk>/juridico/editar', JuridicoUpdateView.as_view(), name='juridico_editar'),
    path('<int:pk>/juridico/apagar', JuridicoDeleteView.as_view(), name='juridico_apagar'),
]
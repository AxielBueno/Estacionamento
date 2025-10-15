from django.contrib import admin
from django.urls import path, include
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    path('', include('pessoa.urls')),
    path('', include('vaga.urls')),
    path('', include('veiculo.urls')),
    path('', include('estadia.urls')),
    path('', include('funcionarios.urls')),
    path('', include('agendamentos.urls')),
]

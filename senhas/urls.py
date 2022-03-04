from django.urls import path
from . import views
from django.conf.urls import include


app_name='senhas'

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('cad_transporte/', views.cad_transporte, name='cad_transporte'),
    path('cad_acesso_ponto/', views.cad_acesso_ponto, name='cad_acesso_ponto'),
    path('cad_viagem/<str:tipo>', views.viagem_inclui, name='viagem_inclui'),
    path('viagem/<str:id>', views.viagem, name='viagem'),
    path('viagem_altera/<str:id>', views.viagem_altera, name='viagem_altera'),
    #
    path('gera_senha/<str:id>', views.gera_senha, name='gera_senha'),

]
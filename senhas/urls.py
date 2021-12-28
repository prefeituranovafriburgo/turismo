from django.urls import path
from . import views
from django.conf.urls import include


app_name='senhas'

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('cad_transporte/', views.cad_transporte, name='cad_transporte'),
    path('cad_acesso_ponto/', views.cad_acesso_ponto, name='cad_acesso_ponto'),
    path('viagem_inclui/', views.viagem_inclui, name='viagem_inclui'),
    path('viagem/<int:id>', views.viagem, name='viagem'),
    path('viagem_altera/<int:id>', views.viagem_altera, name='viagem_altera'),
    #
    path('gera_senha/<int:id>', views.gera_senha, name='gera_senha'),

]
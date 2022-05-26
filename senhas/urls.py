from django.urls import path
from . import views
from django.conf.urls import include


app_name='senhas'

urlpatterns = [
    path('', views.inicio, name='inicio'),
    
    path('cad_transporte/', views.cad_transporte, name='cad_transporte'),
    path('cad_acesso_ponto/', views.cad_acesso_ponto, name='cad_acesso_ponto'),
    
    path('cad_viagem/c/<str:tipo>', views.viagem_inclui, name='viagem_inclui'),
    
    path('cad_viagem/caledonia', views.cadastrar_viagem_caledonia, name='caledonia'),
    path('cad_viagem/caledonia/editar/<str:id>', views.viagem_altera_caledonia, name='caledonia_editar'),
    path('cad_viagem/caledonia/validarData', views.get_validar_caledonia, name='get_validar_caledonia'),

    path('viagem/<str:id>/22NF', views.viagem, name='viagem'),
    path('viagem/excluir/<str:id>/22NF', views.excluir_viagem, name='excluir_senha'),
    path('viagem/fiscalizar/<str:id>/22NF', views.fiscalizar_viagem, name='fiscalizar_viagem'),
    path('viagem_altera/<str:id>', views.viagem_altera, name='viagem_altera'),
    #
    path('gera_senha_html/<str:id>/22NF', views.gera_senha_to_html, name='gera_senha_html'),
    path('gera_senha_pdf/<str:id>/22NF', views.gera_senha_to_pdf, name='gera_senha'),
]
from django.urls import path
from . import views
from django.conf.urls import include


app_name='senhas'

urlpatterns = [
    path('', views.inicio, name='inicio'),
    
    path('cad_transporte/', views.cad_transporte, name='cad_transporte'),
    path('cad_acesso_ponto/', views.cad_acesso_ponto, name='cad_acesso_ponto'),
    
    path('cadastrar_viagem/compras', views.viagem_compras_cadastrar, name='viagem_compras_cadastrar'),
    path('cadastrar_viagem/turismo', views.viagem_turismo_cadastrar, name='viagem_turismo_cadastrar'),
    path('cadastrar_viagem/caledonia', views.viagem_caledonia_cadastrar, name='caledonia'),

    path('editar_viagem/compras/<id>', views.viagem_compras_editar, name='viagem_compras_editar'),
    path('editar_viagem/turismo/<id>', views.viagem_turismo_editar, name='viagem_turismo_editar'),
    #path('editar_viagem/caledonia<id>', views.cadastrar_viagem_editar, name='caledonia'),

    path('cadastrar_viagem/caledonia/validarData', views.get_validar_caledonia, name='get_validar_caledonia'),

    path('viagem/<str:id>/22NF', views.viagem, name='viagem'),
    path('viagem/excluir/<str:id>/22NF', views.excluir_viagem, name='excluir_senha'),
    path('viagem/fiscalizar/<str:id>/22NF', views.fiscalizar_viagem, name='fiscalizar_viagem'),
    #
    path('gera_senha_html/<str:id>/22NF', views.gera_senha_to_html, name='gera_senha_html'),
    path('gera_senha_pdf/<str:id>/22NF', views.gera_senha_to_pdf, name='gera_senha'),
]
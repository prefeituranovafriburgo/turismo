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

    path('editar_viagem/compras/<senha>', views.viagem_compras_editar, name='viagem_compras_editar'),
    path('editar_viagem/turismo/<senha>', views.viagem_turismo_editar, name='viagem_turismo_editar'),
    path('editar_viagem/caledonia/<senha>', views.viagem_caledonia_editar, name='viagem_caledonia_editar'),

    path('cad_viagem/caledonia/validarData/<str:date>', views.get_validar_caledonia, name='get_validar_caledonia'),

    path('viagem/<str:senha>/23NF', views.viagem, name='viagem'),
    path('viagem/excluir/<str:id>/23NF', views.excluir_viagem, name='excluir_senha'),
    path('viagem/fiscalizar/<str:id>/23NF', views.fiscalizar_viagem, name='fiscalizar_viagem'),
    #
    path('gera_senha_html/<str:id>/23NF', views.gera_senha_to_html, name='gera_senha_html'),
    path('gera_senha_pdf/<str:id>/23NF', views.gera_senha_to_pdf, name='gera_senha'),
]

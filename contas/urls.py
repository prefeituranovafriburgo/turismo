from django.urls import path
from . import views

app_name='contas'

urlpatterns = [
#    path('ajax/load_bairros/', views.load_bairros, name = 'ajax_load_bairros'),
    #
    path('change_password', views.change_password, name='change_password'),
    path("password_reset", views.password_reset_request, name="password_reset"),
    path('sair', views.sair, name='sair'),
    #
    path('cadastrar', views.cadastrar, name='cadastrar'),
    path('cadastro', views.cadastro, name='cadastro'),
    #
    path('ajax/load_cidades/', views.load_cidades, name = 'ajax_load_cidades'),

]
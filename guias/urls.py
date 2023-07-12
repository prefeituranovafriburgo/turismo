from django.urls import path, include
from guias import views

app_name='guias'

urlpatterns = [
    path('', views.index, name='guias'),
    path('cadastrar', views.cadastrar, name='cadastrar'),
    path('mapa-turistico', views.mapa_turistico, name='mapa_turistico'),
]

from django.urls import path, include
from guias import views

app_name='guias'

urlpatterns = [
    path('', views.index, 'guias'),
]

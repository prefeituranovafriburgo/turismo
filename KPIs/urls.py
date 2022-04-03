from django.urls import path
from . import views
from django.conf.urls import include


app_name='KPIs'

urlpatterns = [
    path('', views.index, name='main'),    
]
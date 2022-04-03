from django.urls import path, include
from report import views

app_name='report'

urlpatterns = [
    path('', views.receberProblema, name='receberReport'),
    path('ver', views.verProblemasRelatados, name='verReport'),
]
    


from django.urls import path
from . import views
from django.conf.urls import include


urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('tipos/', views.tipos, name='tipos'),

    path('equipamentos/<int:id>', views.equipamentos, name='equipamentos'),
    path('equipamento/<int:id>', views.equipamento, name='equipamento'),
    path('mostra_qrcode/<int:id>', views.mostra_qrcode, name='mostra_qrcode'),
    path('estatisticas/', views.estatisticas, name='estatisticas'),

    path('qr-code/', include('qr_code.urls', namespace="qr_code")),
]
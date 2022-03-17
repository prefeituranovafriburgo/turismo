"""turismo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from contas.views import login_view
admin.site.site_header = "SECRETARIA MUNICIPAL DE TURISMO E MARKETING"
admin.site.site_title = "PREFEITURA MUNICIPAL DE NOVA FRIBURGO"

urlpatterns = [
    path('', include('senhas.urls')),
    path('contas/', include('contas.urls')),    
    path('guias/', include('guias.urls')),
    path('equipamentos/', include('equipamentos.urls')),
    path('report/', include('report.urls')),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('login/',login_view, name='login'),
    path('social-auth/', include('social_django.urls', namespace='social-auth')),
]

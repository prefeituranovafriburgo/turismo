from django.contrib import admin
from .models import *

# Register your models here.

class EstadoAdmin(admin.ModelAdmin):
    list_display = ['id', 'nome', 'uf']
    search_fields = ['nome']

admin.site.register(Estado, EstadoAdmin)

class CidadeAdmin(admin.ModelAdmin):
    list_display = ['id', 'estado', 'nome']
    list_filter = ['estado']
    search_fields = ['nome']

admin.site.register(Cidade, CidadeAdmin)

class UsuarioAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'cpf', 'celular', 'dt_inclusao']
    list_filter = ['cidade']
    search_fields = ['user__first_name']

admin.site.register(Usuario, UsuarioAdmin)

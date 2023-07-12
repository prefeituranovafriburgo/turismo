from django.contrib import admin
from .models import *

# Register your models here.

class BairroAdmin(admin.ModelAdmin):
    list_display = ['nome', 'dt_inclusao']
    search_fields = ['nome']

admin.site.register(Bairro, BairroAdmin)

class Tipo_EquipamentoAdmin(admin.ModelAdmin):
    list_display = ['descricao', 'dt_inclusao']
    search_fields = ['descricao']

admin.site.register(Tipo_Equipamento, Tipo_EquipamentoAdmin)

class EquipamentoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'tipo_equipamento', 'bairro', 'dt_inclusao']
    list_filter = ['tipo_equipamento']
    search_fields = ['nome', 'tipo_equipamento__nome']

admin.site.register(Equipamento, EquipamentoAdmin)

class VisitanteAdmin(admin.ModelAdmin):
    list_display = ['uuid', 'equipamento', 'dt_inclusao']
    list_filter = ['equipamento']
    search_fields = ['uuid', 'equipamento__nome']

admin.site.register(Visitante, VisitanteAdmin)

from django.contrib import admin
from .models import *

# Register your models here.

class Pontos_TuristicosAdmin(admin.ModelAdmin):
    list_display = ['id', 'nome', 'requer_agendamento', 'ativo', 'dt_inclusao']
    list_filter = ['requer_agendamento']
    search_fields = ['nome']

admin.site.register(Pontos_Turisticos, Pontos_TuristicosAdmin)

class Motivo_ViagemAdmin(admin.ModelAdmin):
    list_display = ['id', 'descricao', 'ativo', 'dt_inclusao']
    search_fields = ['descricao']

admin.site.register(Motivo_Viagem, Motivo_ViagemAdmin)

class Tipo_VeiculoAdmin(admin.ModelAdmin):
    list_display = ['id', 'nome', 'ativo', 'dt_inclusao']
    search_fields = ['nome']

admin.site.register(Tipo_Veiculo, Tipo_VeiculoAdmin)

class ViagemAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'dt_Chegada', 'dt_Saida', 'dt_inclusao']
    search_fields = ['user']

admin.site.register(Viagem, ViagemAdmin)

class Viagem_TurismoAdmin(admin.ModelAdmin):
    list_display = ['id', 'viagem', 'nome_guia', 'celular', 'dt_inclusao']
    search_fields = ['viagem', 'nome_guia']

admin.site.register(Viagem_Turismo, Viagem_TurismoAdmin)

class Links_MenuAdmin(admin.ModelAdmin):
    list_display = ['nome', 'url']
    search_fields = ['nome']

admin.site.register(Links_Menu, Links_MenuAdmin)

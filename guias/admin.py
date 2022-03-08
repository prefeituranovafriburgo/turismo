from telnetlib import SE
from django.contrib import admin
from .models import *

# Register your models here.

class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['id', 'nome']
    search_fields = ['nome']

admin.site.register(Categoria, CategoriaAdmin)

class Segmento_AtuacaoAdmin(admin.ModelAdmin):
    list_display = ['id', 'nome']    
    search_fields = ['nome']

admin.site.register(Segmento_Atuacao, Segmento_AtuacaoAdmin)

class IdiomasAdmin(admin.ModelAdmin):
    list_display = ['id', 'nome']    
    search_fields = ['nome']

admin.site.register(Idiomas, IdiomasAdmin)

class Guias_TurismoAdmin(admin.ModelAdmin):
    list_display=['id', 'nome', 'cadastur', 'validade_cadastur']
    search_fields = ['nome','cadastur','validade_cadastur']
admin.site.register(Guias_Turismo, Guias_TurismoAdmin)
from django.contrib import admin
from .models import ProblemasRelatados
# Register your models here.
class ProblemasReportadosAdmin(admin.ModelAdmin):
    list_display = ['id', 'local', 'descricao', 'ativo', 'dt_inclusao']    

admin.site.register(ProblemasRelatados, ProblemasReportadosAdmin)

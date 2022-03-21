from django.db import models

from contas.models import Usuario
from django.contrib.auth.models import User
# Create your models here.
class ProblemasRelatados(models.Model):

    class Meta:
        verbose_name_plural = "Problemas Relatados"
        verbose_name = "Problema"
        ordering = ['id']

    def __str__(self):
        return 'problema %s - %s' % (self.id,self.user)

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    local = models.CharField(max_length=150)        
    descricao = models.CharField(max_length=350)    
    ativo = models.BooleanField(default=True)    
    dt_inclusao = models.DateTimeField(auto_now_add=True, verbose_name='Data de Inclusão')
from django.db import models
from django.utils import timezone

# Create your models here.
class Categoria(models.Model):
    nome = models.CharField(unique=True, max_length=60)
    def __str__(self):
        return self.nome
class Segmento_Atuacao(models.Model):
    nome = models.CharField(unique=True, max_length=60)
    class Meta:
        verbose_name_plural = "Segmentos de Atuação"
        verbose_name = "Segmento de Atuação"
    def __str__(self):
        return self.nome
class Idiomas(models.Model):
    nome = models.CharField(unique=True, max_length=60)
    class Meta:
        verbose_name_plural = "Idiomas"
        verbose_name = "Idioma"
    
    def __str__(self):
        return self.nome
    

class Guias_Turismo(models.Model):

    def __str__(self):
        return '%s' % (self.nome)

    nome = models.CharField(max_length=60)
    cadastur = models.CharField(unique=True, max_length=16)
    validade_cadastur=models.DateField('Validade Cadastur')
    telefone=models.CharField(max_length=11, default='')
    email=models.CharField(max_length=60, blank=True, null=True)
    categoria=models.ManyToManyField(Categoria)
    segmento_de_atuacao=models.ManyToManyField(Segmento_Atuacao, verbose_name='Segmento de Atuação')
    idiomas=models.ManyToManyField(Idiomas)
    instagram=models.CharField(max_length=60, blank=True, null=True)
    facebook=models.CharField(max_length=60, blank=True, null=True)
    site=models.CharField(max_length=60, blank=True, null=True)    

    class Meta:
        verbose_name_plural = "Guias de Turismo Receptivo"
        verbose_name = "Guia de Turismo Receptivo"
        ordering = ['nome']


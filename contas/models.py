from django.db import models
from django.contrib.auth.models import User
from .functions import validate_CPF, validate_CNPJ

# Create your models here.

class Estado(models.Model):

    class Meta:
        ordering = ['nome']

    def __str__(self):
        return '%s' % (self.nome)

    nome = models.CharField(unique=True, max_length=60)
    uf = models.CharField(unique=True, max_length=2)


class Cidade(models.Model):

    class Meta:
        ordering = ['nome']
        unique_together = ('estado', 'nome')

    def __str__(self):
        return '%s - %s' % (self.estado, self.nome)

    estado = models.ForeignKey(Estado, on_delete=models.PROTECT)
    nome = models.CharField(max_length=60)


class Usuario(models.Model):

    class Meta:
        verbose_name_plural = "Usuários"
        verbose_name = "Usuário"
        ordering = ['user']

    def __str__(self):
        return '%s' % (self.user)

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    cpf = models.CharField(unique=True, max_length=11, validators=[validate_CPF])
    # cadastur = models.CharField(unique=True, max_length=14)
    celular = models.CharField(max_length=11)
    telefone = models.CharField(max_length=10, blank=True, null=True)
    cidade = models.ForeignKey(Cidade, on_delete=models.PROTECT)
    ativo = models.BooleanField(default=True)
    dt_inclusao = models.DateTimeField(auto_now_add=True, verbose_name='Dt. Inclusão')

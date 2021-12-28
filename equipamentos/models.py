from django.db import models

# Create your models here.


class Bairro(models.Model):
    def __str__(self):
        return self.nome

    class Meta:
        ordering = ['nome']

    nome = models.CharField(unique=True, max_length=100)
    dt_inclusao = models.DateTimeField(auto_now_add=True)


class Tipo_Equipamento(models.Model):
    def __str__(self):
        return self.descricao

    class Meta:
        verbose_name_plural = "Tipos de Equipamentos"
        verbose_name = "Tipo de Equipamento"
        ordering = ['descricao']

    descricao = models.CharField(unique=True, max_length=50)
    dt_inclusao = models.DateTimeField(auto_now_add=True)


class Equipamento(models.Model):
    def __str__(self):
        return self.nome

    class Meta:
        ordering = ['nome']

    nome = models.CharField(unique=True, max_length=250)
    tipo_equipamento = models.ForeignKey(Tipo_Equipamento, on_delete=models.PROTECT)
    descricao = models.CharField(max_length=3000)
    foto = models.CharField(max_length=250)
    bairro = models.ForeignKey(Bairro, on_delete=models.PROTECT)
    dt_inclusao = models.DateTimeField(auto_now_add=True)


class Visitante(models.Model):
    def __str__(self):
        return self.uuid

    class Meta:
        ordering = ['dt_inclusao']

    uuid = models.CharField(max_length=32)
    equipamento = models.ForeignKey(Equipamento, on_delete=models.PROTECT)
    dt_inclusao = models.DateTimeField(auto_now_add=True)

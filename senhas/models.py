from django.db import models
from django.contrib.auth.models import User
from contas.models import Cidade, Estado
from senhas.validations import validate_celular, validate_data, validate_nome, validate_passageiros, validate_telefone, validate_CNPJ, validate_Cadastur

# Create your models here.


class Pontos_Turisticos(models.Model):

    class Meta:
        verbose_name_plural = "Pontos Turísticos"
        verbose_name = "Ponto Turístico"
        ordering = ['nome']

    def __str__(self):
        return '%s' % (self.nome)

    nome = models.CharField(unique=True, max_length=60,
                            validators=[validate_nome])
    obs = models.TextField(
        max_length=2000, verbose_name='Observação', blank=True, null=True)
    requer_agendamento = models.BooleanField(default=False)
    ativo = models.BooleanField(default=True)
    dt_inclusao = models.DateTimeField(
        auto_now_add=True, verbose_name='Dt. Inclusão')


class Motivo_Viagem(models.Model):

    class Meta:
        verbose_name_plural = "Motivos das Viagens"
        verbose_name = "Motivo da Viagem"
        ordering = ['descricao']

    def __str__(self):
        return '%s' % (self.descricao)

    descricao = models.CharField(
        unique=True, max_length=60, verbose_name='Descrição')
    ativo = models.BooleanField(default=True)
    dt_inclusao = models.DateTimeField(
        auto_now_add=True, verbose_name='Dt. Inclusão')


class Tipo_Veiculo(models.Model):

    class Meta:
        verbose_name_plural = "Tipos de Veículos"
        verbose_name = "Tipo de Veículo"
        ordering = ['nome']

    def __str__(self):
        return '%s' % (self.nome)

    nome = models.CharField(unique=True, max_length=60)
    ativo = models.BooleanField(default=True)
    dt_inclusao = models.DateTimeField(
        auto_now_add=True, verbose_name='Dt. Inclusão')


class Viagem(models.Model):

    class Meta:
        verbose_name_plural = "Viagens"
        verbose_name = "Viagem"
        ordering = ['user', 'dt_Chegada', 'dt_Saida']

    def __str__(self):
        return '%s - %s - %s' % (self.user, self.dt_Chegada, self.dt_Saida)

    responsavel_viagem = models.CharField(
        max_length=120, default=None, validators=[validate_nome])
    contato_responsavel = models.CharField(max_length=15, default=None)
    senha = models.CharField(max_length=10, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT, null=True)
    dt_Chegada = models.DateField('Data Chegada', validators=[validate_data])
    dt_Saida = models.DateField(
        'Data Saída', null=True, blank=True, validators=[validate_data])
    ficarao_hospedados = models.BooleanField(
        default=False, verbose_name='Ficarão Hospedados?')
    hotel = models.CharField(max_length=120, blank=True, null=True)
    restaurante_reservado = models.BooleanField(
        default=False, verbose_name='Restaurante reservado?')
    restaurante = models.CharField(max_length=120, blank=True, null=True)
    tipo_veiculo = models.ForeignKey(Tipo_Veiculo, on_delete=models.PROTECT)
    quant_passageiros = models.PositiveSmallIntegerField(
        validators=[validate_passageiros])
    empresa_transporte = models.CharField(max_length=120)
    cnpj_empresa_transporte = models.CharField(
        max_length=18, validators=[validate_CNPJ])
    cadastur_empresa_transporte = models.CharField(
        max_length=18, validators=[validate_Cadastur])
    obs = models.TextField(
        max_length=2000, verbose_name='Observação', blank=True, null=True)
    estado_origem = models.ForeignKey(
        Estado, on_delete=models.PROTECT, blank=True, null=True)
    cidade_origem = models.ForeignKey(Cidade, on_delete=models.PROTECT)
    dt_inclusao = models.DateTimeField(
        auto_now_add=True, verbose_name='Dt. Inclusão')
    ativo = models.BooleanField(default=True)


class Viagem_Turismo(models.Model):

    class Meta:
        verbose_name_plural = "Viagens com Turismo"
        verbose_name = "Viagem com Turismo"
        ordering = ['viagem']

    def __str__(self):
        return '%s' % (self.viagem)

    viagem = models.OneToOneField(
        Viagem, on_delete=models.CASCADE, null=True, blank=True)
    outros = models.CharField(default='', max_length=120, blank=True)
    nome_guia = models.CharField(max_length=60, validators=[validate_nome])
    cadastur_guia = models.CharField(
        max_length=18, validators=[validate_Cadastur])
    celular = models.CharField(max_length=15, validators=[validate_celular])
    telefone = models.CharField(
        max_length=14, blank=True, null=True, validators=[validate_telefone])
    pontos_turisticos = models.ManyToManyField(Pontos_Turisticos, blank=True)
    dt_inclusao = models.DateTimeField(
        auto_now_add=True, verbose_name='Dt. Inclusão')
    ativo = models.BooleanField(default=True)

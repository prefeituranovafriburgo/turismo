from django import forms
from django.forms import ModelForm, ValidationError
from .models import *
from .functions import validate_CPF


class CadastrarForm(ModelForm):
    nome = forms.CharField(max_length=60)
    email = forms.CharField(max_length=200)
    cpf = forms.CharField(label='CPF', max_length=14, widget = forms.TextInput(attrs={'onkeydown':"mascara(this,icpf)"}))
    celular = forms.CharField(label= "Celular", max_length=15, widget = forms.TextInput(attrs={'onkeydown':"mascara(this,icelular)", 'onload' : 'mascara(this,icelular)'}))
    telefone = forms.CharField(label = "Telefone",required=False, max_length=14, widget = forms.TextInput(attrs={'onkeydown':"mascara(this,itelefone)", 'onload' : 'mascara(this,itelefone)'}))
    estado = forms.ModelChoiceField(queryset=Estado.objects.all(), widget = forms.Select(attrs={'class': "selEstado"}))
    senha = forms.CharField(label = 'Senha:', widget=forms.PasswordInput)
    senha_confirma = forms.CharField(label = 'Confirmação de senha:', widget=forms.PasswordInput)

    field_order = ['nome', 'cpf', 'cadastur', 'email', 'celular', 'telefone', 'estado', 'cidade']

    class Meta:
        model = Usuario
        exclude = ['user', 'ativo', 'dt_inclusao']
    def clean_cpf(self):
        cpf = validate_CPF(self.cleaned_data["cpf"])
        cpf = cpf.replace('.', '')
        cpf = cpf.replace('-', '')
        return cpf
    def clean_celular(self):
        telefone = self.cleaned_data["celular"]
        telefone = telefone.replace("(",'')
        telefone = telefone.replace(")",'')
        telefone = telefone.replace("-",'')
        telefone = telefone.replace(" ",'')
        if len(telefone) == 10:
            if telefone[2:3] != '2':
                raise ValidationError('Insira um número válido ')
        else:
            if len(telefone) != 11:
                raise ValidationError('Insira um número válido ')
        return telefone
    
    def clean_telefone(self):
        telefone = self.cleaned_data["telefone"]
        telefone = telefone.replace("(",'')
        telefone = telefone.replace(")",'')
        telefone = telefone.replace("-",'')
        telefone = telefone.replace(" ",'')
        if len(telefone) != 10 and len(telefone) != 0:
            raise ValidationError('Insira um número válido')        
        return telefone

    def clean_senha_confirma(self):
        if self.cleaned_data["senha"] != self.cleaned_data["senha_confirma"]:
            raise ValidationError('Senha não confirmada corretamente.')

        return self.cleaned_data["senha_confirma"]


class CadastroForm(ModelForm):
    nome = forms.CharField(max_length=60)
    email = forms.CharField(max_length=200)
    cpf = forms.CharField(label='CPF', max_length=14, widget = forms.TextInput(attrs={'onkeydown':"mascara(this,icpf)"}))
    celular = forms.CharField(label= "Celular", max_length=15, widget = forms.TextInput(attrs={'onkeydown':"mascara(this,icelular)", 'onload' : 'mascara(this,icelular)'}))
    telefone = forms.CharField(label = "Telefone",required=False, max_length=14, widget = forms.TextInput(attrs={'onkeydown':"mascara(this,itelefone)", 'onload' : 'mascara(this,itelefone)'}))
    estado = forms.ModelChoiceField(queryset=Estado.objects.all(), widget = forms.Select(attrs={'class': "selEstado"}))

    field_order = ['nome', 'cpf', 'cadastur', 'email', 'celular', 'telefone', 'estado', 'cidade']

    class Meta:
        model = Usuario
        exclude = ['user', 'ativo', 'dt_inclusao', 'senha']
    def clean_cpf(self):
        cpf = validate_CPF(self.cleaned_data["cpf"])
        cpf = cpf.replace('.', '')
        cpf = cpf.replace('-', '')
        return cpf
    def clean_celular(self):
        telefone = self.cleaned_data["celular"]
        telefone = telefone.replace("(",'')
        telefone = telefone.replace(")",'')
        telefone = telefone.replace("-",'')
        telefone = telefone.replace(" ",'')
        if len(telefone) == 10:
            if telefone[2:3] != '2':
                raise ValidationError('Insira um número válido ')
        else:
            if len(telefone) != 11:
                raise ValidationError('Insira um número válido ')
        return telefone
    
    def clean_telefone(self):
        telefone = self.cleaned_data["telefone"]
        telefone = telefone.replace("(",'')
        telefone = telefone.replace(")",'')
        telefone = telefone.replace("-",'')
        telefone = telefone.replace(" ",'')
        if len(telefone) != 10 and len(telefone) != 0:
            raise ValidationError('Insira um número válido')        
        return telefone

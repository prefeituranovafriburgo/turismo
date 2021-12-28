from django import forms
from django.forms import ModelForm, ValidationError
from .models import *
from contas.models import Estado
from contas.functions import validate_CNPJ

class ViagemForm(ModelForm):
    dt_Chegada = forms.DateTimeField(required = False, widget=forms.SelectDateWidget(years=range(2021, 2030)))
    dt_Saida = forms.DateTimeField(required = False, widget=forms.SelectDateWidget(years=range(2021, 2030)))
    cnpj_empresa_transporte = forms.CharField(label='CNPJ', max_length=18, widget = forms.TextInput(attrs={'onkeydown':"mascara(this,icnpj)"}))

    class Meta:
        model = Viagem
        exclude = ['user', 'dt_inclusao']

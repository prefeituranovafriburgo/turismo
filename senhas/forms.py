import datetime
from pickle import TRUE
from django.http import JsonResponse
from django import forms
from django.forms import ModelForm, ValidationError
from .models import *
from contas.models import Estado
from contas.functions import validate_CNPJ
from .validations import validate_CNPJ
import json

class Date(forms.DateInput):
    input_type = 'date'


class Viagem_TurismoForm(ModelForm):
    class Meta:
        model = Viagem_Turismo
        widgets = {
            'nome_guia': forms.TextInput(attrs={'onblur': 'validar(event)',
                                                'required': 'true',
                                                'class': 'form-control'}),
            'cadastur_guia': forms.TextInput(attrs={'onblur': 'validar(event)',
                                                    'required': 'true',
                                                    'class': 'form-control'}),
            'celular': forms.TextInput(attrs={'onblur': 'validar(event)',
                                              'onkeydown': 'mascara(this,icelular)',
                                              'required': 'true',
                                              'class': 'form-control'}),
            'telefone': forms.TextInput(attrs={'onblur': 'validar(event)',
                                                         'onkeydown': 'mascara(this,itelefone)',
                                                         'required': 'true',
                                                         'class': 'form-control'}),
            'pontos_turisticos': forms.CheckboxSelectMultiple(attrs={'class': 'pontos_input', 'onblur': 'validar(event)',

                                                                     }),
            'outros': forms.TextInput(attrs={'onblur': 'validar(event)',
                                             'required': 'true',
                                             'class': 'form-control'}),
        }

        exclude = ['user', 'dt_inclusao', 'ativo']


class ViagemForm(ModelForm):
    class Meta:
        model = Viagem
        widgets = {
            'responsavel_viagem': forms.TextInput(attrs={'onblur': 'validar(event)',
                                                         'required': 'true',
                                                         'class': 'form-control'}),

            'contato_responsavel': forms.TextInput(attrs={'onkeydown': 'mascara(this,icelular)',
                                                          'onblur': 'validar(event)',
                                                          'class': 'form-control'}),

            'estado_origem': forms.Select(attrs={'onkeydown': 'mascara(this,icelular)',
                                                 'onblur': 'validar(event)',
                                                 'onchange': 'mostracidade(event)',
                                                 'class': 'form-control'}),

            'cidade_origem': forms.Select(attrs={'onblur': 'validar(event)',
                                                 'required': 'true',
                                                 'class': 'form-control'}),

            'dt_Chegada': Date(attrs={'onblur': 'validar(event)',
                                      'required': 'true',
                                      'class': 'form-control'}),

            'dt_Saida': Date(attrs={'onblur': 'validar(event)',
                                    'required': 'true',
                                    'class': 'form-control'}),

            'empresa_transporte': forms.TextInput(attrs={'onblur': 'validar(event)',
                                                         'required': 'true',
                                                         'class': 'form-control'}),

            'empresa_transporte': forms.TextInput(attrs={'onblur': 'validar(event)',
                                                         'required': 'true',
                                                         'class': 'form-control'}),

            'cadastur_empresa_transporte': forms.TextInput(attrs={'onblur': 'validar(event)',
                                                                  'required': 'true',
                                                                  'class': 'form-control'}),

            'cnpj_empresa_transporte': forms.TextInput(attrs={'onblur': 'validar(event)',
                                                              'onkeydown': 'mascara(this,icnpj)',
                                                              'required': 'true',
                                                              'class': 'form-control'}),

            'quant_passageiros': forms.TextInput(attrs={'onblur': 'validar(event)',
                                                        'required': 'true',
                                                        'class': 'form-control'}),

            'hotel': forms.TextInput(attrs={'onblur': 'validar(event)',
                                            'required': 'true',
                                            'class': 'form-control'}),

            'restaurante': forms.TextInput(attrs={'onblur': 'validar(event)',
                                                  'required': 'true',
                                                  'class': 'form-control'}),

            'tipo_veiculo': forms.Select(attrs={'onblur': 'validar(event)',
                                                'required': 'true',
                                                'class': 'form-control'}),

            'obs': forms.Textarea(attrs={'onblur': 'validar(event)',
                                         'required': 'true',
                                         'class': 'form-control'})
        }
        exclude = ['user', 'dt_inclusao', 'ativo']

    def clean_cnpj_empresa_transporte(self):
        cnpj = validate_CNPJ(self.cleaned_data["cnpj_empresa_transporte"])
        cnpj = cnpj.replace('.', '')
        cnpj = cnpj.replace('-', '')
        return cnpj

    def clean(self):
        cleaned_data = super().clean()
        data_chegada = self.cleaned_data['dt_Chegada']
        data_saida = self.cleaned_data['dt_Saida']

        if data_chegada > data_saida:
            raise ValidationError({"dt_Chegada":"Data de saida menor que a de chegada"})

        return cleaned_data 

def validate_data_caledonia(date):
    fail = False
    alert = ''
    viagens_caledonia_do_dia = Viagem.objects.filter(
        senha__contains='PC', ativo=True, dt_Chegada=date).count()

    if str(viagens_caledonia_do_dia) >= str(2):
        format = '%Y-%m-%d'
        dt = date
        data = datetime.strptime(dt, format)
        fail = True
        alert = 'Vagas esgotadas para visitação no dia ' + \
            str(data.strftime('%d/%m/%Y')+'. Escolha outra data.')
            
    return JsonResponse({
        'fail': fail,
        'alert': alert
    }) 
    
class Viagem_CaledoniaForm(ModelForm):
    class Meta:
        model = Viagem
        widgets = {
            'responsavel_viagem': forms.TextInput(attrs={'onblur': 'validar(event)',
                                                         'required': 'true',
                                                         'class': 'form-control'}),

            'contato_responsavel': forms.TextInput(attrs={'onkeydown': 'mascara(this,icelular)',
                                                          'onblur': 'validar(event)',
                                                          'class': 'form-control'}),

            'estado_origem': forms.Select(attrs={'onkeydown': 'mascara(this,icelular)',
                                                 'onblur': 'validar(event)',
                                                 'onchange': 'mostracidade(event)',
                                                 'class': 'form-control'}),

            'cidade_origem': forms.Select(attrs={'onblur': 'validar(event)',
                                                 'required': 'true',
                                                 'class': 'form-control'}),

            'dt_Chegada': Date(attrs={'onblur': 'validar(event)',
                                                'onchange': 'validarVisitacao(event)',
                                                'required': 'true',
                                                'class': 'form-control'}),

            'empresa_transporte': forms.TextInput(attrs={'onblur': 'validar(event)',
                                                         'required': 'true',
                                                         'class': 'form-control'}),

            'empresa_transporte': forms.TextInput(attrs={'onblur': 'validar(event)',
                                                         'required': 'true',
                                                         'class': 'form-control'}),

            'cadastur_empresa_transporte': forms.TextInput(attrs={'onblur': 'validar(event)',
                                                                  'required': 'true',
                                                                  'class': 'form-control'}),

            'cnpj_empresa_transporte': forms.TextInput(attrs={'onblur': 'validar(event)',
                                                              'onkeydown': 'mascara(this,icnpj)',
                                                              'required': 'true',
                                                              'class': 'form-control'}),

            'quant_passageiros': forms.TextInput(attrs={'onblur': 'validar(event)',
                                                        'required': 'true',
                                                        'class': 'form-control'}),

            'hotel': forms.TextInput(attrs={'onblur': 'validar(event)',
                                            'required': 'true',
                                            'class': 'form-control'}),

            'restaurante': forms.TextInput(attrs={'onblur': 'validar(event)',
                                                  'required': 'true',
                                                  'class': 'form-control'}),

            'tipo_veiculo': forms.Select(attrs={'onblur': 'validar(event)',
                                                'required': 'true',
                                                'class': 'form-control'}),

            'obs': forms.Textarea(attrs={'onblur': 'validar(event)',
                                         'required': 'true',
                                         'class': 'form-control'})
        }

        exclude = ['user', 'dt_inclusao', 'ativo', 'dt_Saida']

    def clean_cnpj_empresa_transporte(self):
        cnpj = validate_CNPJ(self.cleaned_data["cnpj_empresa_transporte"])
        cnpj = cnpj.replace('.', '')
        cnpj = cnpj.replace('-', '')
        return cnpj

    def clean_dt_Chegada(self):
        data_chegada = validate_data(self.cleaned_data['dt_Chegada'])

        format = '%Y-%m-%d'
        data_ = data_chegada.strftime(format)

        data = validate_data_caledonia(data_)

        data=json.loads(data.content)
        if data['fail']:
            raise ValidationError(data['alert'])   

        return data_chegada
       



class Viagem_turismo_CaledoniaForm(ModelForm):
    class Meta:
        model = Viagem_Turismo
        widgets = {
            'nome_guia': forms.TextInput(attrs={'onblur': 'validar(event)',
                                                'required': 'true',
                                                'class': 'form-control'}),
            'cadastur_guia': forms.TextInput(attrs={'onblur': 'validar(event)',
                                                    'required': 'true',
                                                    'class': 'form-control'}),
            'celular': forms.TextInput(attrs={'onblur': 'validar(event)',
                                                        'onkeydown': 'mascara(this,icelular)',
                                                        'required': 'true',
                                                        'class': 'form-control'}),
            'telefone': forms.TextInput(attrs={'onblur': 'validar(event)',
                                               'onkeydown': 'mascara(this,itelefone)',
                                               'required': 'true',
                                               'class': 'form-control'}),
        }

        exclude = ['user', 'dt_inclusao', 'ativo', 'pontos_turisticos', 'outros']

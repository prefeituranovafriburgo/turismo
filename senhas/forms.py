from pickle import TRUE
from django import forms
from django.forms import ModelForm, ValidationError
from .models import *
from contas.models import Estado
from contas.functions import validate_CNPJ
from .validations import validate_CNPJ


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
        print(self.cleaned_data["cnpj_empresa_transporte"])
        cnpj = validate_CNPJ(self.cleaned_data["cnpj_empresa_transporte"])
        cnpj = cnpj.replace('.', '')
        cnpj = cnpj.replace('-', '')
        print(cnpj)
        return cnpj


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

        labels = {
            "dt_Chegada": "DATAAAAA"
        }

        def clean_cnpj_empresa_transporte(self):
            print(self.cleaned_data["cnpj_empresa_transporte"])
            cnpj = validate_CNPJ(self.cleaned_data["cnpj_empresa_transporte"])
            cnpj = cnpj.replace('.', '')
            cnpj = cnpj.replace('-', '')
            print(cnpj)
            return cnpj

        exclude = ['user', 'dt_inclusao', 'ativo', 'dt_Saida']


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
            'pontos_turisticos': forms.CheckboxSelectMultiple(attrs={'onblur': 'validar(event)',
                                                                     'onchange': 'checkOutros(event)',
                                                                     }),
            'outros': forms.TextInput(attrs={'onblur': 'validar(event)',
                                             'required': 'true',
                                             'class': 'form-control'}),
        }

        exclude = ['user', 'dt_inclusao', 'ativo', 'pontos_turisticos']

__author__ = "Théo Carranza theocarranza@gmail.com"
__copyright__ = "Copyright (C) 2017 Théo Carranza"
__license__ = "Public Domain"
__version__ = "1.0"

""" This is a slight modification from the class created by author dudus
 (https://djangosnippets.org/users/dudus/) for use on the model layer.
 It is optimized for Python 3.5  and PEP8 compliant. """

import re
from itertools import cycle

from django.core.validators import EMPTY_VALUES
from django.forms import ValidationError
from django.utils.translation import ugettext_lazy as _



error_messages = {
    'invalid': _("Número de CPF inválido."),
    'digits_only': _("Este campo requer somente números."),
    'max_digits': _("Este campo requer 11 dígitos."),
}


def DV_maker(v):
    if v >= 2:
        return 11 - v
    return 0


def validate_CPF(value):
    """
    Value can be either a string in the format XXX.XXX.XXX-XX or an
    11-digit number.
    """

    if value in EMPTY_VALUES:
        return u''
    if not value.isdigit():
        value = re.sub("[-\.]", "", value)
    orig_value = value[:]
    try:
        int(value)
    except ValueError:
        raise ValidationError(error_messages['digits_only'])
    if len(value) != 11:
        raise ValidationError(error_messages['max_digits'])
    orig_dv = value[-2:]

    new_1dv = sum([i * int(value[idx]) for idx, i in enumerate(range(10, 1, -1))])
    new_1dv = DV_maker(new_1dv % 11)
    value = value[:-2] + str(new_1dv) + value[-1]
    new_2dv = sum([i * int(value[idx]) for idx, i in enumerate(range(11, 1, -1))])
    new_2dv = DV_maker(new_2dv % 11)
    value = value[:-1] + str(new_2dv)
    if value[-2:] != orig_dv:
        raise ValidationError(error_messages['invalid'])

    return orig_value

def validate_CNPJ(value):
    """
    Value can be either a string in the format XX.XXX.XXX/XXXX-XX or a
    group of 14 characters.
    :type value: object
    """
    value = str(value)
    if value in EMPTY_VALUES:
        return u''
    if not value.isdigit():
        value = re.sub("[-/\.]", "", value)
    orig_value = value[:]
    try:
        int(value)
    except ValueError:
        raise ValidationError(error_messages['digits_only'])
    if len(value) > 14:
        raise ValidationError(error_messages['max_digits'])
    orig_dv = value[-2:]

    new_1dv = sum([i * int(value[idx]) for idx, i in enumerate(list(range(5, 1, -1)) + list(range(9, 1, -1)))])
    new_1dv = DV_maker(new_1dv % 11)
    value = value[:-2] + str(new_1dv) + value[-1]
    new_2dv = sum([i * int(value[idx]) for idx, i in enumerate(list(range(6, 1, -1)) + list(range(9, 1, -1)))])
    new_2dv = DV_maker(new_2dv % 11)
    value = value[:-1] + str(new_2dv)
    if value[-2:] != orig_dv:
        raise ValidationError(error_messages['invalid'])

    return orig_value

#VALIDATIONS FOR EDUARDO SALARINI
def validations(request):    
    validate={}
    validate['nome']=validateNOME(request['nome'])
    validate['cpf']=validateCPF(request['cpf'])
    validate['cadastur']=validateCadastur(request['cadastur'])
    validate['email']=validateEMAIL(request['email'])
    validate['celular']=validateCelular(request['celular'])
    validate['telefone']=validateTelefone(request['telefone'])
    validate['senha']=validatePassword(request['senha'], request['senha_confirma'])    
    return validate

def validationsViagem(request):  
    validate={}
    validate['veiculo']=validateVeiculo(request['tipo_veiculo'])
    validate['quant_passageiros']=validatePassageiros(request['quant_passageiros'])
    validate['cadastur_empresa_transporte']=validateCadastur(request['cadastur_empresa_transporte'])
    validate['cnpj_empresa_transporte']=validateCNPJ(request['cnpj_empresa_transporte'])
    return validate

def validateCNPJ(cnpj_):
    cnpj = [int(char) for char in cnpj_ if char.isdigit()]
    if len(cnpj) != 14:
        return {'state': False, 'msg': 'CNPJ invalido.'}

    if cnpj in (c * 14 for c in "1234567890"):
        return {'state': False, 'msg': 'CNPJ invalido.'}

    cnpj=''.join([str(_) for _ in cnpj])
    cnpj_r = cnpj[::-1]
    for i in range(2, 0, -1):
        cnpj_enum = zip(cycle(range(2, 10)), cnpj_r[i:])
        dv = sum(map(lambda x: int(x[1]) * x[0], cnpj_enum)) * 10 % 11
        if cnpj_r[i - 1:i] != str(dv % 10):
            return {'state': False, 'msg': 'CNPJ invalido.'}
    return {'state': True, 'msg': ''}

def validatePassageiros(passageiros):
    if len(passageiros)<1 or passageiros=='':
        return {'state': False, 'msg': 'Informe a quantidade de passageiros.'}  
    return {'state': True, 'msg': ''}

def validateVeiculo(veiculo):
    if veiculo!='':
        return {'state': True, 'msg': ''}
    return {'state': False, 'msg': 'Informe o veiculo.'}


def validateNOME(nome):
    if not bool(re.fullmatch('[A-Za-z]{2,25}( [A-Za-z]{2,25})?', nome)) or len(nome)<=3:
        return {'state': False, 'msg': 'Nome inválido.'}
    return {'state': True, 'msg': ''}

    return 'teste'
def validateCadastur(cadastur):
    if len(cadastur)!=8:
        return {'state': False, 'msg': 'Cadastur inválido.'}
    return {'state': True, 'msg': ''}

def validateCPF(cpf_):      
    #  Obtém os números do CPF e ignora outros caracteres
    cpf = [int(char) for char in cpf_ if char.isdigit()]
    print(cpf)
    #  Verifica se o CPF tem 11 dígitos
    if len(cpf) != 11:
        return {'state': False, 'msg': 'CPF inválido.'}
    #  Verifica se o CPF tem todos os números iguais, ex: 111.111.111-11
    #  Esses CPFs são considerados inválidos mas passam na validação dos dígitos
    #  Antigo código para referência: if all(cpf[i] == cpf[i+1] for i in range (0, len(cpf)-1))
    if cpf == cpf[::-1]:
        return {'state': False, 'msg': 'CPF inválido.'}
    #  Valida os dois dígitos verificadores
    for i in range(9, 11):
        value = sum((cpf[num] * ((i+1) - num) for num in range(0, i)))
        digit = ((value * 10) % 11) % 10
        if digit != cpf[i]:
            return {'state': False, 'msg': 'CPF inválido.'}
    return {'state': True, 'msg': '', 'cpf': ''.join([str(_) for _ in cpf])}

def validateEMAIL(email):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    if(re.fullmatch(regex, email)):
        return {'state': True, 'msg': ''}
    return {'state': False, 'msg': 'Email inválido.'}

def validateCelular(cel):
    celular=[int(char) for char in cel if char.isdigit()]
    if len(celular)!=11:
        return {'state': False, 'msg': 'Número de celular inválido.'}        
    return {'state': True, 'msg': ''}   

def validateTelefone(tel):
    telefone=[int(char) for char in tel if char.isdigit()]
    if len(telefone)!=11:
        return {'state': False, 'msg': 'Número de telefone inválido.'}        
    return {'state': True, 'msg': ''}   

def validatePassword(senha, senha2):
    if senha==senha2:
        if not len(senha)>=8:
            return {'state': False, 'msg': 'A senha precisa ter pelo menos 8 caracteres.'}        
        return {'state': True, 'msg': ''}
    
    return {'state': False, 'msg': 'Senhas não coincidem.'}        



from datetime import datetime, timedelta
import re
from itertools import cycle

from django.core.validators import EMPTY_VALUES
from django.forms import ValidationError
from django.utils.translation import gettext_lazy as _

error_messages = {
    'invalid_CNPJ': _("CNPJ inválido."),
    'max_digits': _("Este campo requer 14 dígitos."),

    'invalid_date': _('Data inválida.'),
    'invalid_date_format': _('Formato de data inválido.'),

    'not_a_match': _("Senhas não coincidem"),
    'invalid_min_senha_length': _('A senha precisar ter pelo menos 8 caracteres'),

    'invalid_numero_passageiros': _("Informe um número maior que 1."),

    'invalid_nome': _("Nome inválido."),

    'tel_max_digits': _("O telefone deve conter 10 ou 11 números."),

    'invalid_CPF': _("CPF inválido."),

    'invalid_Cadastur': _('Cadastur inválido.'),

    'invalid_EMAIL': _('Email inválido.'),

    'invalid_celular': _("O número de celular é invalido."),
    'invalid_telefone': _("O número de telefone é invalido."),
}


def validate_CNPJ(value):
    cnpj = [int(char) for char in value if char.isdigit()]
    if len(cnpj) != 14:
        raise ValidationError(error_messages['max_digits'])
    if cnpj in (c * 14 for c in "1234567890"):
        raise ValidationError(error_messages['invalid_CNPJ'])
    orig_value = ''.join([str(_) for _ in cnpj])
    cnpj_r = orig_value[::-1]
    for i in range(2, 0, -1):
        cnpj_enum = zip(cycle(range(2, 10)), cnpj_r[i:])
        dv = sum(map(lambda x: int(x[1]) * x[0], cnpj_enum)) * 10 % 11
        if cnpj_r[i - 1:i] != str(dv % 10):
            raise ValidationError(error_messages['invalid_CNPJ'])
    return orig_value


def validate_passageiros(value):
    if value < 1 or value == '':
        raise ValidationError(error_messages['invalid_numero_passageiros'])
    return value


def validate_nome(nome):
    if not bool(re.fullmatch("^[\w'\-,.][^0-9_!¡?÷?¿/\\+=@#$%ˆ&*(){}|~<>;:[\]]{2,}$", nome)) or len(nome) <= 3:
        raise ValidationError(error_messages['invalid_nome'])
    return nome


def validate_Cadastur(cadastur):
    cadastur_ = [int(char) for char in cadastur if char.isdigit()]

    if cadastur in (c * len(cadastur) for c in "1234567890"):
        raise ValidationError(error_messages['invalid_Cadastur'])

    cadastur = ''.join([str(_) for _ in cadastur_])

    if len(cadastur_) < 8:
        raise ValidationError(error_messages['invalid_Cadastur'])

    return cadastur


def validate_CPF(cpf_):
    #  Obtém os números do CPF e ignora outros caracteres
    cpf = [int(char) for char in cpf_ if char.isdigit()]
    #  Verifica se o CPF tem 11 dígitos
    if len(cpf) != 11:
        return ValidationError(error_messages['invalid_CPF'])

    #  Verifica se o CPF tem todos os números iguais, ex: 111.111.111-11
    #  Esses CPFs são considerados inválidos mas passam na validação dos dígitos
    #  Antigo código para referência: if all(cpf[i] == cpf[i+1] for i in range (0, len(cpf)-1))
    if cpf in (c * 11 for c in "1234567890"):
        return ValidationError(error_messages['invalid_CPF'])

    if cpf == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]:
        return ValidationError(error_messages['invalid_CPF'])

    if cpf == cpf[::-1]:
        return ValidationError(error_messages['invalid_CPF'])
    #  Valida os dois dígitos verificadores
    for i in range(9, 11):
        value = sum((cpf[num] * ((i+1) - num) for num in range(0, i)))
        digit = ((value * 10) % 11) % 10
        if digit != cpf[i]:
            return ValidationError(error_messages['invalid_CPF'])

    return ''.join([str(_) for _ in cpf])


def validate_EMAIL(email):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    if(not re.fullmatch(regex, email)):
        raise ValidationError(error_messages['invalid_EMAIL'])
    return email


def validate_celular(cel):
    celular = [int(char) for char in cel if char.isdigit()]
    if len(celular) == 11:
        return ''.join([str(_) for _ in celular])

    raise ValidationError(error_messages['invalid_celular'])


def validate_telefone(tel):
    telefone = [int(char) for char in tel if char.isdigit()]
    if len(telefone) == 10 or len(telefone) == 0:
        return ''.join([str(_) for _ in telefone])

    raise ValidationError(error_messages['invalid_telefone'])

def validate_senha(senha, senha2):
    if senha == senha2:
        if not len(senha) >= 8:
            raise ValidationError(error_messages['invalid_min_senha_length'])
        return senha

    raise ValidationError(error_messages['not_a_match'])
    
def validate_data(data):
    print('teste', data)
    try:
        format = '%Y-%m-%d'
        data_ = datetime.strptime(data.strftime(format), format)
    except Exception as E:
        raise ValidationError(error_messages['invalid_date_format'])

    data_now = datetime.now() - timedelta(2)
    if data_ < data_now:
        raise ValidationError(error_messages['invalid_date'])
    
    return data

from django import template
register = template.Library()

@register.filter(name='formata_tel')
def formata_tel(numero):
    if numero == None:
        return ''

    if len(numero) == 10:
        first = numero[0:2]
        second = numero[2:6]
        third = numero[6:10]
        return '(' + first + ')' + ' ' + second + '-' + third
    else:
        first = numero[0:2]
        second = numero[2:7]
        third = numero[7:11]
        return '(' + first + ')' + ' ' + second + '-' + third

@register.filter(name='formata_cep')
def formata_cep(numero):
    if numero == None:
        return ''

    first = numero[0:2]
    second = numero[2:5]
    third = numero[5:9]
    return first + '.' + second + '-' + third

@register.filter(name='formata_cpf')
def formata_cpf(numero):
    if numero == None:
        return ''

    first = numero[0:3]
    second = numero[3:6]
    third = numero[6:9]
    fourth = numero[9:11]
    return first + '.' + second + '.' + third + '-' + fourth

@register.filter(name='formata_cnpj')
def formata_cnpj(numero):
    if numero == None:
        return ''

    first = numero[0:2]
    second = numero[2:5]
    third = numero[5:8]
    fourth = numero[8:12]
    fifth = numero[12:14]
    return first + '.' + second + '.' + third + '/' + fourth + '-' + fifth

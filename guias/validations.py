import re 
from contas.functions import validateCadastur, validateTelefone

def validar_cadastro_guia(request):
    validation={}
    validation['nome']=validar_nome(request['nome'])
    validation['cadastur']=validateCadastur([request['cadastur']])
    validation['telefone']=validateTelefone([request['telefone']])
    validation['email']=validar_email(request['email'])
    print(validation)
    for i in validation:
        if validation[i]['state']==True:
            print(i)
            return False, validation
    return True, validation
    

def validar_nome(str):
    if all(char.isalpha() or char.isspace() for char in str):
        return {'state': False, 'msg':''}
    return {'state': True, 'msg': 'Nome inválido.'}

def validar_email(email):
    regex=re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
    if re.fullmatch(regex, email):
       return {'state': False, 'msg':''}
    return {'state': True, 'msg': 'Email inválido.'}
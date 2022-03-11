import re 
from contas.functions import validateCadastur, validateCelular, validateEMAIL, validateNOME, validateTelefone

def validar_cadastro_guia(request):
    print('validar', request)
    validation={}
    validation['nome']=validateNOME(request['nome'])
    validation['cadastur']=validateCadastur(request['cadastur'])
    validation['telefone']=validateTelefone(request['telefone'])
    validation['email']=validateEMAIL(request['email'])
    print(validation)
    for i in validation:
        if validation[i]['state']==False:
            print('outro teste', i)
            return False, validation
    return True, validation
    

def validar_nome(str):
    if all(char.isalpha() or char.isspace() for char in str):
        return {'state': True, 'msg':''}
    return {'state': False, 'msg': 'Nome inválido.'}

def validar_email(email):
    regex=re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
    if re.fullmatch(regex, email):
       return {'state': True, 'msg':''}
    return {'state': False, 'msg': 'Email inválido.'}
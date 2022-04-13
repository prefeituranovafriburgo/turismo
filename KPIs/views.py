from multiprocessing import context
from urllib import request
from django.shortcuts import render
from contas.models import Cidade
from turismo.decorators import membro_secretaria_required
from senhas.models import Viagem, Viagem_Turismo
from django.contrib.auth.models import User
from django.db.models import Count

@membro_secretaria_required
def index(request):
    #Usuários Registrados
    ano_registro_users='2022'
    users_ano=User.objects.filter(date_joined__year=ano_registro_users)
    total_usuarios=users_ano.count()
    users_mes=User.objects.filter(date_joined__contains='-03-')    
    #Viagens Registradas
    viagens=Viagem.objects.all()
    viagem_turismo=Viagem_Turismo.objects.all().count()
    ##Origens Registradas
    cidades_contadas=viagens.values('cidade_origem').annotate(total=Count('cidade_origem')).order_by('cidade_origem')
    date_cidades=[]
    for i in cidades_contadas:
        cidade=Cidade.objects.get(id=i['cidade_origem'])
        date_cidades.append({'nome': cidade.nome + ' - ' + cidade.estado.uf, 'qnt':i['total']})

    # print(date_cidades)
    context={
        'date_cidades': date_cidades,
        'ano_registro_users': ano_registro_users,
        'total_usuarios': total_usuarios,
        'total_viagens': viagens.count(),
        'total_turismo': viagem_turismo,
        'total_compras': viagens.count()-viagem_turismo,
        'date_usuarios': [0, 10, 23 , 17, 9, 11, 27],
        'date_usuarios_anual': [20, 80, 123 , 217, 19, 11, 127, 63],
        'meses': {'Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho',
                  'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'}
    }
    return render(request, 'kpis/index.html', context)

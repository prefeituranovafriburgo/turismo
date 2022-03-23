from multiprocessing import context
from urllib import request
from django.shortcuts import render
from turismo.decorators import membro_secretaria_required
from senhas.models import Viagem, Viagem_Turismo
from django.contrib.auth.models import User

@membro_secretaria_required
def index(request):
    #Usuários Registrados
    users_ano=User.objects.filter(date_joined__year='2022')
    users_mes=User.objects.filter(date_joined__contains='-03-')    
    #Viagens Registradas
    viagens=Viagem.objects.all().count()
    viagem_turismo=Viagem_Turismo.objects.all().count()
    ##Origens Registradas
    print(users_mes, users_ano)
    print(request.user.date_joined)

    context={
        'total_viagens': viagens,
        'total_turismo': viagem_turismo,
        'total_compras': viagens-viagem_turismo,
        'date_usuarios': [0, 10, 23 , 17, 9, 11, 27],
        'date_usuarios_anual': [20, 80, 123 , 217, 19, 11, 127, 63],
        'meses': {'Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho',
                  'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'}
    }
    return render(request, 'kpis/index.html', context)

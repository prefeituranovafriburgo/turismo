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
    return render(request, 'kpis/index.html')

@membro_secretaria_required
def usuarios(request):
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
    cores=['#0015ff', '#00fff6', '#329787', '#0cff00', '#fff200', '#ffa100',
           '#ff0000', '#ff0077', '#ff00c3', '#ff00c0', '#b600ff', '#5000ff', 
           '#00aeff', '#0050ff']
    for i in cidades_contadas:
        cidade=Cidade.objects.get(id=i['cidade_origem'])
        try:
            date_cidades.append({'nome': cidade.nome + ' - ' + cidade.estado.uf, 'qnt':i['total'], 'cor': cores.pop()})
        except:
            date_cidades.append({'nome': cidade.nome + ' - ' + cidade.estado.uf, 'qnt':i['total'], 'cor': 'silver'})

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
    return render(request, 'kpis/usuarios.html', context)

@membro_secretaria_required
def viagens(request):
    viagens=Viagem.objects.all()
    viagem_turismo=Viagem_Turismo.objects.all().count()
    context={
        'total_viagens': viagens.count(),
        'total_turismo': viagem_turismo,
        'total_compras': viagens.count()-viagem_turismo,
        'filtro': False,
        }
    print(request)
    if request.method=='POST':        
        if request.POST['dt_inclusao']!='' and request.POST['dt_inclusao_f']!='':
            
            viagens=Viagem.objects.filter(dt_inclusao__range=[request.POST['dt_inclusao'],request.POST['dt_inclusao_f']]).order_by('dt_inclusao')
            soma=0
            for i in viagens:
                soma+=i.quant_passageiros            
            try:
                viagem_turismo=Viagem_Turismo.objects.filter(dt_inclusao__range=[request.POST['dt_inclusao'],request.POST['dt_inclusao_f']]).count()
            except:
                viagem_turismo=0
            context={
                'dt_inicial': request.POST['dt_inclusao'],
                'dt_final': request.POST['dt_inclusao_f'],
                'filtro': True,
                'viagens': viagens,
                'total_viagens': viagens.count(),
                'total_turismo': viagem_turismo,
                'total_compras': viagens.count()-viagem_turismo,
                'soma': soma,
                'filtrado_por': 'inclusão'
            }
        elif request.POST['dt_chegada']!='' and request.POST['dt_chegada_f']!='':            
            viagens=Viagem.objects.filter(dt_Chegada__range=[request.POST['dt_chegada'],request.POST['dt_chegada_f']]).order_by('dt_Chegada')
            soma=0
            turismo=[]
            for i in viagens:
                soma+=i.quant_passageiros            
                try: 
                    turismo.append(Viagem_Turismo.objects.get(viagem=i))
                except:
                    pass
            viagem_turismo=len(turismo)
            context={
                'dt_inicial': request.POST['dt_chegada'],
                'dt_final': request.POST['dt_chegada_f'],
                'filtro': True,
                'viagens': viagens,
                'total_viagens': viagens.count(),
                'total_turismo': viagem_turismo,
                'total_compras': viagens.count()-viagem_turismo,
                'soma': soma,
                'filtrado_por': 'chegada'
            }
    return render(request, 'kpis/viagens.html', context)
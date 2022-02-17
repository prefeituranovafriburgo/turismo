from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from contas.functions import validationsViagem

from contas.views import sair
from senhas.models import Tipo_Veiculo, Viagem, Viagem_Turismo
from .models import Pontos_Turisticos
from .forms import ViagemForm
from .functions import get_random_string

# Create your views here.

@login_required
def inicio(request):
    return render(request, 'senhas/index.html')


@login_required
def cad_transporte(request):    
    viagens = Viagem.objects.filter(user=request.user)
    return render(request, 'senhas/cad_transporte.html', { 'viagens': viagens })


@login_required
def viagem_inclui(request, tipo):
    print(tipo)
    # Essa variavel VALIDATION é iniciada aqui para não haver conflito 
    # enquanto não existir uma requisição POST
    validation={'veiculo': {'state': True},'quant_passageiros': {'state': True}, 
                'cnpj_empresa_transporte': {'state': True}, 'cadastur_empresa_transporte': {'state': True}, }  

    if request.method == 'POST':
        print(request.POST)        
        form = ViagemForm(request.POST)
        #Aqui a VALIDATION toma novos valores de acordo com o FORM
        validation, valido=validationsViagem(request.POST)
                                
        if valido:            
            try:
                viagem=Viagem(                    
                    user=request.user, 
                    dt_Chegada=request.POST['dt_chegada'],
                    dt_Saida=request.POST['dt_saida'],
                    ficarao_hospedados=True,
                    hotel=request.POST['hotel'],
                    restaurante=request.POST['restaurante'],
                    tipo_veiculo=Tipo_Veiculo.objects.get(id=request.POST['tipo_veiculo']),
                    quant_passageiros=request.POST['quant_passageiros'],
                    empresa_transporte=request.POST['empresa_transporte'],
                    cnpj_empresa_transporte=validation['cnpj_empresa_transporte']['cnpj'],
                    cadastur_empresa_transporte=request.POST['cadastur_empresa_transporte'],
                    obs=request.POST['obs'])                
                viagem.save()    
                          
                if tipo=='turismo':
                    viagem.senha='t'+get_random_string()+str(viagem.id)+get_random_string()+'/22NF' 
                    viagem.save()
                    viagem_turismo=Viagem_Turismo(
                        viagem=viagem,
                        nome_guia=request.POST['nome_guia'],
                        cadastur_guia=request.POST['cadastur_guia'],
                        celular=request.POST['celular'],
                        telefone=request.POST['telefone'],                        
                    ) 
                    viagem_turismo.save()
                    for ponto in request.POST.getlist('pontos_turisticos'):
                        print(ponto)
                        viagem_turismo.pontos_turisticos.add(Pontos_Turisticos.objects.get(nome=ponto))
                    viagem_turismo.save()                    
                else:
                    viagem.senha='c'+get_random_string()+str(viagem.id)+get_random_string()+'/22NF' 
                    viagem.save()
                messages.success(request, 'Viagem cadastrada.')
                return redirect('senhas:cad_transporte')

            except Exception as e:
                print('e:', e)
                erro = str(e).split(', ')

                print('erro:', erro)

                if erro[0] == '(1062':
                    messages.error(request, 'Erro: Usuário já existe.')
                else:
                    # Se teve erro:
                    print('Erro: ', form.errors)
                    erro_tmp = str(form.errors)
                    erro_tmp = erro_tmp.replace('<ul class="errorlist">', '')
                    erro_tmp = erro_tmp.replace('</li>', '')
                    erro_tmp = erro_tmp.replace('<ul>', '')
                    erro_tmp = erro_tmp.replace('</ul>', '')
                    erro_tmp = erro_tmp.split('<li>')

                    messages.error(request, erro_tmp[1] + ': ' + erro_tmp[2])
        else:
            messages.error(request, 'Corrigir o erro apresentado.')
    else:
        form = ViagemForm()

    #Pegando as devidas informações para os selects do formulario abaixo
    veiculos=Tipo_Veiculo.objects.all()
    pontosTuristicos= Pontos_Turisticos.objects.all()
    #Incluindo as informações coletas no contexto para uso no Template
    context={ 
        'form': form, 
        'validation': validation, 
        'veiculos': veiculos, 
        'pontos': pontosTuristicos,
        'tipo': tipo
    }
    return render(request, 'senhas/viagem_inclui.html', context)


@login_required
def viagem(request, id):

    viagem = Viagem.objects.get(id=id)

    try:
        viagem_turismo = Viagem_Turismo.objects.get(viagem=viagem)
        pontos_turisticos=viagem_turismo.pontos_turisticos.all()
        print(pontos_turisticos)
    except:
        viagem_turismo = None
        pontos_turisticos= None

    return render(request, 'senhas/viagem.html', { 'viagem': viagem, 'viagem_turismo': viagem_turismo, 'pontos_turisticos': pontos_turisticos })


@login_required
def viagem_altera(request, id):
    from datetime import date

    viagem = Viagem.objects.get(id=id)

    if date.today() > viagem.dt_Saida:
        messages.error(request, 'Não é mais possível alterar viagem, já que a viagem já ocorreu.')
        return redirect('/viagem/' + str(id))


    if viagem.user != request.user:
        messages.error(request, 'Viagem não percente a usuário logado.')
        return redirect('/viagem/' + str(id))


    if request.method == 'POST':
        form = ViagemForm(request.POST, instance=viagem)

        if form.is_valid():
#            cidade = Cidade.objects.get(id=request.POST.get('cidade'))

            try:

                form.save()

                messages.success(request, 'Viagem alterada.')
                return redirect('/viagem/' + str(id))

            except Exception as e:
                print('e:', e)
                erro = str(e).split(', ')

                print('erro:', erro)

                if erro[0] == '(1062':
                    messages.error(request, 'Erro: Usuário já existe.')
                else:
                    # Se teve erro:
                    print('Erro: ', form.errors)
                    erro_tmp = str(form.errors)
                    erro_tmp = erro_tmp.replace('<ul class="errorlist">', '')
                    erro_tmp = erro_tmp.replace('</li>', '')
                    erro_tmp = erro_tmp.replace('<ul>', '')
                    erro_tmp = erro_tmp.replace('</ul>', '')
                    erro_tmp = erro_tmp.split('<li>')

                    messages.error(request, erro_tmp[1] + ': ' + erro_tmp[2])
        else:
            messages.error(request, 'Corrigir o erro apresentado.')
    else:
        form = ViagemForm(instance=viagem)

    return render(request, 'senhas/viagem_inclui.html', { 'form': form })


@login_required
def cad_acesso_ponto(request):

    return render(request, 'senhas/cad_acesso_ponto.html')


@login_required
def gera_senha(request, id):

    viagem = Viagem.objects.get(id=id)

    try:
        viagem_turismo = Viagem_Turismo.objects.get(viagem=viagem)
    except:
        viagem_turismo = None

    return render(request, 'senhas/gera_senha.html', { 'viagem': viagem, 'viagem_turismo': viagem_turismo })

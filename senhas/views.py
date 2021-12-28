from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from contas.views import sair
from senhas.models import Viagem, Viagem_Turismo
from .forms import ViagemForm

# Create your views here.

@login_required
def inicio(request):
    return render(request, 'senhas/inicio.html')


@login_required
def cad_transporte(request):

    viagens = Viagem.objects.filter(user=request.user)

    return render(request, 'senhas/cad_transporte.html', { 'viagens': viagens })


@login_required
def viagem_inclui(request):
    if request.method == 'POST':
        form = ViagemForm(request.POST)

        if form.is_valid():

            try:
                form_aux = form.save(commit=False)
                form_aux.user = request.user
                form_aux.save()

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

    return render(request, 'senhas/viagem_inclui.html', { 'form': form })


@login_required
def viagem(request, id):

    viagem = Viagem.objects.get(id=id)

    try:
        viagem_turismo = Viagem_Turismo.objects.get(viagem=viagem)
    except:
        viagem_turismo = None

    return render(request, 'senhas/viagem.html', { 'viagem': viagem, 'viagem_turismo': viagem_turismo })


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

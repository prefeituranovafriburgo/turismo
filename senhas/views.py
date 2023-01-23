from multiprocessing import context

from django.http import FileResponse, Http404, JsonResponse

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from requests import request
from contas.functions import validationsViagem
from django.core.exceptions import PermissionDenied
import json
from contas.views import sair
from contas.models import Estado, Cidade
from senhas.models import Tipo_Veiculo, Viagem, Viagem_Turismo

from turismo.settings import BASE_DIR
from .models import Links_Menu, Pontos_Turisticos
from .forms import Viagem_CaledoniaForm, Viagem_turismo_CaledoniaForm, ViagemForm, Viagem_TurismoForm
from .functions import get_random_string
import time
import pickle
from datetime import date, timedelta, datetime
import pdfkit
from turismo.decorators import membro_secretaria_required, membro_fiscais_required

@login_required
def inicio(request):
    context={
        'links': Links_Menu.objects.all().values()
    }
    return render(request, 'senhas/index.html', context)


@login_required
def cad_transporte(request):
    hoje = date.today()
    viagens = Viagem.objects.filter(user=request.user, ativo=True)

    return render(request, 'senhas/cad_transporte.html', {'viagens': viagens})


@login_required
def viagem_compras_editar(request, senha):
    from datetime import date
    viagem = Viagem.objects.get(senha=senha)
    estados = Estado.objects.all().order_by('nome')

    if date.today() > viagem.dt_Saida:
        messages.error(
            request, 'Não é mais possível alterar viagem, já que a viagem já ocorreu.')
        return redirect('/viagem/' + str(senha))

    if viagem.user != request.user:
        messages.error(request, 'Viagem não percente a usuário logado.')
        return redirect('/viagem/' + str(senha))

    if request.method == 'POST':
        form = ViagemForm(request.POST, instance=viagem)
        if form.is_valid():
            viagem = form.save()
            viagem.senha = senha
            viagem.save()
            messages.success(request, 'Viagem alterada.')
            return redirect('senhas:cad_transporte')
        else:
            print(form.errors)

    form = ViagemForm(instance=viagem)

    context = {
        'form': form,
        'viagem': viagem,
        'estados': estados,
    }

    return render(request, 'senhas/editar/viagem_compras_editar.html', context)


@login_required
def viagem_turismo_editar(request, senha):
    from datetime import date
    viagem = Viagem.objects.get(senha=senha)
    viagem_turismo = Viagem_Turismo.objects.get(viagem=viagem)
    estados = Estado.objects.all().order_by('nome')

    form = ViagemForm(instance=viagem)
    form_turismo = Viagem_TurismoForm(instance=viagem_turismo)

    if date.today() > viagem.dt_Saida:
        messages.error(
            request, 'Não é mais possível alterar viagem, já que a viagem já ocorreu.')
        return redirect('/viagem/' + str(senha))

    if viagem.user != request.user:
        messages.error(request, 'Viagem não percente a usuário logado.')
        return redirect('/viagem/' + str(senha))

    if request.method == 'POST':
        form = ViagemForm(request.POST, instance=viagem)
        form_turismo = Viagem_TurismoForm(request.POST, instance=viagem)
        if form.is_valid():
            if form_turismo.is_valid():

                viagem = form.save()
                viagem.senha = senha
                viagem.save()

                viagem_turismo = form_turismo.save()
                viagem_turismo.senha = senha
                viagem_turismo.save()

                messages.success(request, 'Viagem alterada.')
                return redirect('senhas:cad_transporte')

            else:
                print(form_turismo.errors)
        else:
            print(form.errors)

    context = {
        'form': form,
        'form_turismo': form_turismo,
        'viagem': viagem,
        'estados': estados,
    }

    return render(request, 'senhas/editar/viagem_turismo_editar.html', context)


@login_required
def viagem_caledonia_editar(request, senha):
    from datetime import date
    viagem = Viagem.objects.get(senha=senha)
    viagem_turismo = Viagem_Turismo.objects.get(viagem=viagem)
    estados = Estado.objects.all().order_by('nome')

    form = Viagem_CaledoniaForm(instance=viagem)
    form_turismo = Viagem_turismo_CaledoniaForm(instance=viagem_turismo)

    if date.today() > viagem.dt_Saida:
        messages.error(
            request, 'Não é mais possível alterar viagem, já que a viagem já ocorreu.')
        return redirect('/viagem/' + str(senha))

    if viagem.user != request.user:
        messages.error(request, 'Viagem não percente a usuário logado.')
        return redirect('/viagem/' + str(senha))

    if request.method == 'POST':
        form = Viagem_CaledoniaForm(request.POST, instance=viagem)
        form_turismo = Viagem_turismo_CaledoniaForm(
            request.POST, instance=viagem)

        if form.is_valid():
            if form_turismo.is_valid():

                viagem = form.save()
                viagem.senha = senha
                viagem.save()

                viagem_turismo = form_turismo.save()
                viagem_turismo.senha = senha
                viagem_turismo.save()

                messages.success(request, 'Viagem alterada.')
                return redirect('senhas:cad_transporte')

            else:
                print(form_turismo.errors)
        else:
            print(form.errors)

    context = {
        'form': form,
        'form_turismo': form_turismo,
        'viagem': viagem,
        'estados': estados,
    }

    return render(request, 'senhas/editar/viagem_caledonia_editar.html', context)


@login_required
def viagem_compras_cadastrar(request):
    estados = Estado.objects.all().order_by('nome')
    form = ViagemForm()

    if request.method == 'POST':
        form = ViagemForm(request.POST)

        if form.is_valid():
            viagem = form.save()
            viagem.user = request.user
            viagem.senha = 'C'+get_random_string()+str(viagem.id)+get_random_string()
            viagem.save()

            messages.success(request, 'Viagem cadastrada com sucesso!')
            return redirect('senhas:cad_transporte')
        else:
            print('O form de viagem tem algum erro: somente compras')
            print(form.errors)

    context = {
        'form': form,
        'estados': estados,
    }
    return render(request, 'senhas/cadastros/viagem_compras_cadastrar.html', context)


@login_required
def viagem_turismo_cadastrar(request):
    estados = Estado.objects.all().order_by('nome')
    form = ViagemForm()
    form_turismo = Viagem_TurismoForm()

    if request.method == 'POST':
        print(request.POST)
        form = ViagemForm(request.POST)
        form_turismo = Viagem_TurismoForm(request.POST)

        if form.is_valid():
            if form_turismo.is_valid():
                viagem = form.save()
                viagem.user = request.user
                viagem.senha = 'T'+get_random_string()+str(viagem.id)+get_random_string()
                viagem.save()
                viagem_turismo = form_turismo.save()
                viagem_turismo.viagem = viagem
                viagem_turismo.save()

                messages.success(request, 'Viagem cadastrada com sucesso!')
                return redirect('senhas:cad_transporte')
            else:
                print('O form_turismo tem algum erro: viagem com turismo -> model viagem_turismo')
                print(form_turismo.errors)

        else:
            print('O form de viagem tem algum erro: viagem com turismo -> model viagem')
            print(form.errors)

    context = {
        'form': form,
        'form_turismo': form_turismo,
        'estados': estados,
    }
    return render(request, 'senhas/cadastros/viagem_turismo_cadastrar.html', context)


@login_required
def viagem_caledonia_cadastrar(request):
    estados = Estado.objects.all().order_by('nome')
    form = Viagem_CaledoniaForm()
    form_turismo = Viagem_turismo_CaledoniaForm()

    if request.method == 'POST':
        form = Viagem_CaledoniaForm(request.POST)
        form_turismo = Viagem_turismo_CaledoniaForm(request.POST)

        if form.is_valid():
            if form_turismo.is_valid():
                viagem = form.save()

                viagem.user = request.user
                viagem.senha = 'PC'+get_random_string()+str(viagem.id)+get_random_string()
                viagem.dt_Saida = viagem.dt_Chegada

                viagem.save()

                viagem_turismo = form_turismo.save()
                viagem_turismo.outros = 'Pico da Caledônia'
                viagem_turismo.viagem = viagem

                viagem_turismo.save()

                messages.success(request, 'Viagem cadastrada com sucesso!')
                return redirect('senhas:cad_transporte')

            else:
                print('O form_turismo tem algum erro: =/')
                print(form_turismo.errors)

        else:
            print('O form de viagem tem algum erro: =/')
            print(form.errors)

    context = {
        'form': form,
        'form_turismo': form_turismo,
        'estados': estados,
    }

    return render(request, 'senhas/cadastros/viagem_caledonia_cadastrar.html', context)


def viagem(request, senha):
    viagem = Viagem.objects.get(senha=senha)
    try:
        viagem_turismo = Viagem_Turismo.objects.get(viagem=viagem)
        pontos_turisticos = viagem_turismo.pontos_turisticos.all()
    except:
        viagem_turismo = None
        pontos_turisticos = None
    if not viagem.user == request.user:
        return redirect('senhas:cad_transporte')

    urlNames = {
        'T': 'viagem_turismo_editar',
        'C': 'viagem_compras_editar',
        'P': 'viagem_caledonia_editar',
    }
    nome_rota = 'senhas:'+urlNames[senha[0]]
    rota = redirect(nome_rota, senha)

    context = {
        'viagem': viagem,
        'rota': rota,
        'viagem_turismo': viagem_turismo,
        'pontos_turisticos': pontos_turisticos
    }

    return render(request, 'senhas/viagem.html', context)


@login_required
def excluir_viagem(request, id):
    viagem = Viagem.objects.get(senha=id)
    if request.method == 'POST':
        if viagem.user == request.user:
            viagem.ativo = False
            viagem.save()
            viagem_turismo = Viagem_Turismo.objects.get(viagem=viagem)
            viagem_turismo.ativo = False
            viagem_turismo.save()
            return redirect('senhas:cad_transporte')

    if not viagem.user == request.user:
        return redirect('senhas:cad_transporte')
    return render(request, 'senhas/excluir_senha.html', {'viagem': viagem})


@membro_fiscais_required
def fiscalizar_viagem(request, id):
    viagem = Viagem.objects.get(senha=id)
    try:
        viagem_turismo = Viagem_Turismo.objects.get(viagem=viagem)
        pontos_turisticos = viagem_turismo.pontos_turisticos.all()
    except:
        viagem_turismo = None
        pontos_turisticos = None
    return render(request, 'senhas/viagem.html', {'viagem': viagem, 'viagem_turismo': viagem_turismo, 'pontos_turisticos': pontos_turisticos})


@login_required
def cad_acesso_ponto(request):

    return render(request, 'senhas/cad_acesso_ponto.html')


def gera_senha_to_html(request, id):

    viagem = Viagem.objects.get(senha=id)
    endereco = 'https://senhas.novafriburgo.rj.gov.br/viagem/fiscalizar/' + \
        str(id)+'/22NF'
    # endereco = 'http://localhost:8000/viagem/fiscalizar/' + str(id)+'/22NF'
    try:
        viagem_turismo = Viagem_Turismo.objects.get(viagem=viagem)
    except:
        viagem_turismo = None

    pontosTuristicos_selecionados_ = []
    if viagem.senha[0] == 'T':
        tipo = 'turismo'
        viagem_turismo = Viagem_Turismo.objects.get(viagem=viagem)
        for u in viagem_turismo.pontos_turisticos.all():
            pontosTuristicos_selecionados_.append(u)
    elif viagem.senha[0] == 'C':
        tipo = 'compras'
        viagem_turismo = {}
    veiculos = Tipo_Veiculo.objects.all()

    context = {
        'viagem': viagem,
        'viagem_turismo': viagem_turismo,
        'pontos_turisticos': pontosTuristicos_selecionados_,
        'endereco': endereco}

    return render(request, 'senhas/gera_senha.html', context)


def gera_senha_to_pdf(request, id):
    try:
        url_pdf = '/home/turismo/site/turismo/senhas/static/pdf/'+id+'.pdf'
        # url_pdf='/home/eduardo/projects/turismo/senhas/static/pdf/'+id+'.pdf'
        pdfkit.from_url(
            'https://senhas.novafriburgo.rj.gov.br/gera_senha_html/'+id+'/22NF', url_pdf)
        # pdfkit.from_url('http://localhost:8000/gera_senha_html/'+id+'/22NF', url_pdf)
        context = {
            'pdf': url_pdf
        }
        try:
            return FileResponse(open(url_pdf, 'rb'), content_type='application/pdf')
        except Exception as E:
            print(E)
            raise Http404()
    except Exception as E:
        print(E)
        return redirect('senhas:cad_transporte')


def validate_data_caledonia(date):
    fail = False
    alert = ''
    viagens_caledonia_do_dia = Viagem.objects.filter(
        senha__contains='PC', ativo=True, dt_Chegada=date).count()

    if str(viagens_caledonia_do_dia) >= str(2):
        format = '%Y-%m-%d'
        dt = date
        data = datetime.strptime(dt, format)
        fail = True
        alert = 'Vagas esgotadas para visitação no dia ' + \
            str(data.strftime('%d/%m/%Y')+'. Escolha outra data.')
            
    return JsonResponse({
        'fail': fail,
        'alert': alert
    })

def get_validar_caledonia(request, date):
    if request.method == 'GET':
        return validate_data_caledonia(date)

    raise PermissionDenied()

from multiprocessing import context
from django.http import FileResponse, Http404, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from requests import request
from contas.functions import validationsViagem

from contas.views import sair
from contas.models import Estado, Cidade
from senhas.models import Tipo_Veiculo, Viagem, Viagem_Turismo
from turismo.settings import BASE_DIR
from .models import Pontos_Turisticos
from .forms import Viagem_CaledoniaForm, Viagem_turismo_CaledoniaForm, ViagemForm, Viagem_TurismoForm
from .functions import get_random_string
import time
import pickle
from datetime import date, timedelta, datetime
import pdfkit
from turismo.decorators import membro_secretaria_required, membro_fiscais_required


@login_required
def inicio(request):
    return render(request, 'senhas/index.html')


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

    form = ViagemForm(instance=viagem)
    form_turismo = Viagem_TurismoForm(instance=viagem_turismo)

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
    viagem_turismo = Viagem.objects.get(senha=senha)
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

    form = ViagemForm(instance=viagem)
    form_turismo = Viagem_TurismoForm(instance=viagem)

    print(form_turismo)
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
            print('O form de viagem tem algum erro: =/')
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
    return render(request, 'senhas/cadastros/viagem_turismo_cadastrar.html', context)


@login_required
def viagem_caledonia_cadastrar(request):
    estados = Estado.objects.all().order_by('nome')
    form = Viagem_CaledoniaForm()
    form_turismo = Viagem_turismo_CaledoniaForm()
    print(form_turismo)
    if request.method == 'POST':
        form = ViagemForm(request.POST)
        form_turismo = Viagem_CaledoniaForm(request.POST)

        if form.is_valid():
            if form_turismo.is_valid():
                try:
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
                except Exception as e:
                    print('deu ruuim', e)

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
def viagem_altera(request, id):
    validation = {'veiculo': {'state': True}, 'quant_passageiros': {'state': True},
                  'cnpj_empresa_transporte': {'state': True}, 'cadastur_empresa_transporte': {'state': True},
                  'cadastur_guia':  {'state': True}, 'telefone':  {'state': True},
                  'celular': {'state': True}, 'chegada_saida': {'state_chegada': True, 'state_saida': True, 'msg': ''},
                  'cidade': {'state': True}, 'estado': {'state': True}, 'empresa_transporte': {'state': True},
                  'nome_guia': {'state': True}, 'responsavel_viagem': {'state': True}, 'contato_responsavel': {'state': True}}
    from datetime import date
    tipo = ''
    viagem = Viagem.objects.get(senha=id)

    if date.today() > viagem.dt_Saida:
        messages.error(
            request, 'Não é mais possível alterar viagem, já que a viagem já ocorreu.')
        return redirect('/viagem/' + str(id))

    if viagem.user != request.user:
        messages.error(request, 'Viagem não percente a usuário logado.')
        return redirect('/viagem/' + str(id))

    if request.method == 'POST':
        form = ViagemForm(request.POST)
        # Aqui a VALIDATION toma novos valores de acordo com o FORM
        if viagem.senha[0] == 'T':
            tipo = 'turismo'
        validation, valido = validationsViagem(request.POST, tipo)
        if valido:
            try:
                ViagemForm
                if request.POST['ficarao_hospedados']:
                    fh = True
            except:
                fh = False
            try:
                if request.POST['restaurante_reservado']:
                    rr = True
            except:
                rr = False
            try:
                viagem.responsavel_viagem = request.POST['responsavel_viagem']
                viagem.contato_responsavel = validation['contato_responsavel']['celular']
                viagem.user = request.user
                viagem.dt_Chegada = request.POST['dt_chegada']
                viagem.dt_Saida = request.POST['dt_saida']
                viagem.ficarao_hospedados = fh
                viagem.hotel = request.POST['hotel']
                viagem.restaurante_reservado = rr
                viagem.restaurante = request.POST['restaurante']
                viagem.tipo_veiculo = Tipo_Veiculo.objects.get(
                    id=request.POST['tipo_veiculo'])
                viagem.quant_passageiros = request.POST['quant_passageiros']
                viagem.empresa_transporte = request.POST['empresa_transporte']
                viagem.cnpj_empresa_transporte = validation['cnpj_empresa_transporte']['cnpj']
                viagem.cadastur_empresa_transporte = request.POST['cadastur_empresa_transporte']
                viagem.obs = request.POST['obs']
                viagem.estado_origem = Estado.objects.get(
                    id=request.POST['estado'])
                viagem.cidade_origem = Cidade.objects.get(
                    id=request.POST['cidade'])
                viagem.save()

                if viagem.senha[0] == 'T':
                    viagem_turismo = Viagem_Turismo.objects.get(viagem=viagem)

                    viagem_turismo.outros = request.POST['outros']
                    viagem_turismo.nome_guia = request.POST['nome_guia']
                    viagem_turismo.cadastur_guia = request.POST['cadastur_guia']
                    viagem_turismo.celular = validation['celular']['celular']
                    viagem_turismo.telefone = validation['telefone']['telefone']
                    viagem_turismo.pontos_turisticos.clear()
                    viagem_turismo.save()

                    if request.POST['outros'] == '':
                        viagem_turismo.pontos_turisticos.clear()
                        for ponto in request.POST.getlist('pontos_turisticos'):
                            viagem_turismo.pontos_turisticos.add(
                                Pontos_Turisticos.objects.get(nome=ponto))
                        viagem_turismo.save()
                messages.success(request, 'Viagem alterada.')
                return redirect('senhas:cad_transporte')

            except Exception as e:
                print('e:', e)
                messages.error(request, 'Corrigir o erro apresentado.')
                # erro = str(e).split(', ')

                # print('erro:', erro)

                # if erro[0] == '(1062':
                #     messages.error(request, 'Erro: Usuário já existe.')
                # else:
                #     # Se teve erro:
                #     print('Erro: ', form.errors)
                #     erro_tmp = str(form.errors)
                #     erro_tmp = erro_tmp.replace('<ul class="errorlist">', '')
                #     erro_tmp = erro_tmp.replace('</li>', '')
                #     erro_tmp = erro_tmp.replace('<ul>', '')
                #     erro_tmp = erro_tmp.replace('</ul>', '')
                #     erro_tmp = erro_tmp.split('<li>')

                #     messages.error(request, erro_tmp[1] + ': ' + erro_tmp[2])
        else:
            messages.error(request, 'Corrigir o erro apresentado.')

    form = ViagemForm(instance=viagem)
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
    pontosTuristicos = Pontos_Turisticos.objects.filter(ativo=True)

    estado = viagem.estado_origem
    estados = Estado.objects.all().order_by('nome')
    cidade = viagem.cidade_origem
    # Incluindo as informações coletas no contexto para uso no Template
    # Estado.objects.get()
    context = {
        'form': form,
        'validation': validation,
        'viagem': viagem,
        'viagem_turismo': viagem_turismo,
        'pontos_selecionados': pontosTuristicos_selecionados_,
        'veiculos': veiculos,
        'pontos': pontosTuristicos,
        'tipo': tipo,
        'titulo': 'ALTERAR',
        'estado_': estado,
        'estados': estados,
        'cidade': cidade
    }

    return render(request, 'senhas/viagem_inclui.html', context)


@login_required
def viagem_altera_caledonia(request, id):
    validation = {'veiculo': {'state': True}, 'quant_passageiros': {'state': True},
                  'cnpj_empresa_transporte': {'state': True}, 'cadastur_empresa_transporte': {'state': True},
                  'cadastur_guia':  {'state': True}, 'telefone':  {'state': True},
                  'celular': {'state': True}, 'chegada_saida': {'state_chegada': True, 'state_saida': True, 'msg': ''},
                  'cidade': {'state': True}, 'estado': {'state': True}, 'empresa_transporte': {'state': True},
                  'nome_guia': {'state': True}, 'responsavel_viagem': {'state': True}, 'contato_responsavel': {'state': True}}
    from datetime import date
    tipo = ''
    viagem = Viagem.objects.get(senha=id)

    if date.today() > viagem.dt_Saida:
        messages.error(
            request, 'Não é mais possível alterar viagem, já que a viagem já ocorreu.')
        return redirect('/viagem/' + str(id))

    if viagem.user != request.user:
        messages.error(request, 'Viagem não percente a usuário logado.')
        return redirect('/viagem/' + str(id))

    if request.method == 'POST':
        form = ViagemForm(request.POST)
        # Aqui a VALIDATION toma novos valores de acordo com o FORM
        if viagem.senha[0] == 'T':
            tipo = 'turismo'
        validation, valido = validationsViagem(request.POST, tipo)
        if valido:
            try:
                if request.POST['ficarao_hospedados']:
                    fh = True
            except:
                fh = False
            try:
                if request.POST['restaurante_reservado']:
                    rr = True
            except:
                rr = False
            try:
                viagem.responsavel_viagem = request.POST['responsavel_viagem']
                viagem.contato_responsavel = validation['contato_responsavel']['celular']
                viagem.user = request.user
                viagem.dt_Chegada = request.POST['dt_chegada']
                viagem.dt_Saida = request.POST['dt_chegada']
                viagem.ficarao_hospedados = fh
                viagem.hotel = request.POST['hotel']
                viagem.restaurante_reservado = rr
                viagem.restaurante = request.POST['restaurante']
                viagem.tipo_veiculo = Tipo_Veiculo.objects.get(
                    id=request.POST['tipo_veiculo'])
                viagem.quant_passageiros = request.POST['quant_passageiros']
                viagem.empresa_transporte = request.POST['empresa_transporte']
                viagem.cnpj_empresa_transporte = validation['cnpj_empresa_transporte']['cnpj']
                viagem.cadastur_empresa_transporte = request.POST['cadastur_empresa_transporte']
                viagem.obs = request.POST['obs']
                viagem.estado_origem = Estado.objects.get(
                    id=request.POST['estado'])
                viagem.cidade_origem = Cidade.objects.get(
                    id=request.POST['cidade'])
                viagem.save()

                if viagem.senha[0] == 'T':
                    viagem_turismo = Viagem_Turismo.objects.get(viagem=viagem)

                    viagem_turismo.outros = 'Pico da Caledônia'
                    viagem_turismo.nome_guia = request.POST['nome_guia']
                    viagem_turismo.cadastur_guia = request.POST['cadastur_guia']
                    viagem_turismo.celular = validation['celular']['celular']
                    viagem_turismo.telefone = validation['telefone']['telefone']
                    viagem_turismo.pontos_turisticos.clear()
                    viagem_turismo.save()

                messages.success(request, 'Viagem alterada.')
                return redirect('senhas:cad_transporte')

            except Exception as e:
                print('e:', e)
                messages.error(request, 'Corrigir o erro apresentado.')
        else:
            messages.error(request, 'Corrigir o erro apresentado.')

    form = ViagemForm(instance=viagem)
    pontosTuristicos_selecionados_ = []
    if viagem.senha[0] == 'P':
        tipo = 'turismo'
        viagem_turismo = Viagem_Turismo.objects.get(viagem=viagem)
        for u in viagem_turismo.pontos_turisticos.all():
            pontosTuristicos_selecionados_.append(u)
    elif viagem.senha[0] == 'C':
        tipo = 'compras'
        viagem_turismo = {}
    veiculos = Tipo_Veiculo.objects.all()
    pontosTuristicos = Pontos_Turisticos.objects.filter(ativo=True)

    estado = viagem.estado_origem
    estados = Estado.objects.all().order_by('nome')
    cidade = viagem.cidade_origem
    # Incluindo as informações coletas no contexto para uso no Template
    # Estado.objects.get()
    context = {
        'form': form,
        'validation': validation,
        'viagem': viagem,
        'viagem_turismo': viagem_turismo,
        'pontos_selecionados': pontosTuristicos_selecionados_,
        'veiculos': veiculos,
        'pontos': pontosTuristicos,
        'tipo': tipo,
        'titulo': 'ALTERAR',
        'estado_': estado,
        'estados': estados,
        'cidade': cidade
    }

    return render(request, 'senhas/cadastros/caledonia.html', context)


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

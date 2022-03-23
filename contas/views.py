import requests
import json
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm, PasswordResetForm
from django.contrib import messages
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse

from django.contrib.auth.models import User

from contas.forms import CadastrarForm, CadastroForm
from contas.functions import validations, validarAlteraçãoUsuario
from contas.models import Cidade, Usuario, Estado
from senhas.templatetags.template_filters import formata_cpf
from turismo.settings import hCAPTCHA_PUBLIC_KEY, hCAPTCHA_PRIVATE_KEY
# Create your views here.

def cadastrar(request):
    if request.user.is_authenticated:
        return redirect('/')
    #Iniciamos a variavel VALIDATION aqui com todos os STATE como True.
    #Quando submetido o formulario, o que estiver incorreto muda seu STATE para False.
    validation={'nome': {'state': True},'cpf': {'state': True},'email': {'state': True}, 
                'celular': {'state': True}, 'telefone': {'state': True}, 'senha': {'state': True},
                'cidade':{'state': True}, 'estado':{'state': True}}

    #Busca-se todos os estados para uso no Template.
    estados = Estado.objects.all().order_by('nome')

    if request.method == 'POST':        
        #Retoma as informações do formulario do cliente e preenche nosso objeto
        #para realização da validação dos campos
        form = CadastrarForm(request.POST)

        #Essa validação é para retornar ao Frontend e notificar o usuário
        validation, valido=validations(request.POST)

        #Abaixo recebemos a validação da API do Google do reCAPTCHA
        ''' Begin reCAPTCHA validation '''
        recaptcha_response = request.POST.get('h-captcha-response')
        data = {
            'secret': hCAPTCHA_PRIVATE_KEY,
            'response': recaptcha_response
        }
        r = requests.post('https://hcaptcha.com/siteverify', data=data)
        result = r.json()
        ''' End reCAPTCHA validation '''

        #Se o reCAPTCHA garantir que o usuário é um robô
        print(result)
        if result['success']:
            #Se o formulario estiver com as informações preenchidas corretamente
            if form.is_valid():
                cidade = Cidade.objects.get(id=request.POST.get('cidade'))
                try:
                    user = User.objects.create_user(request.POST['email'], request.POST['email'], request.POST['senha'])

                    # Atualiza os campos de USER
                    user.first_name = request.POST['nome']
                    user.last_name = request.POST['nome']
                    user.save()

                    # Atualiza os campos de USUARIO
                    usuario = Usuario(
                        user=user,
                        cpf=form.cleaned_data['cpf'],
                        # cadastur=form.cleaned_data['cadastur'],
                        celular=form.cleaned_data['celular'],
                        telefone=form.cleaned_data['telefone'],
                        cidade=cidade,
                    )
                    usuario.save()

                    messages.success(request, 'Cadastro criado.')
                    return redirect('/')

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
                #Abaixo resgatamos as informações do formulario e amarzenamos
                #na devida variavel para uso no Template
                try:
                    estado=Estado.objects.get(id=request.POST['estado'])
                except:
                    estado=''
                try:
                    cidade=Cidade.objects.get(id=request.POST['cidade'])
                except:
                    cidade=''
                estados = Estado.objects.all().order_by('nome')
                context={
                    'form': form,
                    'validations': validation,
                    'nome':request.POST['nome'],
                    'cpf': request.POST['cpf'],
                    'email':request.POST['email'],
                    'celular':request.POST['celular'],
                    'telefone':request.POST['telefone'],
                    'estado_':estado,
                    'cidade': cidade,
                    'estados': estados,
                    'hCAPTCHA': hCAPTCHA_PUBLIC_KEY
                }
                return render(request, 'contas/cadastrar.html', context)
        else:
            validation={'nome': {'state': True},'cpf': {'state': True},'email': {'state': True}, 
                        'celular': {'state': True}, 'telefone': {'state': True}, 'senha': {'state': True},
                        'cidade':{'state': True}, 'estado':{'state': True}}

            messages.error(request, 'Corrigir o erro apresentado.')
                
            try:
                estado=Estado.objects.get(id=request.POST['estado'])
            except:
                estado=''
            try:
                cidade=Cidade.objects.get(id=request.POST['cidade'])
            except:
                cidade=''
                estados = Estado.objects.all().order_by('nome')
                context={
                    'form': form,
                    'robo': True,
                    'validations': validation,
                    'nome':request.POST['nome'],
                    'cpf': request.POST['cpf'],
                    'email':request.POST['email'],
                    'celular':request.POST['celular'],
                    'telefone':request.POST['telefone'],
                    'estado_':estado,
                    'cidade': cidade,
                    'estados': estados,
                    'hCAPTCHA': hCAPTCHA_PUBLIC_KEY
                }
                return render(request, 'contas/cadastrar.html', context)
    
    else:                
        form = CadastrarForm()          
    return render(request, 'contas/cadastrar.html', { 'hCAPTCHA': hCAPTCHA_PUBLIC_KEY,'form': form, 'estados': estados, 'validations': validation })


@login_required
def cadastro(request):
    #Recupera as informações do usuário para preenchimento do Template
    user = request.user    
    usuario = Usuario.objects.get(user=user)
    
    if request.method == 'POST':
        #Valida os dados preenchidos no formulario pelo cliente
        validations,valido=validarAlteraçãoUsuario(request.POST)
        
        if valido:
            cidade = Cidade.objects.get(id=request.POST.get('cidade'))
            try:
                user.username =request.POST['email']
                user.email = request.POST['email']
                user.first_name = request.POST['nome']
                usuario.cpf = validations['cpf']['cpf']
                user.email = request.POST['email']
                usuario.celular = validations['celular']['celular']
                usuario.telefone = validations['telefone']['telefone']              
                usuario.cidade= cidade
                user.save()
                usuario.save()
                messages.success(request, 'Cadastro alterado.')
                #Se bem sucedido, redireciona para o Index
                return redirect('/')

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
        
        form = CadastroForm(instance=usuario)
    context={
        'email': user.email,
        'nome': user.first_name,        
        'cpf': usuario.cpf,
        'celular': usuario.celular,
        'telefone': usuario.telefone,
        'estados': Estado.objects.all(),
        'cidades': Cidade.objects.filter(estado=Estado.objects.get(nome=usuario.cidade.estado)),
        'estado_': usuario.cidade.estado,
        'cidade': usuario.cidade
    }
    return render(request, 'contas/cadastro.html', context)
    # return render(request, 'contas/cadastro.html', { 'form': form })


#Essa View retorna a cidade nos formularios do cliente
#ao selecionarem o estado
def load_cidades(request):    
    if not request.GET.get('id'):        
        return render(request, 'contas/ret_cidades.html', {})
    estado_id = request.GET.get('id')
    cidades = Cidade.objects.filter(estado = estado_id).order_by('nome')
    return render(request, 'contas/ret_cidades.html', {'cidades' : cidades})

#Essa View não é mais utilizada
def load_estados(request):   
    estados = Estado.objects.all().order_by('nome')
    return render(request, 'contas/ret_estado.html', {'estados' : estados})



@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Importante!
            messages.success(request, 'Senha alterada.')
            return redirect('contas:change_password')
        else:
            messages.error(request, 'Você deve cumprir todos os requisitos para alterar sua senha.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'registration/change_password.html', { 'form': form })


def password_reset_request(request):
	if request.method == "POST":
		password_reset_form = PasswordResetForm(request.POST)
		if password_reset_form.is_valid():
			data = password_reset_form.cleaned_data['email']
			associated_users = User.objects.filter(email=data)
			if associated_users.exists():
				for user in associated_users:
					subject = "Alteração de Senha do Sistema de Senhas da Secretária Municipal de Turismo de Nova Friburgo"
					email_template_name = "registration/password_reset_email.txt"
					c = {
					"email":user.email,
					'domain':'127.0.0.1:8000',
					'site_name': 'Website',
					"uid": urlsafe_base64_encode(force_bytes(user.pk)),
					"user": user,
					'token': default_token_generator.make_token(user),
					'protocol': 'http',
					}
					email = render_to_string(email_template_name, c)
					try:
						send_mail(subject, email, user.email, [user.email], fail_silently=False)
					except BadHeaderError:
						return HttpResponse('Invalid header found.')
					return redirect ("password_reset_done")
	password_reset_form = PasswordResetForm()
	return render(request=request, template_name="registration/password_reset.html", context={"password_reset_form":password_reset_form})


@login_required
def sair(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('/accounts/logout')
    else:
        return redirect('/accounts/login')

def login_view(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        #Abaixo recebemos a validação da API do hCAPTCHA
        ''' Begin hCAPTCHA validation '''
        recaptcha_response = request.POST.get('h-captcha-response')
        data = {            
            'secret': hCAPTCHA_PRIVATE_KEY,
            'response': recaptcha_response
        }
        r = requests.post('https://hcaptcha.com/siteverify', data=data)
        result = r.json()
        ''' End hCAPTCHA validation '''
        print(result)
        #Se o hCAPTCHA garantir que o usuário é um robô
        if result['success']:
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')
            else:                
                context={
                    'error': True,
                    'hCAPTCHA': hCAPTCHA_PUBLIC_KEY
                }
                return render(request, 'registration/login.html', context)
        else:
            context={
                'error2': True,            
                'hCAPTCHA': hCAPTCHA_PUBLIC_KEY
            }
            return render(request, 'registration/login.html', context)
    context={
        'hCAPTCHA': hCAPTCHA_PUBLIC_KEY
    }
    return render(request, 'registration/login.html', context)

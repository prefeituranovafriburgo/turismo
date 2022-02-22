from django.shortcuts import render, redirect

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
from contas.functions import validations
from contas.models import Cidade, Usuario, Estado
from senhas.templatetags.template_filters import formata_cpf

# Create your views here.

def cadastrar(request):
    validation={'nome': {'state': True},'cpf': {'state': True},'email': {'state': True}, 
                'celular': {'state': True}, 'telefone': {'state': True}, 'senha': {'state': True}}
    estados = Estado.objects.all().order_by('nome')
    if request.method == 'POST':        
        form = CadastrarForm(request.POST)
        validation=validations(request.POST)
        if form.is_valid():
            cidade = Cidade.objects.get(id=request.POST.get('cidade'))
            try:
                user = User.objects.create_user(request.POST.get('email'), request.POST.get('email'), request.POST.get('senha'))

                # Update fields and then save again
                user.first_name = request.POST.get('nome')
#                user.last_name = request.POST.get('nome')
                user.save()

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
            
            try:
                estado=Estado.objects.get(id=request.POST['estado'])
            except:
                estado=''
            try:
                cidade=Cidade.objects.get(id=request.POST['cidade'])
            except:
                cidade=''
            print(estado, cidade)
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
                'estados': estados
            }
            print('teste')
            return render(request, 'contas/cadastrar.html', context)
    else:        
        form = CadastrarForm()
    estados=Estado.objects.all()           
    return render(request, 'contas/cadastrar.html', { 'form': form, 'estados': estados, 'validations': validation })



def cadastro(request):

    user = request.user    
    usuario = Usuario.objects.get(user=user)

    if request.method == 'POST':
        form = CadastroForm(request.POST, instance=usuario)

        if form.is_valid():
            cidade = Cidade.objects.get(id=request.POST.get('cidade'))

            try:
                user.username = form.cleaned_data['email']
                user.email = form.cleaned_data['email']
                user.first_name = form.cleaned_data['nome']
                user.save()

                form.save()

                messages.success(request, 'Cadastro alterado.')
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

#         form.fields['email'].initial = user.email
#         form.fields['nome'].initial = user.first_name
#         form.fields['estado'].initial = usuario.cidade.estado
#         form.fields['cidade'].initial = usuario.cidade
# #        form.fields['cpf_aux'].initial = formata_cpf(usuario.cpf)
#         print('cpf:', form.fields['cpf'].initial)
#         form.fields['celular'].initial = usuario.celular
#         form.fields['telefone'].initial = usuario.telefone
    """
    context={
        'email': user.email,
        'nome': user.first_name,
        'cadastur': usuario.cadastur,
        'cpf': usuario.cpf,
        'celular': usuario.celular,
        'telefone': usuario.telefone,
        'estado': usuario.cidade.estado,
        'cidade': usuario.cidade
    }
    return render(request, 'contas/cadastro2.html', context)
    """

    return render(request, 'contas/cadastro.html', { 'form': form })



def load_cidades(request):    
    if not request.GET.get('id'):
        
        return render(request, 'contas/ret_cidades.html', {})

    estado_id = request.GET.get('id')
    cidades = Cidade.objects.filter(estado = estado_id).order_by('nome')


    return render(request, 'contas/ret_cidades.html', {'cidades' : cidades})

def load_estados(request):   
    estados = Estado.objects.all().order_by('nome')
    return render(request, 'contas/ret_estado.html', {'estados' : estados})



@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Senha alterada.')
            return redirect('contas:change_password')
        else:
            messages.error(request, 'Corrigir o erro apresentado.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'registration/change_password.html', { 'form': form })


def password_reset_request(request):
	if request.method == "POST":
		password_reset_form = PasswordResetForm(request.POST)
		if password_reset_form.is_valid():
			data = password_reset_form.cleaned_data['email']
			associated_users = User.objects.filter(Q(email=data))
			if associated_users.exists():
				for user in associated_users:
					subject = "Password Reset Requested"
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
						send_mail(subject, email, 'admin@example.com' , [user.email], fail_silently=False)
					except BadHeaderError:
						return HttpResponse('Invalid header found.')
					return redirect ("/password_reset/done/")
	password_reset_form = PasswordResetForm()
	return render(request=request, template_name="registration/password_reset.html", context={"password_reset_form":password_reset_form})


@login_required
def sair(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('/accounts/logout')
    else:
        return redirect('/accounts/login')

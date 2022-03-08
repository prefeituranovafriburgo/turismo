from http.client import OK
from multiprocessing import context
from django.shortcuts import render
from guias.models import Categoria, Guias_Turismo, Idiomas, Segmento_Atuacao
from .validations import validar_cadastro_guia
# Create your views here.
def index(request):
    guias=Guias_Turismo.objects.all()
    context={
        'guias': guias,
        'fotos': ['01', '02']
    }
    return render(request, 'guias/index.html', context)

def mapa_turistico(request):    
    return render(request, 'guias/mapa-turistico.html')

def cadastrar(request):    

    if request.method == 'POST':
        valido, validation=validar_cadastro_guia(request.POST)
        print('opcao', valido)
        if valido:
            print('ok')    
        else:
            form={
                'nome': request.POST['nome'],
                'cadastur': request.POST['cadastur'],
                'validade': request.POST['validade'],
                'telefone': request.POST['telefone'],
                'email': request.POST['email'],
            }
    else:
        form=''
        validation=''        
    
    categorias = Categoria.objects.all()
    segmentos = Segmento_Atuacao.objects.all()
    idiomas = Idiomas.objects.all()

    context={
    'segmentos': segmentos,
    'categorias': categorias,
    'idiomas': idiomas,
    'validation': validation,
    'form': form
    }
    return render(request, 'guias/cadastrar_guia.html', context)
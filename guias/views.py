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
            form=''  
            try:
                guia=Guias_Turismo(
                                    nome=request.POST['nome'], 
                                    cadastur=request.POST['cadastur'], 
                                    validade_cadastur=request.POST['validade'], 
                                    telefone=request.POST['telefone'], 
                                    email=request.POST['email'],
                                    instagram=request.POST['instagram'],
                                    facebook=request.POST['facebook'],
                                    site=request.POST['site'],
                                  )
                guia.save()
                for categoria in request.POST.getlist('categorias'):
                    guia.categoria.add(Categoria.objects.get(nome=categoria))
                for segmento in request.POST.getlist('segmentos'):
                    guia.segmento_de_atuacao.add(Segmento_Atuacao.objects.get(nome=segmento))
                for idioma in request.POST.getlist('idiomas'):
                    guia.idiomas.add(Idiomas.objects.get(nome=idioma))
                guia.save()    
            except Exception as E:
                if str(E)=='UNIQUE constraint failed: guias_guias_turismo.cadastur':
                    form={
                    'nome': request.POST['nome'],
                    'cadastur': request.POST['cadastur'],
                    'validade': request.POST['validade'],
                    'telefone': request.POST['telefone'],
                    'email': request.POST['email'],
                    }
                    validation={'cadastur': {'state':True, 'msg': 'Cadastur já cadastrado.'}}
                else:
                    print(E)
            
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
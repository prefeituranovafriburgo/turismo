from urllib import request
from django.shortcuts import render
from .models import ProblemasRelatados

def receberProblema(request):
    if request.method == 'POST':
        try:
            problema=ProblemasRelatados(user=request.user,
                                        local=request.POST['local'],
                                        descricao=request.POST['detalhe'],
                                        ativo=True)
            problema.save()
            return render(request, 'report/success.html')
        except Exception as E:
            print(E)
        
    return render(request, 'report/index.html')

def verProblemasRelatados(request):
    problemas=ProblemasRelatados.objects.all()
    context={
        'problemas': problemas
    }
    return render(request, 'report/verProblemas.html', context)
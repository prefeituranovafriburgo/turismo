from urllib import request
from django.shortcuts import render
from .models import ProblemasRelatados
from django.contrib.auth.decorators import login_required
from turismo.decorators import membro_secretaria_required, membro_fiscais_required
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

@login_required
@membro_fiscais_required
def verProblemasRelatados(request):    

    problemas=ProblemasRelatados.objects.all()
    context={
        'problemas': problemas
    }
    return render(request, 'report/verProblemas.html', context)
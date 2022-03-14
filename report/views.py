from urllib import request
from django.shortcuts import render

def receberProblema(request):
    if request.method == 'POST':
        print('\nOnde foi detectado o problema:',request.POST['local'])
        print('Relato do problema:',request.POST['detalhe'],'\n')
        return render(request, 'report/success.html')
    return render(request, 'report/index.html')
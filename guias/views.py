from django.shortcuts import render
from guias.models import Guias_Turismo
# Create your views here.
def index(request):
    guias=Guias_Turismo.objects.all()
    context={
        'guias': guias,
    }
    return render(request, 'guias/index.html', context)
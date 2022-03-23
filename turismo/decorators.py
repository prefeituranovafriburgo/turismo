from django.http import HttpResponseRedirect
from django.core.exceptions import PermissionDenied
from django.urls import reverse
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.models import Group

from django.http import HttpResponseForbidden

def membro_secretaria_required(view_func):    
    def wrap(request, *args, **kwargs):
        if  Group.objects.get(name='Secretaria de Turismo') in request.user.groups.all() or request.user.is_superuser:
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponseForbidden()
    return wrap
    
def membro_fiscais_required(view_func):    
    def wrap(request, *args, **kwargs):
        if  Group.objects.get(name='Fiscais') in request.user.groups.all() or request.user.is_superuser:
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponseForbidden()
    return wrap
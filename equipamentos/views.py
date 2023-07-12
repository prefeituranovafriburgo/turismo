# ===========================
# Instruções
# Para instalar QR Code, usar: pip install django-qr-code
# https://django-qr-code.readthedocs.io/en/latest/pages/README.html


from django.shortcuts import render
from .models import *
from django.contrib.auth.decorators import login_required
# from django.shortcuts import render
# from qr_code.qrcode.utils import QRCodeOptions
@login_required
def inicio(request):
    return render(request, 'inicio.html')
@login_required
def equipamento(request, id):
   
    equipamento = Equipamento.objects.get(id=id)

    # Trata UUID
    sessao = request.session.get("sessao", '')

    if sessao == '':
        import uuid
        sessao = str(uuid.uuid4().hex)
        request.session["sessao"] = sessao

    grava_log(sessao, equipamento)

    ver_tambem = Equipamento.objects.filter(tipo_equipamento=equipamento.tipo_equipamento).exclude(id=equipamento.id)

    return render(request, 'equipamento.html', { 'equipamento': equipamento, 'ver_tambem': ver_tambem })

@login_required
def grava_log(sessao, equipamento):

    visitante = Visitante(uuid=sessao, equipamento=equipamento)
    visitante.save()

    return

@login_required
def tipos(request):
    tipos = Tipo_Equipamento.objects.all()
    return render(request, 'tipos.html', { 'tipos': tipos })


@login_required
def equipamentos(request, id):
    equipamentos = Equipamento.objects.filter(tipo_equipamento=id)
    return render(request, 'equipamentos.html', { 'equipamentos': equipamentos })



def mostra_qrcode(request, id):

    equipamento = Equipamento.objects.get(id=id)

    endereco = 'https://turismo.jlb.net.br/equipamentos/equipamento/' + str(id)

    return render(request, 'mostra_qrcode.html', {'endereco': endereco, 'equipamento': equipamento})


@login_required
def estatisticas(request):

    total_visitantes = Visitante.objects.count()

    visitantes = Visitante.objects.all().order_by('equipamento__tipo_equipamento').order_by('equipamento__nome')

    total = []

    total_por_visitante = 0

    visitante_ant = visitantes[0]

    for visitante in visitantes:

        if not visitante.equipamento == visitante_ant.equipamento:
            visitante_aux = { 'nome': visitante_ant.equipamento.nome, 'total_por_visitante': total_por_visitante }
            total.append(visitante_aux)
            total_por_visitante = 0
            visitante_ant = visitante

        total_por_visitante = total_por_visitante + 1

    visitante_aux = { 'nome': visitante_ant.equipamento.nome, 'total_por_visitante': total_por_visitante }
    total.append(visitante_aux)

    return render(request, 'estatisticas.html', { 'total_visitantes': total_visitantes, 'total': total })

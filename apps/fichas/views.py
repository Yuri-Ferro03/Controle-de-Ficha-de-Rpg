from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.db.models import Q
from .models import Monstro, NPC
from .forms import NPCForm, MonstroForm
import requests

@require_http_methods(["GET", "POST"])
def registro(request):
    """View para registro de novos usuários"""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Conta criada com sucesso! Você já pode fazer login.')
            return redirect('accounts:login')
    else:
        form = UserCreationForm()
    return render(request, 'fichas/registro.html', {'form': form})

@login_required
def monstro_list(request):
    monstros = Monstro.objects.all()
    return render(request, 'fichas/monstro_list.html', {'monstros': monstros})
@login_required
def monstro_detail(request, pk):
    monstro = get_object_or_404(Monstro, pk=pk)
    return render(request, 'fichas/monstro_detail.html', {'monstro': monstro})
@login_required
def npc_create(request):
    if request.method == 'POST':
        form = NPCForm(request.POST, request.FILES)
        if form.is_valid():
            npc = form.save(commit=False)
            npc.criado_por = request.user
            npc.save()
            messages.success(request, 'NPC salvo com sucesso!')
            return redirect('fichas:monstro_list')
    else:
        form = NPCForm()
    return render(request, 'fichas/npc_create.html', {'form': form})

def home(request):
    recent_npcs = NPC.objects.all().order_by('-criado_em')[:6]
    recent_monstros = Monstro.objects.all().order_by('-criado_em')[:6]
    context = {
        'recent_npcs': recent_npcs,
        'recent_monstros': recent_monstros,
    }
    return render(request, 'fichas/home.html', context)

def lista_npcs(request):
    npcs = NPC.objects.all().order_by('nome')
    
    busca = request.GET.get('busca', '')
    if busca:
        npcs = npcs.filter(Q(nome__icontains=busca))
    
    context = {
        'npcs': npcs,
        'busca': busca
    }
    return render(request, 'fichas/lista_npcs.html', context)

def detalhe_npc(request, id):
    npc = get_object_or_404(NPC, id=id)
    context = {'npc': npc}
    return render(request, 'fichas/detalhe_npc.html', context)

def lista_monstros(request):
    monstros = Monstro.objects.all().order_by('nome')
    
    busca = request.GET.get('busca', '')
    if busca:
        monstros = monstros.filter(Q(nome__icontains=busca) | Q(tipo__icontains=busca))
    
    context = {
        'monstros': monstros,
        'busca': busca
    }
    return render(request, 'fichas/lista_monstros.html', context)

def detalhe_monstro(request, id):
    monstro = get_object_or_404(Monstro, id=id)
    context = {'monstro': monstro}
    return render(request, 'fichas/detalhe_monstro.html', context)

@login_required
def criar_npc(request):
    if request.method == 'POST':
        form = NPCForm(request.POST, request.FILES)
        if form.is_valid():
            npc = form.save(commit=False)
            npc.criado_por = request.user
            npc.save()
            messages.success(request, 'NPC criado com sucesso!')
            return redirect('fichas:detalhe_npc', id=npc.id)
    else:
        form = NPCForm()
    
    context = {'form': form}
    return render(request, 'fichas/criar_npc.html', context)

@login_required
def criar_monstro(request):
    if request.method == 'POST':
        form = MonstroForm(request.POST, request.FILES)
        if form.is_valid():
            monstro = form.save()
            messages.success(request, 'Monstro criado com sucesso!')
            return redirect('fichas:detalhe_monstro', id=monstro.id)
    else:
        form = MonstroForm()
    
    context = {'form': form}
    return render(request, 'fichas/criar_monstro.html', context)

@login_required
def editar_npc(request, id):
    npc = get_object_or_404(NPC, id=id)
    
    # Apenas o criador pode editar
    if npc.criado_por != request.user and not request.user.is_staff:
        messages.error(request, 'Você não tem permissão para editar este NPC.')
        return redirect('fichas:detalhe_npc', id=npc.id)
    
    if request.method == 'POST':
        form = NPCForm(request.POST, request.FILES, instance=npc)
        if form.is_valid():
            form.save()
            messages.success(request, 'NPC atualizado com sucesso!')
            return redirect('fichas:detalhe_npc', id=npc.id)
    else:
        form = NPCForm(instance=npc)
    
    context = {'form': form, 'npc': npc}
    return render(request, 'fichas/editar_npc.html', context)

@login_required
def editar_monstro(request, id):
    monstro = get_object_or_404(Monstro, id=id)
    
    if request.method == 'POST':
        form = MonstroForm(request.POST, request.FILES, instance=monstro)
        if form.is_valid():
            form.save()
            messages.success(request, 'Monstro atualizado com sucesso!')
            return redirect('fichas:detalhe_monstro', id=monstro.id)
    else:
        form = MonstroForm(instance=monstro)
    
    context = {'form': form, 'monstro': monstro}
    return render(request, 'fichas/editar_monstro.html', context)

@login_required
def deletar_npc(request, id):
    npc = get_object_or_404(NPC, id=id)
    
    # Apenas o criador ou admin pode deletar
    if npc.criado_por != request.user and not request.user.is_staff:
        messages.error(request, 'Você não tem permissão para deletar este NPC.')
        return redirect('fichas:detalhe_npc', id=npc.id)
    
    if request.method == 'POST':
        npc.delete()
        messages.success(request, 'NPC deletado com sucesso!')
        return redirect('fichas:lista_npcs')
    
    context = {'npc': npc}
    return render(request, 'fichas/deletar_npc.html', context)

@login_required
def deletar_monstro(request, id):
    monstro = get_object_or_404(Monstro, id=id)
    
    if request.method == 'POST':
        monstro.delete()
        messages.success(request, 'Monstro deletado com sucesso!')
        return redirect('fichas:lista_monstros')
    
    context = {'monstro': monstro}
    return render(request, 'fichas/deletar_monstro.html', context)

def logout(request):
    """View para logout do usuário"""
    from django.contrib.auth import logout
    logout(request)
    messages.info(request, 'Você saiu da sua conta.')
    return redirect('fichas:home')
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.db.models import Q
from django.urls import reverse
from .models import Monstro, NPC, InitiativeSession, InitiativeParticipant
from .forms import NPCForm, MonstroForm, InitiativeSessionForm, InitiativeParticipantForm
import requests


TRACKER_SESSION_KEY = "initiative_tracker"

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
    tracker = _get_initiative_tracker(request)
    context = {
        'recent_npcs': recent_npcs,
        'recent_monstros': recent_monstros,
        'initiative_tracker': tracker,
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
    return render(request, 'fichas/npcs/lista_npcs.html', context)

def detalhe_npc(request, id):
    npc = get_object_or_404(NPC, id=id)
    context = {'npc': npc}
    return render(request, 'fichas/npcs/detalhe_npc.html', context)

def lista_monstros(request):
    monstros = Monstro.objects.all().order_by('nome')
    
    busca = request.GET.get('busca', '')
    if busca:
        monstros = monstros.filter(Q(nome__icontains=busca) | Q(tipo__icontains=busca))
    
    context = {
        'monstros': monstros,
        'busca': busca
    }
    return render(request, 'fichas/monstros/lista_monstros.html', context)

def detalhe_monstro(request, id):
    monstro = get_object_or_404(Monstro, id=id)
    context = {'monstro': monstro}
    return render(request, 'fichas/monstros/detalhe_monstro.html', context)

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
    return render(request, 'fichas/npcs/criar_npc.html', context)

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
    return render(request, 'fichas/monstros/criar_monstro.html', context)

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
    return render(request, 'fichas/npcs/editar_npc.html', context)

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
    return render(request, 'fichas/monstros/editar_monstro.html', context)

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
    return render(request, 'fichas/npcs/deletar_npc.html', context)

@login_required
def deletar_monstro(request, id):
    monstro = get_object_or_404(Monstro, id=id)
    
    if request.method == 'POST':
        monstro.delete()
        messages.success(request, 'Monstro deletado com sucesso!')
        return redirect('fichas:lista_monstros')
    
    context = {'monstro': monstro}
    return render(request, 'fichas/monstros/deletar_monstro.html', context)

def logout(request):
    """View para logout do usuário"""
    from django.contrib.auth import logout
    logout(request)
    messages.info(request, 'Você saiu da sua conta.')
    return redirect('fichas:home')


def _get_initiative_tracker(request):
    tracker = request.session.get(TRACKER_SESSION_KEY)
    if not tracker:
        tracker = {"participants": [], "current_index": 0, "next_id": 1}
        request.session[TRACKER_SESSION_KEY] = tracker
    return tracker


@login_required
def perfil(request):
    return perfil_usuario(request, request.user.username)


@login_required
def perfil_usuario(request, username):
    profile_user = get_object_or_404(User, username=username)
    is_owner = profile_user == request.user
    npcs = NPC.objects.filter(criado_por=profile_user).order_by('-criado_em')
    context = {
        "profile_user": profile_user,
        "is_owner": is_owner,
        "npcs": npcs,
    }
    return render(request, 'fichas/profile.html', context)


@login_required
def iniciativa_list(request):
    sessions = InitiativeSession.objects.filter(owner=request.user).order_by('-criado_em')
    context = {"sessions": sessions}
    return render(request, 'fichas/iniciativa_list.html', context)


@login_required
@require_http_methods(["GET", "POST"])
def iniciativa_create(request):
    if request.method == 'POST':
        form = InitiativeSessionForm(request.POST)
        if form.is_valid():
            session = form.save(commit=False)
            session.owner = request.user
            session.save()
            messages.success(request, 'Sessão de iniciativa criada com sucesso.')
            return redirect('fichas:iniciativa_detail', session_id=session.id)
    else:
        form = InitiativeSessionForm()
    context = {"form": form}
    return render(request, 'fichas/iniciativa_create.html', context)


@login_required
def iniciativa_detail(request, session_id):
    session = get_object_or_404(InitiativeSession, id=session_id, owner=request.user)
    participants = session.participants.all()
    context = {
        "session": session,
        "participants": participants,
    }
    return render(request, 'fichas/iniciativa_detail.html', context)


@login_required
@require_http_methods(["POST"])
def iniciativa_add_participant(request, session_id):
    session = get_object_or_404(InitiativeSession, id=session_id, owner=request.user)
    form = InitiativeParticipantForm(request.POST)
    if form.is_valid():
        participant = form.save(commit=False)
        participant.session = session
        participant.save()
        messages.success(request, 'Participante adicionado à iniciativa.')
    return redirect('fichas:iniciativa_detail', session_id=session.id)


@login_required
@require_http_methods(["POST"])
def iniciativa_next(request, session_id):
    session = get_object_or_404(InitiativeSession, id=session_id, owner=request.user)
    count = session.participant_count()
    if count:
        session.current_index = (session.current_index + 1) % count
        session.save(update_fields=["current_index"])
    return redirect('fichas:iniciativa_detail', session_id=session.id)


@login_required
@require_http_methods(["POST"])
def iniciativa_prev(request, session_id):
    session = get_object_or_404(InitiativeSession, id=session_id, owner=request.user)
    count = session.participant_count()
    if count:
        session.current_index = (session.current_index - 1) % count
        session.save(update_fields=["current_index"])
    return redirect('fichas:iniciativa_detail', session_id=session.id)


@login_required
@require_http_methods(["POST"])
def iniciativa_simple_add(request):
    tracker = _get_initiative_tracker(request)
    name = request.POST.get('name', '').strip()
    initiative_raw = request.POST.get('initiative', '0')
    try:
        initiative = int(initiative_raw)
    except (TypeError, ValueError):
        initiative = 0
    if name:
        next_id = tracker.get('next_id', 1)
        participants = tracker.get('participants', [])
        participants.append({"id": next_id, "name": name, "initiative": initiative})
        participants.sort(key=lambda p: (-p.get('initiative', 0), p.get('id', 0)))
        tracker['participants'] = participants
        tracker['next_id'] = next_id + 1
        if tracker.get('current_index', 0) >= len(participants):
            tracker['current_index'] = 0
        request.session[TRACKER_SESSION_KEY] = tracker
    home_url = reverse('fichas:home') + '?initiative=open'
    return redirect(home_url)


@login_required
@require_http_methods(["POST"])
def iniciativa_simple_remove(request):
    tracker = _get_initiative_tracker(request)
    pid_raw = request.POST.get('pid')
    try:
        pid = int(pid_raw)
    except (TypeError, ValueError):
        pid = None
    participants = tracker.get('participants', [])
    if pid is not None:
        participants = [p for p in participants if p.get('id') != pid]
        tracker['participants'] = participants
        if participants:
            current_index = tracker.get('current_index', 0)
            if current_index >= len(participants):
                tracker['current_index'] = 0
        else:
            tracker['current_index'] = 0
    request.session[TRACKER_SESSION_KEY] = tracker
    home_url = reverse('fichas:home') + '?initiative=open'
    return redirect(home_url)


@login_required
@require_http_methods(["POST"])
def iniciativa_simple_next(request):
    tracker = _get_initiative_tracker(request)
    participants = tracker.get('participants', [])
    if participants:
        current_index = tracker.get('current_index', 0)
        current_index = (current_index + 1) % len(participants)
        tracker['current_index'] = current_index
        request.session[TRACKER_SESSION_KEY] = tracker
    home_url = reverse('fichas:home') + '?initiative=open'
    return redirect(home_url)


@login_required
@require_http_methods(["POST"])
def iniciativa_simple_prev(request):
    tracker = _get_initiative_tracker(request)
    participants = tracker.get('participants', [])
    if participants:
        current_index = tracker.get('current_index', 0)
        current_index = (current_index - 1) % len(participants)
        tracker['current_index'] = current_index
        request.session[TRACKER_SESSION_KEY] = tracker
    home_url = reverse('fichas:home') + '?initiative=open'
    return redirect(home_url)


@login_required
@require_http_methods(["POST"])
def iniciativa_simple_clear(request):
    tracker = {"participants": [], "current_index": 0, "next_id": 1}
    request.session[TRACKER_SESSION_KEY] = tracker
    home_url = reverse('fichas:home') + '?initiative=open'
    return redirect(home_url)
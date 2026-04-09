import json

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Prefetch
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST
from django.views.generic import CreateView, ListView, UpdateView

from .models import Group, Sectors, WorkStation


@login_required
def index(request):
    return render(request, "rule/index.html")


# views dos Grupos
class GrupoListView(LoginRequiredMixin, ListView):
    model = Group
    template_name = "rule/group/group_list.html"
    context_object_name = "grupos"


class GroupCreateView(LoginRequiredMixin, CreateView):
    model = Group
    template_name = "rule/group/group_form.html"
    fields = "__all__"
    success_url = reverse_lazy("rule:grupos_list")


class GrupoUpdateView(LoginRequiredMixin, UpdateView):
    model = Group
    template_name = "rule/group/group_form.html"
    fields = "__all__"
    success_url = reverse_lazy("rule:grupos_list")


# views do Setor
class SetorListView(LoginRequiredMixin, ListView):
    template_name = "rule/sector/sector_list.html"
    context_object_name = "grupos_com_setores"

    def get_queryset(self):
        setores_ordenados = Sectors.objects.order_by("name")
        setores = Group.objects.prefetch_related(
            Prefetch("sectors_set", queryset=setores_ordenados)
        )
        return setores


class SetorCreateView(LoginRequiredMixin, CreateView):
    model = Sectors
    template_name = "rule/sector/sector_form.html"
    fields = "__all__"
    success_url = reverse_lazy("rule:setores_list")


class SetorUpdateView(LoginRequiredMixin, UpdateView):
    model = Sectors
    template_name = "rule/sector/sector_form.html"
    fields = "__all__"
    success_url = reverse_lazy("rule:setores_list")


# views do Posto de Trabalho
class PostoTrabaloListView(LoginRequiredMixin, ListView):
    model = WorkStation
    template_name = "rule/workstation/workstation_list.html"
    context_object_name = "postos"
    ordering = ["description"]


class PostoTrabalhoCreateView(LoginRequiredMixin, CreateView):
    model = WorkStation
    template_name = "rule/workstation/workstation_form.html"
    fields = "__all__"
    success_url = reverse_lazy("rule:postos_list")


class PostoTrabalhoUpdateView(LoginRequiredMixin, UpdateView):
    model = WorkStation
    template_name = "rule/workstation/workstation_form.html"
    fields = "__all__"
    success_url = reverse_lazy("rule:postos_list")


@login_required
def get_grupos(request):
    """Retorna os grupos em formato JSON."""
    grupos = Group.objects.all().values("id", "name")
    return JsonResponse(list(grupos), safe=False)


@login_required
@require_GET
def get_setores_by_grupo(request, grupo_id):
    """Retorna os setores de um grupo específico em formato JSON."""
    try:
        grupo = Group.objects.get(id=grupo_id)
        setores = Sectors.objects.filter(group=grupo).values("id", "name")
        return JsonResponse(list(setores), safe=False)
    except Group.DoesNotExist:
        return JsonResponse({"error": "Grupo não encontrado"}, status=404)


@login_required
@csrf_exempt  # Apenas para simplificar o exemplo; em produção, use token CSRF
@require_POST
def cadastrar_posto(request):
    """Recebe dados do formulário e cadastra um novo posto de trabalho."""
    try:
        data = json.loads(request.body)
        setor_id = data.get("setor_id")
        nome_posto = data.get("nome_posto")

        setor = Sectors.objects.get(pk=setor_id)
        WorkStation.objects.create(description=nome_posto, sector=setor)

        return JsonResponse(
            {"message": "Posto de trabalho cadastrado com sucesso!"}, status=201
        )
    except json.JSONDecodeError:
        return JsonResponse({"error": "Dados inválidos"}, status=400)
    except Sectors.DoesNotExist:
        return JsonResponse({"error": "Setor não encontrado"}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

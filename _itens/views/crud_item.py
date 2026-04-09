from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import JsonResponse
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import (
    CreateView,
    DetailView,
    ListView,
)

from _itens.forms import ItemAcabadoForm
from _itens.models import (
    ComponenteProgramacao,
    Componentes,
    Estrutura,
    FamilyProd,
    ItemAcabado,
    ItemBase,
)

PER_PAGE = 25


class ItemAcabadoListView(LoginRequiredMixin, ListView):
    model = ItemAcabado
    template_name = "_itens/item/index.html"
    context_object_name = "itens"
    paginate_by = PER_PAGE

    def get_queryset(self):
        queryset = ItemAcabado.objects.filter(is_active=True).select_related("family")
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        paginator = context["paginator"]
        page = context["page_obj"]
        num_pages = paginator.num_pages

        current_page = page.number

        start_index = max(1, current_page - 2)
        if start_index == 1:
            end_index = min(
                num_pages, 5
            )  # show up to 5 pages if we're near the beginning
        else:
            end_index = min(num_pages, current_page + 2)

        page_range = range(start_index, end_index + 1)

        context["page_range"] = page_range
        context["title"] = "Itens"
        return context


class ItemAcabadoSearchView(LoginRequiredMixin, ListView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._search_value = ""

    def setup(self, request, *args, **kwargs):
        self._search_value = request.GET.get("search", "").strip()
        return super().setup(request, *args, **kwargs)

    def get_queryset(self):
        search_value = self._search_value

        queryset = super().get_queryset()

        if search_value:
            queryset = queryset.filter(
                Q(item_cod__icontains=search_value)
                | Q(item_desc__icontains=search_value)
                | Q(family__name__icontains=search_value)
            )
        return queryset

    model = ItemAcabado
    template_name = "_itens/item/index.html"
    context_object_name = "itens"
    ordering = "item_cod"
    paginate_by = PER_PAGE

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self._search_value:
            search_value = self._search_value
            context.update({"search_value": search_value})

        paginator = context["paginator"]
        page = context["page_obj"]
        num_pages = paginator.num_pages

        current_page = page.number

        start_index = max(1, current_page - 2)
        if start_index == 1:
            end_index = min(
                num_pages, 5
            )  # show up to 5 pages if we're near the beginning
        else:
            end_index = min(num_pages, current_page + 2)

        page_range = range(start_index, end_index + 1)

        context["page_range"] = page_range
        return context


class ItemAcabadoDetailView(LoginRequiredMixin, DetailView):
    model = ItemAcabado
    template_name = "_itens/item/detail.html"
    context_object_name = "item"


class ItemAcabadoCreateView(LoginRequiredMixin, CreateView):
    model = ItemAcabado
    form_class = ItemAcabadoForm
    template_name = "_itens/item/create.html"
    context_object_name = "form"

    success_url = reverse_lazy(
        "_itens:item_list",
    )

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        messages.success(self.request, "Item Criado com sucesso.")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        form_action = reverse("_itens:item_create")
        context["form_action"] = form_action

        familias = FamilyProd.objects.all()
        # familias = FamilyProd.objects.all().values_list("name", flat=True)
        context["all_families"] = familias

        return context


# ===== ENDPOINTS AJAX PARA GERENCIAR BOM =====


class GetBomAbaView(View):
    """Retorna a BOM (Estrutura + ComponenteProgramacao) para um item"""

    def get(self, request, item_id):
        bom_producao = []
        bom_compra = []

        try:
            item = ItemAcabado.objects.get(pk=item_id)

            # Itens produzidos
            estruturas = Estrutura.objects.filter(item=item).select_related("subitem")
            for est in estruturas:
                bom_producao.append(
                    {
                        "id": est.id,
                        "subitem_id": est.subitem.pk,
                        "codigo": est.subitem.itembase_cod,
                        "nome": est.subitem.itembase_name,
                        "qtde_pre": est.qntde_pre or 0,
                        "qtde_usi": est.qntde_usi or 0,
                        "qtde_lix": est.qntde_lix or 0,
                    }
                )

            # Itens comprados
            componentes = ComponenteProgramacao.objects.filter(
                item_acabado=item
            ).select_related("componente")
            for comp in componentes:
                bom_compra.append(
                    {
                        "id": comp.id,
                        "componente_id": comp.componente.pk,
                        "codigo": comp.componente.codigo,
                        "nome": comp.componente.name,
                        "grupo": comp.componente.grupo.name,
                        "quantidade": comp.quantidade,
                        "tipo_compra": comp.componente.get_tipo_compra_display(),
                        "prazo_dias": comp.componente.prazo_entrega_dias or 0,
                    }
                )
        except ItemAcabado.DoesNotExist:
            pass

        return JsonResponse(
            {
                "bom_producao": bom_producao,
                "bom_compra": bom_compra,
            },
            safe=False,
        )


class AddEstruturaProdView(View):
    """Adiciona um item à estrutura (itens produzidos)"""

    def post(self, request, item_id):
        try:
            item = ItemAcabado.objects.get(pk=item_id)
            itembase_id = request.POST.get("itembase_id")
            qtde_pre = request.POST.get("qtde_pre", 0)
            qtde_usi = request.POST.get("qtde_usi", 0)
            qtde_lix = request.POST.get("qtde_lix", 0)

            itembase = ItemBase.objects.get(pk=itembase_id)

            estrutura, created = Estrutura.objects.get_or_create(
                item=item,
                subitem=itembase,
                defaults={
                    "qntde_pre": int(qtde_pre) or 0,
                    "qntde_usi": int(qtde_usi) or 0,
                    "qntde_lix": int(qtde_lix) or 0,
                },
            )

            if not created:
                # Atualizar se já existe
                estrutura.qntde_pre = int(qtde_pre) or 0
                estrutura.qntde_usi = int(qtde_usi) or 0
                estrutura.qntde_lix = int(qtde_lix) or 0
                estrutura.save()

            return JsonResponse(
                {
                    "success": True,
                    "message": "Item adicionado com sucesso",
                    "estrutura": {
                        "id": estrutura.id,
                        "subitem_id": itembase.pk,
                        "codigo": itembase.itembase_cod,
                        "nome": itembase.itembase_name,
                        "qtde_pre": estrutura.qntde_pre,
                        "qtde_usi": estrutura.qntde_usi,
                        "qtde_lix": estrutura.qntde_lix,
                    },
                }
            )
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=400)


class RemoveEstruturaProdView(View):
    """Remove um item da estrutura"""

    def post(self, request, estructura_id):
        try:
            estrutura = Estrutura.objects.get(pk=estructura_id)
            estrutura.delete()
            return JsonResponse(
                {"success": True, "message": "Item removido com sucesso"}
            )
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=400)


class AddComponenteCompraView(View):
    """Adiciona um componente (item comprado) ao produto"""

    def post(self, request, item_id):
        try:
            item = ItemAcabado.objects.get(pk=item_id)
            componente_id = request.POST.get("componente_id")
            quantidade = request.POST.get("quantidade", 1)

            componente = Componentes.objects.get(pk=componente_id)

            comp_prog, created = ComponenteProgramacao.objects.get_or_create(
                item_acabado=item,
                componente=componente,
                defaults={"quantidade": float(quantidade) or 1},
            )

            if not created:
                comp_prog.quantidade = float(quantidade) or 1
                comp_prog.save()

            return JsonResponse(
                {
                    "success": True,
                    "message": "Componente adicionado com sucesso",
                    "componente": {
                        "id": comp_prog.id,
                        "componente_id": componente.pk,
                        "codigo": componente.codigo,
                        "nome": componente.name,
                        "grupo": componente.grupo.name,
                        "quantidade": comp_prog.quantidade,
                        "tipo_compra": componente.get_tipo_compra_display(),
                        "prazo_dias": componente.prazo_entrega_dias or 0,
                    },
                }
            )
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=400)


class RemoveComponenteCompraView(View):
    """Remove um componente comprado do produto"""

    def post(self, request, componente_prog_id):
        try:
            comp_prog = ComponenteProgramacao.objects.get(pk=componente_prog_id)
            comp_prog.delete()
            return JsonResponse(
                {"success": True, "message": "Componente removido com sucesso"}
            )
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=400)


class BuscaItemBaseView(View):
    """Busca ItemBase para autocomplete"""

    def get(self, request):
        term = request.GET.get("q", "")
        resultados = []

        if term:
            itens = ItemBase.objects.filter(
                Q(itembase_cod__icontains=term) | Q(itembase_name__icontains=term)
            )[:10]

            for item in itens:
                resultados.append(
                    {
                        "id": item.pk,
                        "text": f"{item.itembase_cod} - {item.itembase_name}",
                    }
                )

        return JsonResponse({"results": resultados}, safe=False)


class BuscaComponenteView(View):
    """Busca Componente para autocomplete"""

    def get(self, request):
        term = request.GET.get("q", "")
        resultados = []

        if term:
            componentes = Componentes.objects.filter(
                Q(codigo__icontains=term) | Q(name__icontains=term)
            )[:10]

            for comp in componentes:
                resultados.append(
                    {"id": comp.pk, "text": f"{comp.codigo} - {comp.name}"}
                )

        return JsonResponse({"results": resultados}, safe=False)

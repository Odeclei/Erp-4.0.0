import logging

from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView, View

from _itens.models import ItemAcabado
from ppcp.forms import ItemProgramacaoForm, ManufacturingOrderForm
from ppcp.models import ItemProgramacao, ManufacturingOrder

PER_PAGE = 20


class OrderListView(ListView):
    model = ManufacturingOrder
    template_name = "ppcp/index.html"
    context_object_name = "ordens"
    ordering = "-order_number"
    paginate_by = PER_PAGE
    queryset = ManufacturingOrder.objects.select_related("status").all()

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
        return context

    def get_queryset(self):
        query_set = super().get_queryset().order_by("-order_number")
        return query_set


class OrderDetailView(DetailView):
    model = ManufacturingOrder
    template_name = "ppcp/detail.html"
    context_object_name = "item"
    form_class = ItemProgramacaoForm
    sucess_url = reverse_lazy("order:list")
    queryset = ManufacturingOrder.objects.select_related(
        "created_by", "changed_by", "status"
    )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        form = ItemProgramacaoForm()

        ajax_url = reverse_lazy("order:add_item", kwargs={"pk": self.kwargs["pk"]})
        # pk_order = self.kwargs["pk"]

        context["itens_list"] = ItemProgramacao.objects.filter(
            programacao_id=self.object.pk
        ).select_related("item")

        context.update(
            {
                "item_form": form,
                "ajax_url": ajax_url,
            }
        )

        return context


class OrderCreateView(CreateView):
    model = ManufacturingOrder
    form_class = ManufacturingOrderForm
    template_name = "ppcp/create.html"
    context_object_name = "form"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form_action = reverse("order:create")

        context.update(
            {
                "form_action": form_action,
            }
        )
        return context

    def get_success_url(self):
        return reverse_lazy("order:list")

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        messages.success(self.request, "Item Criado com sucesso.")
        return super().form_valid(form)


class OrderUpdateView(UpdateView):
    model = ManufacturingOrder
    template_name = "ppcp/create.html"
    form_class = ManufacturingOrderForm
    context_object_name = "form"

    def get_success_url(self):
        return reverse_lazy("order:detail", kwargs={"pk": self.object.pk})  # type: ignore

    def form_valid(self, form):
        form.instance.changed_by = self.request.user
        messages.success(self.request, "Item Alterado com sucesso.")
        return super().form_valid(form)


class OrderSearchView(ListView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._search_value = ""

    def setup(self, request, *args, **kwargs):
        self._search_value = request.GET.get("search", "").strip()
        return super().setup(request, *args)

    def get_queryset(self):
        search_value = self._search_value
        return super().get_queryset().filter(order_number__icontains=search_value)

    model = ManufacturingOrder
    template_name = "ppcp/index.html"
    context_object_name = "ordens"
    ordering = "-order_number"
    paginate_by = PER_PAGE

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self._search_value:
            search_value = self._search_value
            context.update(
                {
                    "search_value": search_value,
                }
            )
        return context


class BuscaItemView(View):
    def get(self, request, *args, **kwargs):
        term = request.GET.get("q")

        results = []

        # DEBUG: Total de itens no banco
        total_items = ItemAcabado.objects.count()

        if total_items == 0:
            logging.warning("Nenhum item encontrado no banco de dados.", exc_info=True)

        if term:
            # Ajuste 'item_cod' e 'item_desc' para os nomes reais no seu model
            itens = ItemAcabado.objects.filter(
                Q(item_cod__icontains=term) | Q(item_desc__icontains=term)
            )[:20]

            for idx, item in enumerate(itens, 1):
                results.append(
                    {"id": item.pk, "text": f"{item.item_cod} - {item.item_desc}"}
                )

        return JsonResponse({"results": results}, safe=False)


class GetBomView(View):
    """Retorna a Bill of Materials (BOM) de um produto em JSON"""

    def get(self, request, *args, **kwargs):
        from _itens.models import ComponenteProgramacao, Estrutura

        item_id = request.GET.get("item_id")
        bom_producao = []
        bom_compra = []

        if item_id:
            try:
                item = ItemAcabado.objects.get(pk=item_id)

                # ===== ITENS PRODUZIDOS (Estrutura) =====
                estruturas = Estrutura.objects.filter(item=item).select_related(
                    "subitem"
                )
                for est in estruturas:
                    bom_producao.append(
                        {
                            "id": est.subitem.pk,
                            "codigo": est.subitem.itembase_cod,
                            "nome": est.subitem.itembase_name,
                            "qtde_pre": est.qntde_pre or 0,
                            "qtde_usi": est.qntde_usi or 0,
                            "qtde_lix": est.qntde_lix or 0,
                        }
                    )

                # ===== ITENS COMPRADOS (ComponenteProgramacao) =====
                componentes = ComponenteProgramacao.objects.filter(
                    item_acabado=item
                ).select_related("componente")

                for comp_prog in componentes:
                    comp = comp_prog.componente
                    bom_compra.append(
                        {
                            "id": comp.pk,
                            "codigo": comp.codigo,
                            "nome": comp.name,
                            "quantidade": comp_prog.quantidade,
                            "grupo": comp.grupo.name,
                            "tipo_compra": comp.get_tipo_compra_display(),
                            "qtde_minima": comp.qtde_minima,
                            "prazo_dias": comp.prazo_entrega_dias or 0,
                        }
                    )
            except ItemAcabado.DoesNotExist:
                pass

        return JsonResponse(
            {"bom_producao": bom_producao, "bom_compra": bom_compra}, safe=False
        )

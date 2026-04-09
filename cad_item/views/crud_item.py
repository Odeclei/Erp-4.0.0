# flake8: noqa
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
    View,
)

from cad_item.forms import EstruturaForm, ItemForm
from _itens.models import Estrutura, FamilyProd, ItemAcabado as Item, ItemBase as SubItem

PER_PAGE = 20


class ItemListView(ListView):
    model = Item
    template_name = "cad_item/index.html"
    context_object_name = "itens"
    ordering = ("-item_cod",)
    paginate_by = PER_PAGE
    queryset = Item.objects.filter(is_active=True)

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


class ItemCreateView(CreateView):
    model = Item
    form_class = ItemForm
    template_name = "cad_item/create.html"
    context_object_name = "form_item"

    def get_initial(self):
        initial = super().get_initial()
        initial["term"] = ""
        return initial

    def get_success_url(self):
        return reverse_lazy(
            "cad_item:detail", kwargs={"pk": self.object.pk}
        )  # type: ignore

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        form_action = reverse("cad_item:creat")
        family_list = FamilyProd.objects.all().order_by("description")

        ctx.update(
            {
                "form_action": form_action,
                "family_list": family_list,
            }
        )
        return ctx

    def get(self, request, *args, **kwargs):
        term = request.GET.get("term")

        if term:
            families = FamilyProd.objects.filter(
                Q(description__icontains=term) | Q(refer__icontains=term)
            )

            familia_valores = families.values()
            familia_list = list(familia_valores)
            json = JsonResponse(familia_list, safe=False)
            return json
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        messages.success(self.request, "Item Criado com sucesso.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, f"Erro ao cadastrar Item: {form.errors}")
        return super().form_invalid(form)


class ItemUpdateView(UpdateView):
    model = Item
    template_name = "cad_item/create.html"
    form_class = ItemForm
    context_object_name = "form_item"
    success_url = reverse_lazy("cad_item:detail")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form_action = reverse_lazy("cad_item:update", kwargs={"pk": self.object.pk})
        family_list = FamilyProd.objects.all().order_by("description")
        context.update(
            {
                "form_action": form_action,
                "family_list": family_list,
            }
        )
        return context

    def get_success_url(self):
        return reverse_lazy(
            "cad_item:detail", kwargs={"pk": self.object.pk}
        )  # type: ignore

    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        messages.success(self.request, "Item Alterado com Sucesso.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Erro ao atualizar o item.")
        return super().form_invalid(form)


class BuscaFamiliaView(View):
    def get(self, request, *args, **kwargs):
        termo_busca = request.GET.get("q", "").strip()

        family_list = []

        if termo_busca:
            families = FamilyProd.objects.filter(
                Q(description__icontains=termo_busca) | Q(refer__icontains=termo_busca)
            ).order_by("refer")[:10]

            for family in families:
                family_list.append({"id": family.pk, "text": f"{family.description}"})
        return JsonResponse({"results": family_list})


class BuscaSubitemView(View):
    def get(self, request, *args, **kwargs):
        termo_busca = request.GET.get("q", "").strip()
        subitem_list = []

        if termo_busca:
            subitens = SubItem.objects.filter(
                Q(subitem_cod__icontains=termo_busca)
                | Q(name_subitem__icontains=termo_busca)
            ).order_by("subitem_cod")[:10]

            for subitem in subitens:
                subitem_list.append(
                    {
                        "id": subitem.pk,
                        "text": f"{subitem.subitem_cod} - {subitem.name_subitem}",
                    }
                )

        return JsonResponse({"results": subitem_list})


class ItemDetailView(DetailView):
    model = Item
    template_name = "cad_item/detail.html"
    context_object_name = "item"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk_produto = self.kwargs["pk"]
        create_estrtura_url = reverse_lazy(
            "cad_item:estrutura", args=[self.object.pk]
        )  # type: ignore

        estrutura_list = (
            Estrutura.objects.all()
            .filter(item__pk=pk_produto)
            .order_by("subitem__subitem_cod")
        )

        context.update(
            {
                "create_estrtura_url": create_estrtura_url,
                "estrutura_list": estrutura_list,
            }
        )
        return context


class ItemEstruturaCreateView(CreateView):
    model = Estrutura
    form_class = EstruturaForm
    template_name = "cad_item/estrutura.html"

    def get_initial(self):
        initial = super().get_initial()
        initial["item"] = self.kwargs["pk"]
        initial["term"] = ""
        return initial

    def get_success_url(self):
        return reverse_lazy(
            "cad_item:estrutura", kwargs={"pk": self.kwargs["pk"]}
        )  # type: ignore

    def form_valid(self, form):
        messages.success(self.request, "Estrutura Cadastrada com Sucesso.")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        pk_produto = self.kwargs["pk"]
        form_action = reverse_lazy(
            "cad_item:estrutura", kwargs={"pk": pk_produto}
        )  # type: ignore
        ajax_url = reverse_lazy("cad_item:buscasubitem")

        produto = get_object_or_404(Item, pk=pk_produto)

        estrutura_list = (
            Estrutura.objects.all()
            .filter(item__pk=pk_produto)
            .order_by("subitem__subitem_cod")
        )

        ctx.update(
            {
                "produto": produto,
                "estrutura_list": estrutura_list,
                "form_action": form_action,
                "ajax_url": ajax_url,
            }
        )
        return ctx


class EstruturaDeleteView(DeleteView):
    model = Estrutura
    template_name = "cad_item/estrutura_confirm_delete.html"

    def get_success_url(self):
        item_pk = self.object.item.pk
        messages.success(self.request, "Estrutura Deletada com Sucesso.")
        return reverse_lazy("cad_item:estrutura", kwargs={"pk": item_pk})


class ItemSearchView(ListView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._search_value = ""

    def setup(self, request, *args, **kwargs):
        self._search_value = request.GET.get("search", "").strip()
        return super().setup(request, *args, **kwargs)

    def get_queryset(self):
        search_value = self._search_value
        return (
            super()
            .get_queryset()
            .filter(
                Q(item_cod__icontains=search_value)
                | Q(name_prod__icontains=search_value)
                | Q(name_abrev__icontains=search_value)
                | Q(semi_code__icontains=search_value)
                | Q(family__description__icontains=search_value)
            )
        )

    model = Item
    template_name = "cad_item/index.html"
    context_object_name = "itens"
    ordering = ("-item_cod",)
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

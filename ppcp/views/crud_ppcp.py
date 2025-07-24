from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView, View

from cad_item.models import Item
from ppcp.forms import ItemProgramacaoForm, ManufacturingOrderForm
from ppcp.models import ItemProgramacao, ManufacturingOrder

PER_PAGE = 20


class OrderListView(ListView):
    model = ManufacturingOrder
    template_name = "ppcp/index.html"
    context_object_name = "ordens"
    ordering = "-order_number"
    paginate_by = PER_PAGE

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = ItemProgramacaoForm()

        ajax_url = reverse_lazy("order:add_item", kwargs={"pk": self.kwargs["pk"]})
        pk_order = self.kwargs["pk"]

        itens_list = (
            ItemProgramacao.objects.all()
            .filter(programacao__pk=pk_order)
            .order_by("-item__item_cod")
        )

        context.update(
            {
                "item_form": form,
                "itens_list": itens_list,
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
        return reverse_lazy(
            "order:detail", kwargs={"pk": self.object.pk}
        )  # type: ignore

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
        termo_busca = request.GET.get("q", "").strip()

        itens_list = []

        if termo_busca:
            itens_query = Item.objects.filter(
                Q(item_cod__icontains=termo_busca) | Q(name_prod__icontains=termo_busca)
            ).order_by("item_cod")[:10]

            for item in itens_query:
                itens_list.append(
                    {"id": item.pk, "text": f"{item.item_cod} - {item.name_prod}"}
                )

        return JsonResponse({"results": itens_list})

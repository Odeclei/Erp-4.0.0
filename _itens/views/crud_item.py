from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db.models import Q

from django.urls import reverse, reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from _itens.models import ItemAcabado, FamilyProd
from _itens.forms import ItemAcabadoForm

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

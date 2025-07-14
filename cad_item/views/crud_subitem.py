# flake: noqa
from django.contrib import messages
from django.db.models import Q
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from cad_item.forms import SubItemForm
from cad_item.models import Material, SubItem

PER_PAGE = 25


class SubItensView(ListView):
    model = SubItem
    template_name = "cad_item/subitem/index.html"
    context_object_name = "itens"
    ordering = ("-subitem_cod",)
    paginate_by = PER_PAGE

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class SubitemDetailView(DetailView):
    model = SubItem
    template_name = "cad_item/subitem/detail.html"
    context_object_name = "item"


class SubitemCreateView(CreateView):
    model = SubItem
    template_name = "cad_item/subitem/create.html"
    form_class = SubItemForm
    context_object_name = "itens"

    def get_success_url(self):
        return reverse_lazy("cad_item:subitem_detail", kwargs={"pk": self.object.pk})  # type: ignore

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form_action = reverse("cad_item:subitem_create")
        material_list = Material.objects.all().order_by("material_code")
        context.update({"form_action": form_action, "material_list": material_list})
        return context

    def form_valid(self, form):
        messages.success(self.request, "SubItem Criado com sucesso.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, f"Erro ao criar o SubItem: {form.errors}")
        return super().form_invalid(form)


class SubitemUpdateView(UpdateView):
    model = SubItem
    template_name = "cad_item/subitem/create.html"
    form_class = SubItemForm
    context_object_name = "form_item"

    def get_success_url(self):
        return reverse_lazy("cad_item:subitem_detail", kwargs={"pk": self.object.pk})  # type: ignore

    def form_valid(self, form):
        messages.success(self.request, "SubItem Alterado com Sucesso.")
        return super().form_valid(form)

    def form_invalid(self, form):
        print("DEBUG: FORM_INVALID FOI CHAMADO!")
        print("DEBUG: Erros do Formulário: ", form.errors)
        return super().form_invalid(form)


class SubitemSearchView(ListView):
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
                Q(subitem_cod__icontains=search_value)
                | Q(name_subitem__icontains=search_value)
            )
        )

    model = SubItem
    template_name = "cad_item/subitem/index.html"
    context_object_name = "itens"
    ordering = "-subitem_cod"
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

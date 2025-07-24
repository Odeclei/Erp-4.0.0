from django.urls import reverse_lazy, reverse
from django.contrib import messages

from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
    View,
)
from django.db.models import Q
from clientes.models import Clientes
from django.http import JsonResponse
from clientes.forms import ClienteForm

PER_PAGE = 20


class ClienteCreateView(CreateView):
    model = Clientes
    form_class = ClienteForm
    template_name = "clientes/create.html"
    context_object_name = "form"

    def get_success_url(self):
        return reverse_lazy("clientes:detail", kwargs={"pk": self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        form_action = reverse("clientes:create")

        context.update(
            {
                "form_action": form_action,
            }
        )
        return context

    def form_valid(self, form):
        messages.success(self.request, "Cliente Criado com sucesso.")
        return super().form_valid(form)

    def form_invalid(self, form):

        messages.error(self.request, "Erro ao Cadastrar Cliente.")
        return super().form_invalid(form)


class ClienteDetailView(DetailView):
    model = Clientes
    template_name = "clientes/detail.html"
    context_object_name = "clientes"


class ClienteReadView(ListView):
    model = Clientes
    template_name = "clientes/index.html"
    ordering = ("-nome_fantasia",)
    paginate_by = PER_PAGE
    context_object_name = "clientes"

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


class ClienteUpdateView(UpdateView):
    model = Clientes
    form_class = ClienteForm
    template_name = "clientes/create.html"
    context_object_name = "clientes"

    def get_success_url(self):
        return reverse_lazy("clientes:detail", kwargs={"pk": self.object.pk})

    def form_valid(self, form):
        messages.success(self.request, "Cliente Alterado com Sucesso.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Erro ao atualizar o Cliente.")
        return super().form_invalid(form)


class ClienteDeleteView(DeleteView): ...


class ClienteBuscaView(ListView):
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
                Q(cnpj__icontains=search_value)
                | Q(nome_fantasia__icontains=search_value)
                | Q(razao_social__icontains=search_value)
            )
        )

    model = Clientes
    template_name = "clientes/index.html"
    context_object_name = "clientes"
    ordering = ("-nome_fantasia",)
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

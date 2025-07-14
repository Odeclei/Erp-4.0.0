from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
    View,
)

from clientes.models import Clientes

PER_PAGE = 20


class ClienteCreateView(CreateView): 
    ...


class ClienteDetailView(DetailView):
    ...


class ClienteReadView(ListView): 
    model = Clientes
    template_name = "clientes/index.html",
    context_object_name = "clientes"
    ordering = 'nome_fantasia'
    paginate_by = PER_PAGE

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class ClienteUpdateView(UpdateView):
    ...


class ClienteDeleteView(DeleteView):
    ...


class ClienteBuscaView(View):
    ...

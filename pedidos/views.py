from webbrowser import get
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.contrib import messages
from pedidos.models import Pedidos, ItemPedido
from pedidos.forms import PedidoForm, ItemPedidoForm
from clientes.models import Clientes
from cad_item.models import Item, Finish

from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)
from django.db.models import Q

from pedidos.models import Pedidos


class PedidoCreateView(CreateView):
    model = Pedidos
    form_class = PedidoForm
    template_name = "pedidos/create.html"
    context_object_name = "form"

    def get_success_url(self):
        return reverse("pedidos:detail", kwargs={"pk": self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        clientes_list = Clientes.objects.all().order_by("nome_fantasia")

        form_action = reverse("pedidos:create")
        context.update(
            {
                "form_action": form_action,
                "clientes_list": clientes_list,
            }
        )
        return context

    def form_valid(self, form):
        messages.success(self.request, "Pedido Cadastrado com Sucesso.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Erro ao Cadastarar o Pedido.")
        return super().form_invalid(form)


class PedidoListView(ListView):
    model = Pedidos
    template_name = "pedidos/index.html"
    context_object_name = "pedidos"


class PedidoUpdateView(UpdateView):
    model = Pedidos
    form_class = PedidoForm
    template_name = "pedidos/create.html"
    context_object_name = "form"

    def get_success_url(self):
        return reverse("pedidos:detail", kwargs={"pk": self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form_action = reverse("pedidos:update", kwargs={"pk": self.object.pk})
        context.update({"form_action": form_action})
        return context

    def form_valid(self, form):
        messages.success(self.request, "Pedido Alterado com Sucesso.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Erro ao atualizar o Pedido.")
        return super().form_invalid(form)


class PedidoDeleteView(DeleteView): ...


class PedidoDetailView(DetailView):
    model = Pedidos
    template_name = "pedidos/detail.html"
    context_object_name = "pedido"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        itens_pedido = ItemPedido.objects.filter(proforma=self.kwargs["pk"])
        context.update({"itens_pedido": itens_pedido})

        return context


class PedidoSearchView(ListView): ...


class ItemPedidoCreateView(CreateView):
    model = ItemPedido
    form_class = ItemPedidoForm
    template_name = "pedidos/add_item.html"
    context_object_name = "form"

    def get_success_url(self):
        return reverse("pedidos:detail", kwargs={"pk": self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        item_list = Item.objects.all().order_by("item_cod")
        finish_list = Finish.objects.all().order_by("name_finish")
        pedido = get_object_or_404(Pedidos, pk=self.kwargs["pk"])
        itens_pedido = ItemPedido.objects.filter(proforma=pedido.pk)
        form_action = reverse("pedidos:add_item", kwargs={"pk": self.kwargs["pk"]})
        context.update(
            {
                "form_action": form_action,
                "item_list": item_list,
                "pedido": pedido,
                "finish_list": finish_list,
                "itens_pedido": itens_pedido,
            }
        )
        return context

    def form_valid(self, form):
        messages.success(self.request, "Item inserido no Pedido com Sucesso.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Erro ao Inserir Item no Pedido.")
        return super().form_invalid(form)


class ItemPedidoUpdateView(UpdateView):
    model = ItemPedido
    form_class = ItemPedidoForm
    template_name = "pedidos/update_item.html"
    context_object_name = "item_pedido"

    def get_object(self, queryset=...):
        item_pedido = get_object_or_404(ItemPedido, pk=self.kwargs["pk"])
        # return super().get_object(queryset)
        return item_pedido

    def get_success_url(self):
        return reverse("pedidos:detail", kwargs={"pk": self.object.proforma.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        item_list = Item.objects.all().order_by("item_cod")
        finish_list = Finish.objects.all().order_by("name_finish")
        context.update(
            {
                "item_list": item_list,
                "finish_list": finish_list,
            }
        )
        return context

    def form_valid(self, form):
        messages.success(self.request, "Item Alterado com Sucesso.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Erro ao atualizar Item.")
        return super().form_invalid(form)

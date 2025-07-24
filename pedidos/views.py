from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.contrib import messages
from pedidos.models import Pedidos, ItemPedido
from pedidos.forms import PedidoForm, ItemPedidoForm
from clientes.models import Clientes
from cad_item.models import Item, Finish
from utility.views import gerar_zpl_etiqueta
from django.views.decorators.csrf import csrf_exempt
import requests

from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

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
    ordering = "-id"
    paginate_by = 20

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


class PedidoUpdateView(UpdateView):
    model = Pedidos
    form_class = PedidoForm
    template_name = "pedidos/create.html"
    context_object_name = "form"

    def get_success_url(self):
        return reverse("pedidos:detail", kwargs={"pk": self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pedido_pk = self.object.pk
        form_action = reverse("pedidos:update", kwargs={"pk": self.object.pk})
        context.update({"form_action": form_action, "pedido_pk": pedido_pk})
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
        return reverse("pedidos:add_item", kwargs={"pk": self.kwargs["pk"]})

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


def EndPedidoView(request, pk):
    print("Entrei em EndPedidoView")
    if request.method == "GET":
        print("é um GET")
        pedido = get_object_or_404(Pedidos, pk=pk)
        print("pedido:", pedido)

        try:
            print("tentando finalizar pedido")
            pedido.pedido_editable = False
            pedido.save()
            print("pedido finalizado com sucesso")

            return JsonResponse(
                {"success": True, "message": "Pedido finalizado com sucesso!"}
            )
        except Exception as e:
            print("erro ao finalizar pedido", e)
            return JsonResponse(
                {"success": False, "message": f"Erro ao finalizar pedido: {e}"},
                status=500,
            )
    print("não é um GET, retornando 405")
    return JsonResponse(
        {"success": False, "message": "Método não permitido"}, status=405
    )


# @csrf_exempt
def ImprimeEtiquetas(request, pk):
    if request.method == "POST":
        PRINT_SERVER_URL = "http://192.168.1.249:5001/print"
        try:
            itens_pedido = ItemPedido.objects.filter(proforma=pk).select_related(
                "item", "finish", "proforma"
            )

            if not itens_pedido.exists():
                return JsonResponse(
                    {
                        "success": False,
                        "message": "Nenhum item encontrado para este pedido.",
                    },
                    status=404,
                )

            for item in itens_pedido:
                item_name = item.item.name_prod
                item_cod = item.item.item_cod
                acabamento = item.finish.name_finish
                pedido_number = item.proforma.pedido_number
                volume_total = item.item.qtde_volume
                volume_total = int(volume_total)

                for i in range(1, item.quantity + 1):
                    for j in range(1, volume_total + 1):
                        index = f"{item.pk}-{i}-{j}"
                        volume_at = j
                        zpl_code = gerar_zpl_etiqueta(
                            item_name,
                            acabamento,
                            index,
                            pedido_number,
                            item_cod,
                            volume_at,
                            volume_total,
                        )

                        print(f"--- Gerando ZPL para Impressão ---\n{zpl_code}")
                        # imprimir_zpl(zpl_code) # Esta linha será usada no serviço de impressão

                        try:
                            response = requests.post(
                                PRINT_SERVER_URL, json={"zpl": zpl_code}, timeout=5
                            )
                            response.raise_for_status()  # Lança um erro para respostas 4xx/5xx
                        except requests.exceptions.RequestException as e:
                            # Se não conseguir conectar ao serviço de impressão, retorna um erro claro.
                            return JsonResponse(
                                {
                                    "success": False,
                                    "message": f"Erro ao conectar com o serviço de impressão: {e}",
                                },
                                status=503,
                            )
            return JsonResponse(
                {"success": True, "message": "Etiquetas enviadas para impressão."}
            )

        except Exception as e:
            return JsonResponse(
                {"success": False, "message": f"Erro ao gerar etiquetas: {e}"},
                status=500,
            )

    return JsonResponse(
        {"success": False, "message": "Método não permitido."}, status=405
    )

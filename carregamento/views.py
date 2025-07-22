import datetime
import json
from django.http import JsonResponse
from carregamento.models import Carregamento
from carregamento.forms import CarregamentoForm
from pedidos.models import ItemPedido, Pedidos
from django.utils import timezone

from django.contrib import messages
from django.urls import reverse
from django.shortcuts import get_object_or_404, redirect


from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)


class CarregamentoListView(ListView):
    model = Carregamento
    template_name = "carregamento/index.html"
    context_object_name = "carregamentos"


class CarregamentoDetailView(DetailView):
    model = Carregamento


class CarregamentoUpdateView(UpdateView): ...


class CarregamentoDeleteView(DeleteView): ...


class CarregamentoCreateView(CreateView):
    model = Carregamento
    template_name = "carregamento/create.html"
    form_class = CarregamentoForm
    context_object_name = "form"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        pedido_pk = self.kwargs.get("pk")
        pedido = get_object_or_404(Pedidos, pk=pedido_pk)
        list_itens_pedido = ItemPedido.objects.filter(proforma=pedido_pk)
        carregamentos = Carregamento.objects.filter(pedido_data=pedido_pk)

        carregamento_por_item_id = {c.item.id: c.qtde_carregada for c in carregamentos}

        carregamento_data = []
        for item in list_itens_pedido:
            # Tenta obter a qtde_carregada do dicionário.
            # Se item.id não estiver no dicionário (ou seja, não há carregamento para este item),
            # default para 0.
            qtde_carregada = carregamento_por_item_id.get(item.id, 0)
            carregamento_data.append(
                {
                    "item_id": item.id,  # É importante usar item.id aqui, não carregamento.item.id
                    "qtde_carregada": qtde_carregada,
                    "qtde_pedido": item.quantity,
                }
            )

        context.update(
            {
                "pedido": pedido,
                "list_itens_pedido": list_itens_pedido,
                "carregamento_data": carregamento_data,
            }
        )

        return context

    def get_success_url(self):
        pedido_pk = self.kwargs.get("pk")
        return reverse("pedido:detail", kwargs={"pk": pedido_pk})

    def form_valid(self, form):
        messages.success(self.request, "Carregamento salvo com Sucesso.")
        return super().form_valid(form)

    # def form_invalid(self, form):
    #     messages.error(self.request, "Erro ao salvar Carregameto.")
    #     return super().form_invalid(form)


def ler_cod_barras(request):
    pedido_pk = request.GET.get("pedido_pk")
    codigo_barras = request.GET.get("codigo_barras")

    parts = codigo_barras.split("-")

    cod_item = None
    programacao = None
    acabamento = None
    if len(parts) == 2:

        if len(parts[0]) >= 14:
            cod_item = parts[0].strip()
            acabamento = parts[1].strip()
        elif len(parts[0]) == 5:
            programacao = parts[0].strip()
            cod_item = parts[1].strip()
        else:
            print("não entrou no if")
            return JsonResponse({"error": "Formato de Codigo de Barras inválido"})

    else:
        return JsonResponse({"error": "Formato de Codigo de Barras inválido"})

    item = ItemPedido.objects.filter(
        proforma=pedido_pk, item__item_cod=cod_item, finish__name_finish=acabamento
    ).first()

    if item:
        return JsonResponse({"item_id": item.pk})

    else:
        messages.error(request, "Item não encontrado no Pedido")
        return JsonResponse({"error": "Item não encontrado"})


def salvar_itens(request):
    # /*************  ✨ Windsurf Command ⭐  *************/
    """
    Handles the saving of item quantities associated with a specific order (pedido).

    This function processes POST requests to save quantities of items related to an order.
    It expects a JSON payload containing a list of item dictionaries, each with an "itemId"
    and a "qtde" (quantity) field. The function validates and processes the data, creating
    `Carregamento` entries for each item. It also handles various exceptions, including JSON
    decoding errors, validation errors, and database-related errors, providing appropriate
    feedback through messages and JSON responses.

    The function requires the following POST parameters:
    - quantidades: A JSON string representing a list of item data.
    - pedido_pk: The primary key of the order (pedido) related to the items.

    Exceptions handled include:
    - json.JSONDecodeError: Raised when the JSON data can't be decoded.
    - ValueError: Raised for missing or invalid parameters.
    - Carregamento.DoesNotExist: Raised if related foreign keys don't exist.
    - General exceptions for any other errors.

    Successful operations return a JSON response indicating success. Invalid requests
    or errors return a JSON response with an error message.
    """

    # /*******  9d7347bd-0646-40db-ab90-f11f9e25465d  *******/
    if request.method == "POST":
        try:
            quantidades_json = request.POST.get("quantidades")
            if not quantidades_json:
                raise ValueError('Parâmtro "quantidades" ausente')

            quantidades_list = json.loads(quantidades_json)
            if not isinstance(quantidades_list, list):
                raise TypeError("Dados de 'quantidades' não são uma lista JSON válida.")

            pedido_pk = request.POST.get("pedido_pk")
            data_inicio = datetime.datetime.now()
            operador = request.user

            for item_data in quantidades_list:
                item_id_str = item_data.get("itemId")
                qtde_carregada_str = item_data.get("qtde")

                try:
                    item_id = int(item_id_str)
                    qtde_carregada = int(qtde_carregada_str)
                except ValueError:
                    raise ValueError('Parâmtro "quantidades" inválido')

                Carregamento.objects.create(
                    pedido_data_id=pedido_pk,
                    item_id=item_id,
                    data_inicio=data_inicio,
                    qtde_carregada=qtde_carregada,
                    operador=operador,
                )
            messages.success(request, "Itens carregados com sucesso!")
            pedido_update = Pedidos.objects.get(pk=pedido_pk)
            pedido_date = pedido_update.data_inicio
            print(pedido_date)
            if not pedido_date:
                pedido_update.data_inicio = timezone.now()

            pedido_update.status = "LOD"
            pedido_update.save()
            return redirect("pedidos:detail", pk=pedido_pk)

        except json.JSONDecodeError as e:
            error_message = f"Erro ao decodificar JSON das quantidades: {e}. Dados recebidos: {quantidades_json}"
            print("Erro:", error_message)
            messages.error(request, error_message)
            return JsonResponse({"success": False, "message": error_message})

        except ValueError as e:
            error_message = f"Erro de validação de dados: {e}"
            print("Erro:", error_message)
            messages.error(request, error_message)
            return JsonResponse({"success": False, "message": error_message})

        except (
            Carregamento.DoesNotExist
        ):  # Exemplo de tratamento para FKs que não existem
            error_message = "Erro: Pedido ou Item não encontrado."
            print("Erro:", error_message)
            messages.error(request, error_message)
            return JsonResponse({"success": False, "message": error_message})

        except Exception as e:
            error_message = f"Ocorreu um erro inesperado ao salvar os itens: {e}"
            print("Erro:", error_message)
            messages.error(request, error_message)
            return JsonResponse({"success": False, "message": error_message})

    else:
        # Lida com casos em que não é uma requisição POST
        print("Requisição não é POST.")
        messages.error(
            request, "Requisição inválida. Apenas requisições POST são permitidas."
        )
        return JsonResponse(
            {
                "success": False,
                "message": "Requisição inválida. Apenas requisições POST são permitidas.",
            }
        )


def encerrarCarregamento(request):
    if request.method == "POST":
        pedido_pk = request.POST.get("pedido_pk")
        print(pedido_pk)
        pedido_update = Pedidos.objects.get(pk=pedido_pk)
        pedido_update.data_fim = timezone.now()
        pedido_update.status = "FIN"
        pedido_update.save()
        messages.success(request, "Carregamento encerrado com sucesso!")
        return JsonResponse({"success": True, "message": "Carregamento encerrado."})
    else:
        return JsonResponse({"success": False, "message": "Requisição inválida."})

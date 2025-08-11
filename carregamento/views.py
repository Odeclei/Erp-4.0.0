import datetime
import json
from django.http import JsonResponse
from django.contrib import messages
from django.urls import reverse
from django.utils import timezone
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
from decimal import Decimal

from carregamento.models import Carregamento, BarcodeProcessed
from carregamento.forms import CarregamentoForm
from pedidos.models import ItemPedido, Pedidos


from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
    View,
)


class CarregamentoListView(ListView):
    model = Carregamento
    template_name = "carregamento/index.html"
    context_object_name = "carregamentos"
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


class CarregamentoSearchView(ListView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._search_value = ""

    def setup(self, request, *args, **kwargs):
        self._search_value = request.GET.get("search", "").strip()
        return super().setup(request, *args, **kwargs)

    def get_queryset(self):
        search_value = self._search_value
        print(f"search_value: {search_value}")
        query_set = (
            super()
            .get_queryset()
            .filter(
                Q(pedido_data__pedido_number__icontains=search_value)
                | Q(pedido_data__cliente__nome_fantasia__icontains=search_value)
                | Q(item__item__item_cod__icontains=search_value)
                | Q(item__item__name_abrev__icontains=search_value)
            )
        )
        print(f"CarregamentoSearchView.get_queryset: {query_set}")
        return query_set

    model = Carregamento
    template_name = "carregamento/index.html"
    context_object_name = "carregamentos"
    ordering = "-id"
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print(f"CarregamentoSearchView.get_context_data: {context}")
        if self._search_value:
            search_value = self._search_value
            context.update(
                {
                    "search_value": search_value,
                }
            )
        print(f"CarregamentoSearchView.get_context_data: {context}")
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


class CarregamentoDetailView(DetailView):
    model = Carregamento
    template_name = "carregamento/detail.html"
    context_object_name = "carregamento"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        carga_data = Carregamento.objects.get(pk=self.kwargs["pk"])
        context.update({"carga_data": carga_data})
        return context


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
        itens_do_pedido = ItemPedido.objects.filter(proforma=pedido_pk)
        if pedido:
            if not pedido.data_inicio:
                pedido.data_inicio = timezone.now()
                pedido.save()

        qtde_lida_dict = {}
        qtde_total_dict = {}
        for item in itens_do_pedido:
            quantidade_lida = float(self.get_quantidade_lida(item.pk, pedido.pk))

            qtde_lida_dict[item.id] = quantidade_lida
            qtde_total_dict[item.pk] = item.quantity

            qtde_lida_decimal = Decimal.from_float(quantidade_lida)
            qtde_total_decimal = Decimal.from_float(item.quantity)

        context.update(
            {
                "itens_do_pedido": itens_do_pedido,
                "qtde_lida_dict": qtde_lida_dict,
                "qtde_total_dict": qtde_total_dict,
                "pedido": pedido,
            }
        )

        return context

    def get_quantidade_lida(self, item_pedido_pk, pedido_pk):
        carregamentos = Carregamento.objects.filter(pedido_data=pedido_pk)
        print(carregamentos)
        quantidade_lida = 0
        for carregamento in carregamentos:
            if carregamento.item.id == item_pedido_pk:
                quantidade_lida = carregamento.qtde_carregada
        return quantidade_lida

    def get_success_url(self):
        pedido_pk = self.kwargs.get("pk")
        return reverse("pedido:detail", kwargs={"pk": pedido_pk})

    def form_valid(self, form):
        messages.success(self.request, "Carregamento salvo com Sucesso.")
        return super().form_valid(form)


def ler_cod_barras(request):
    pedido_pk = request.GET.get("pedido_pk")
    codigo_barras = request.GET.get("codigo_barras")

    if codigo_barras:
        if BarcodeProcessed.objects.filter(codigo_completo=codigo_barras).exists():
            messages.error(request, "Item ja processado anteriormente!")
            return JsonResponse(
                {"error": "Codigo de Barras ja lido anteriormente!"}, status=409
            )

        parts = codigo_barras.split("-")

    pk_item = None
    seq_item = None
    vol_item = None
    cod_item = None
    programacao = None
    acabamento = None

    if len(parts) == 5:
        pk_item = parts[0].strip()
        seq_item = parts[1].strip()
        vol_item = parts[2].strip()
        if len(parts[3]) >= 14:
            cod_item = parts[3].strip()
            acabamento = parts[4].strip()
        elif len(parts[3]) == 5:
            programacao = parts[3].strip()
            cod_item = parts[4].strip()
        else:
            return JsonResponse(
                {
                    "error": "Formato de Codigo de Barras inv lido",
                    "code": "ALREADY_PROCESSED",
                },
                status=400,
            )

    elif len(parts) == 2:
        if len(parts[0]) >= 14:
            cod_item = parts[0].strip()
            acabamento = parts[1].strip()
        elif len(parts[0]) == 5:
            programacao = parts[0].strip()
            cod_item = parts[1].strip()
        else:
            return JsonResponse(
                {
                    "error": "Formato de Codigo de Barras inv lido",
                    "code": "INVALID_FORMAT",
                }
            )

    else:
        return JsonResponse(
            {"error": "Formato de Codigo de Barras inv lido", "code": "INVALID_FORMAT"}
        )

    if pk_item:
        item = get_object_or_404(ItemPedido, pk=pk_item)
    else:
        try:
            item = ItemPedido.objects.get(
                item__item_cod=cod_item, finish__name_finish=acabamento
            )
        except ItemPedido.DoesNotExist:
            item = None

    if item:
        carregamento = Carregamento.objects.filter(item=item).first()
        pedido = get_object_or_404(Pedidos, pk=pedido_pk)
        pedido.status = "LOD"
        pedido.save()
        if not carregamento:
            carregamento = Carregamento.objects.create(
                pedido_data=item.proforma,
                item=item,
                operador=request.user.first_name,
            )
        try:
            BarcodeProcessed.objects.create(
                codigo_completo=codigo_barras, item=item, carregamento=carregamento
            )
            qtde_salva = carregamento.qtde_carregada

            volume = carregamento.item.item.qtde_volume
            qtde_leitura = 1 / volume
            qtde_nova = Decimal.from_float(qtde_salva) + Decimal.from_float(
                qtde_leitura
            )
            if qtde_nova == item.quantity:
                carregamento.data_fim = timezone.now()
            elif qtde_nova > item.quantity:
                return JsonResponse(
                    {
                        "error": "Quantidade lida maior que quantidade do pedido.",
                        "code": "DB_ERROR",
                    },
                    status=400,
                )
            carregamento.qtde_carregada = qtde_nova
            carregamento.save()

            return JsonResponse({"item_id": item.pk, "qtde_nova": qtde_nova})
        except Exception as e:
            messages.error(request, f"Erro ao processar Codigo de Barras: {e}")
            return JsonResponse(
                {"error": "Erro ao processar Codigo de Barras", "code": "QTD_ERROR"},
                status=500,
            )

    else:
        messages.error(request, "Item nao encontrado no Pedido")
        return JsonResponse(
            {"error": "Item nao encontrado", "code": "ITEM_NOT_FOUND"}, status=404
        )


# def salvar_itens(request):
#     # /*************  ✨ Windsurf Command ⭐  *************/
#     """
#     Handles the saving of item quantities associated with a specific order (pedido).

#     This function processes POST requests to save quantities of items related to an order.
#     It expects a JSON payload containing a list of item dictionaries, each with an "itemId"
#     and a "qtde" (quantity) field. The function validates and processes the data, creating
#     `Carregamento` entries for each item. It also handles various exceptions, including JSON
#     decoding errors, validation errors, and database-related errors, providing appropriate
#     feedback through messages and JSON responses.

#     The function requires the following POST parameters:
#     - quantidades: A JSON string representing a list of item data.
#     - pedido_pk: The primary key of the order (pedido) related to the items.

#     Exceptions handled include:
#     - json.JSONDecodeError: Raised when the JSON data can't be decoded.
#     - ValueError: Raised for missing or invalid parameters.
#     - Carregamento.DoesNotExist: Raised if related foreign keys don't exist.
#     - General exceptions for any other errors.

#     Successful operations return a JSON response indicating success. Invalid requests
#     or errors return a JSON response with an error message.
#     """

#     # /*******  9d7347bd-0646-40db-ab90-f11f9e25465d  *******/
#     if request.method == "POST":
#         try:
#             quantidades_json = request.POST.get("quantidades")
#             if not quantidades_json:
#                 raise ValueError('Parâmtro "quantidades" ausente')

#             quantidades_list = json.loads(quantidades_json)
#             if not isinstance(quantidades_list, list):
#                 raise TypeError("Dados de 'quantidades' não são uma lista JSON válida.")

#             pedido_pk = request.POST.get("pedido_pk")
#             data_inicio = datetime.datetime.now()
#             operador = request.user

#             for item_data in quantidades_list:
#                 item_id_str = item_data.get("itemId")
#                 qtde_carregada_str = item_data.get("qtde")

#                 try:
#                     item_id = int(item_id_str)
#                     qtde_carregada = int(qtde_carregada_str)
#                 except ValueError:
#                     raise ValueError('Parâmtro "quantidades" inválido')

#                 Carregamento.objects.create(
#                     pedido_data_id=pedido_pk,
#                     item_id=item_id,
#                     data_inicio=data_inicio,
#                     qtde_carregada=qtde_carregada,
#                     operador=operador,
#                 )
#             messages.success(request, "Itens carregados com sucesso!")
#             pedido_update = Pedidos.objects.get(pk=pedido_pk)
#             pedido_date = pedido_update.data_inicio
#             if not pedido_date:
#                 pedido_update.data_inicio = timezone.now()

#             pedido_update.status = "LOD"
#             pedido_update.save()
#             return redirect("pedidos:detail", pk=pedido_pk)

#         except json.JSONDecodeError as e:
#             error_message = f"Erro ao decodificar JSON das quantidades: {e}. Dados recebidos: {quantidades_json}"
#             messages.error(request, error_message)
#             return JsonResponse({"success": False, "message": error_message})

#         except ValueError as e:
#             error_message = f"Erro de validação de dados: {e}"
#             messages.error(request, error_message)
#             return JsonResponse({"success": False, "message": error_message})

#         except (
#             Carregamento.DoesNotExist
#         ):  # Exemplo de tratamento para FKs que não existem
#             error_message = "Erro: Pedido ou Item não encontrado."
#             messages.error(request, error_message)
#             return JsonResponse({"success": False, "message": error_message})

#         except Exception as e:
#             error_message = f"Ocorreu um erro inesperado ao salvar os itens: {e}"
#             messages.error(request, error_message)
#             return JsonResponse({"success": False, "message": error_message})

#     else:
#         # Lida com casos em que não é uma requisição POST
#         messages.error(
#             request, "Requisição inválida. Apenas requisições POST são permitidas."
#         )
#         return JsonResponse(
#             {
#                 "success": False,
#                 "message": "Requisição inválida. Apenas requisições POST são permitidas.",
#             }
#         )


def encerrarCarregamento(request):
    if request.method == "POST":
        pedido_pk = request.POST.get("pedido_pk")
        cargo_number = request.POST.get("numero_carregamento")
        lacre_number = request.POST.get("numero_lacre")
        print()
        print(request.POST)
        print()

        pedido_update = Pedidos.objects.get(pk=pedido_pk)
        pedido_update.data_fim = timezone.now()
        pedido_update.status = "FIN"
        pedido_update.cargo_number = cargo_number
        pedido_update.lacre_number = lacre_number
        pedido_update.save()
        messages.success(request, "Carregamento encerrado com sucesso!")
        return JsonResponse({"success": True, "message": "Carregamento encerrado."})
    else:
        return JsonResponse({"success": False, "message": "Requisição inválida."})

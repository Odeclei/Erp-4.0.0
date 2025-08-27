from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from clientes.views import PER_PAGE
from pedidos.models import Pedidos, ItemPedido
from pedidos.forms import PedidoForm, ItemPedidoForm
from clientes.models import Clientes
from cad_item.models import Item, Finish
from utility.views import gerar_zpl_etiqueta
from django.contrib.auth.mixins import UserPassesTestMixin
from django.db import transaction
from django.db.models import Q


import requests
import pandas as pd

from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    View,
    UpdateView,
)

from pedidos.models import Pedidos

PER_PAGE = 20


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
        clientes_list = Clientes.objects.all().order_by("nome_fantasia")
        form_action = reverse("pedidos:update", kwargs={"pk": self.object.pk})
        context.update(
            {
                "form_action": form_action,
                "pedido_pk": pedido_pk,
                "clientes_list": clientes_list,
            }
        )
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


class PedidoSearchView(ListView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._search_value = ""

    def setup(self, request, *args, **kwargs):
        self._search_value = request.GET.get("search", "").strip()
        return super().setup(request, *args, **kwargs)

    def get_queryset(self):
        """
        Filtra a lista de pedidos com base no valor da pesquisa.

        Filtra a lista de pedidos com base no valor da pesquisa, que pode ser
        o n mero do pedido, o nome do cliente ou o nome da empresa.

        :return: Uma lista de objetos Pedidos que s o resultado da pesquisa.
        :rtype: QuerySet
        """
        search_value = self._search_value
        queryset = super().get_queryset()

        if search_value:
            print("valor", search_value)
            queryset = queryset.filter(
                Q(pedido_number__icontains=search_value)
                | Q(pedido_cliente__icontains=search_value)
                | Q(cliente__nome_fantasia__icontains=search_value)
            )

        return queryset

    model = Pedidos
    template_name = "pedidos/index.html"
    context_object_name = "pedidos"
    ordering = "-id"
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
        finish = form.cleaned_data.get("finish")
        pedido = form.cleaned_data.get("proforma").pk
        finish_custom = form.cleaned_data.get("finish_custom")
        finish_defined = ""
        if finish:
            finish_defined = finish
            finish.save()
        elif finish_custom:
            finish_add = Finish.objects.create(
                code_finish=pedido,
                name_finish=finish_custom.upper(),
            )
            finish_defined = finish_add
            finish_add.save()
        else:
            print("No finish found in form data")

        item_pedido = form.save(commit=False)
        item_pedido.finish = finish_defined
        item_pedido.save()

        messages.success(self.request, "Item Cadastrado com Sucesso.")
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
        finish = form.cleaned_data.get("finish")
        pedido = form.cleaned_data.get("proforma").pk
        finish_custom = form.cleaned_data.get("finish_custom")
        finish_defined = ""
        if finish:
            finish_defined = finish
            finish.save()
        elif finish_custom:
            finish_add = Finish.objects.create(
                code_finish=pedido,
                name_finish=finish_custom.upper(),
            )
            finish_defined = finish_add
            finish_add.save()
        else:
            print("No finish found in form data")

        item_pedido = form.save(commit=False)
        item_pedido.finish = finish_defined
        item_pedido.save()
        messages.success(self.request, "Item Alterado com Sucesso.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Erro ao atualizar Item.")
        return super().form_invalid(form)


class ItemPedidoDeleteView(DeleteView):
    model = ItemPedido
    template_name = "pedidos/delete_item.html"

    def get_success_url(self):
        messages.success(self.request, "Item Removido com Sucesso.")
        return reverse_lazy("pedidos:detail", kwargs={"pk": self.object.proforma.pk})


class ImportarPedidoView(UserPassesTestMixin, View):
    template_name = "pedidos/importar_pedido.html"

    def test_func(self):
        return self.request.user.is_staff

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        """
        Processa o arquivo Excel e cria/atualiza os pedidos.
        """
        print("Iniciando processamento do arquivo Excel.")

        if "arquivo_excel" not in request.FILES:
            print("Nenhum arquivo foi enviado.")
            return render(
                request,
                self.template_name,
                {
                    "erro": "Nenhum arquivo foi enviado. Por favor, selecione um arquivo Excel."
                },
            )

        arquivo_excel = request.FILES["arquivo_excel"]
        print(f"Arquivo recebido: {arquivo_excel.name}")

        if not arquivo_excel.name.endswith((".xls", ".xlsx")):
            print("Formato de arquivo inválido.")
            return render(
                request,
                self.template_name,
                {
                    "erro": "Formato de arquivo inválido. Por favor, envie um arquivo .xls ou .xlsx."
                },
            )

        try:
            print("Lendo arquivo Excel.")
            df = pd.read_excel(arquivo_excel)
            df = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
            print("Arquivo Excel lido com sucesso.")

            print()
            print(df)
            print()

            with transaction.atomic():
                pedidos_criados = 0
                itens_criados = 0
                print("Iniciando transação de banco de dados.")

                for index, row in df.iterrows():
                    import pdb

                    print(f"Processando linha {index + 2} do Excel.")
                    # programa = row["PROGRAMAÇÃO"]
                    cod_cliente = row["CÓDIGO"]
                    # nome_cliente = row["NOME"]
                    nr_pedido = str(row["PEDIDO"])
                    cod_item = row["ITEM"]
                    # desc_item = row["DESCRIÇÃO"]
                    acabamento = row["NARRATIVA"]
                    observacao = str(row["OBS_PEDIDO"])
                    # O SALDO.FATURAR não está sendo usado, mas a variável pode ser criada
                    qtde_item = row["SALDO.FATURAR"]

                    print("cod_cliente", cod_cliente, type(cod_cliente))
                    print("nr_pedido", nr_pedido, type(nr_pedido))
                    print("cod_item", cod_item, type(cod_item))
                    print("acabamento", acabamento, type(acabamento))
                    print("observacao", observacao, type(observacao))
                    print("qtde_item", qtde_item, type(qtde_item))

                    try:
                        cliente = Clientes.objects.get(pk=cod_cliente)
                        print(f"Cliente {cod_cliente} encontrado.")
                    except Clientes.DoesNotExist:
                        print(
                            f"Cliente {cod_cliente} não encontrado. Linha {index + 2} ignorada."
                        )
                        continue

                    pedido_numero = f"CADASTRAR PEDIDO {index + 2}"
                    pedido, created = Pedidos.objects.get_or_create(
                        pedido_cliente=nr_pedido,
                        defaults={
                            "cliente": cliente,
                            "pedido_cliente": nr_pedido,
                            "pedido_number": pedido_numero,
                        },
                    )
                    if created:
                        pedidos_criados += 1
                        print(f"Pedido {nr_pedido} criado.")

                    try:
                        item = Item.objects.get(item_cod=cod_item)
                        print(f"Item {cod_item} encontrado.")
                    except Item.DoesNotExist:
                        print(
                            f"Item com código {cod_item} não encontrado. Linha {index + 2} ignorada."
                        )
                        continue

                    try:
                        finish_code = f"{nr_pedido}{index + 2}"
                        finish, _ = Finish.objects.get_or_create(
                            code_finish=finish_code, name_finish=acabamento
                        )
                        print(f"Finish {acabamento} processado.")
                    except Exception:
                        finish = "-"
                        print("Erro ao processar acabamento.")

                    ItemPedido.objects.create(
                        proforma=pedido,
                        item=item,
                        finish=finish,
                        quantity=qtde_item,
                        observation=observacao,
                    )
                    itens_criados += 1
                    print(f"ItemPedido criado para pedido {nr_pedido}.")
                    # pdb.set_trace()

            print("Transação de banco de dados finalizada com sucesso.")
            return render(
                request,
                self.template_name,
                {
                    "sucesso": f"Importação concluída com sucesso! {pedidos_criados} pedido(s) e {itens_criados} item(s) de pedido foram criados ou atualizados."
                },
            )

        except Exception as e:
            print(f"Erro durante a importação: {str(e)}")
            return render(
                request,
                self.template_name,
                {"erro": f"Ocorreu um erro durante a importação: {str(e)}"},
            )

    # def post(self, request, *args, **kwargs):
    #     if "arquivo_excel" not in request.FILES:
    #         return render(
    #             request, self.template_name, {"error": "Nenhum arquivo foi carregado."}
    #         )
    #     arquivo_excel = request.FILES["arquivo_excel"]

    #     if not arquivo_excel.name.endswith((".xlsx", ".xls")):
    #         return render(
    #             request,
    #             self.template_name,
    #             {"error": "Formato de arquivo inválido. Deve ser .xlsx ou .xls."},
    #         )
    #     try:
    #         df = pd.read_excel(arquivo_excel)
    #         df = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
    #         print()
    #         print("df", df)
    #         print()
    #         with transaction.atomic():
    #             pedidos_criados = 0
    #             itens_criados = 0

    #             for index, row in df.iterrows():
    #                 print(f"linha {index+2}")

    #                 cod_cliente = row["CÓDIGO"]
    #                 nome_cliente = row["NOME"]
    #                 nr_pedido = row["NR.PEDIDO"]
    #                 cod_item = row["ITEM"]
    #                 desc_item = row["DESCRIÇÃO"]
    #                 qtde_item = row["SALDO.FATURAR"]
    #                 acabamento = row["NARRATIVA"]
    #                 observacao = row["OBS.PEDIDO"]

    #                 print(f"cliente {cod_cliente} - {nome_cliente}")
    #                 print(f"nr_pedido {nr_pedido}")
    #                 print(f"cod_item {cod_item} - {desc_item}")
    #                 print(f"qtde_item {qtde_item}")
    #                 print(f"acabamento {acabamento}")
    #                 print(f"observacao {observacao}")

    #                 try:
    #                     cliente = Clientes.objects.get(pk=cod_cliente)
    #                 except Clientes.DoesNotExist:
    #                     print(
    #                         f"Cliente {cod_cliente} não encontrado. Linha {index+2} ignorada."
    #                     )
    #                     continue

    #                 print(f"cliente {cod_cliente} encontrado")

    #                 pedido, created = Pedidos.objects.get_or_create(
    #                     pedido_cliente=nr_pedido,
    #                     defaults={
    #                         "cliente": cliente,
    #                         "pedido_number": nr_pedido,
    #                     },
    #                 )
    #                 if created:
    #                     pedidos_criados += 1
    #                 print(f"pedido {nr_pedido} criado")

    #                 try:
    #                     item = Item.objects.get(item_cod=cod_item)
    #                 except Item.DoesNotExist:
    #                     print(
    #                         f"Item com código {cod_item} não encontrado. Linha {index+2} ignorada."
    #                     )
    #                     continue

    #                 print(f"item {cod_item} encontrado")

    #                 try:
    #                     finish, _ = Finish.objects.get_or_create(
    #                         name_finish=acabamento,
    #                         code_finish=f"{nr_pedido}{index+2}",
    #                     )
    #                 except Exception:
    #                     finish = "-"
    #                 print(f"finish {acabamento} criado")

    #                 item_pedido = ItemPedido.objects.create(
    #                     proforma=pedido,
    #                     item=item,
    #                     finish=finish,
    #                     quantity=qtde_item,
    #                 )
    #                 itens_criados += 1

    #                 print(f"item_pedido {cod_item} criado")

    #         msg = f"Pedidos e itens criados com sucesso. {pedidos_criados} pedidos criados e {itens_criados} itens criados."
    #         return render(request, self.template_name, {"success": msg})
    #     except Exception as e:
    #         return render(
    #             request,
    #             self.template_name,
    #             {"error": f"Ocorreu um erro durante a importação:{str(e)}"},
    #         )


def EndPedidoView(request, pk):
    if request.method == "GET":
        pedido = get_object_or_404(Pedidos, pk=pk)

        try:
            pedido.pedido_editable = False
            pedido.save()

            return JsonResponse(
                {"success": True, "message": "Pedido finalizado com sucesso!"}
            )
        except Exception as e:
            return JsonResponse(
                {"success": False, "message": f"Erro ao finalizar pedido: {e}"},
                status=500,
            )
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
                print(
                    f"ImprimeEtiquetas: Nenhum item encontrado para este pedido {pk}."
                )
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
                acabamento = item.finish.name_finish if item.finish else ""
                pedido_number = item.proforma.pedido_number
                observation = item.observation

                volume_por_unidade = item.item.qtde_volume
                quantidade_item = int(item.quantity)

                if volume_por_unidade == 0.5:
                    volume_por_unidade = int(1)
                else:
                    volume_por_unidade = int(volume_por_unidade)

                qtde_item_ped = item.quantity
                volume_total = int(volume_por_unidade)

                for i in range(1, qtde_item_ped + 1):
                    for j in range(1, volume_por_unidade + 1):
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
                            observation,
                        )

                        try:
                            response = requests.post(
                                PRINT_SERVER_URL, json={"zpl": zpl_code}, timeout=20
                            )
                            response.raise_for_status()  # Lan a um erro para respostas 4xx/5xx
                        except requests.exceptions.RequestException as e:
                            # Se n o conseguir conectar ao servi o de impress o, retorna um erro claro.
                            print(
                                f"ImprimeEtiquetas: Erro ao conectar com o servi o de impress o: {e}"
                            )
                            return JsonResponse(
                                {
                                    "success": False,
                                    "message": f"Erro ao conectar com o servi o de impress o: {e}",
                                },
                                status=503,
                            )
            return JsonResponse(
                {"success": True, "message": "Etiquetas enviadas para impress o."}
            )

        except Exception as e:
            return JsonResponse(
                {"success": False, "message": f"Erro ao gerar etiquetas: {e}"},
                status=500,
            )

    return JsonResponse(
        {"success": False, "message": "M todo n o permitido."}, status=405
    )


def LiberarPedido(request, pk):
    if request.method == "GET":
        pedido_pk = request.GET.get("pedido_pk")

        if pedido_pk:
            pedido = get_object_or_404(Pedidos, pk=pedido_pk)

            pedido.pedido_editable = True
            pedido.save()

            return JsonResponse(
                {"success": True, "message": "Pedido liberado com sucesso."}
            )
        else:
            return JsonResponse(
                {"success": False, "message": "Pedido nao encontrado."}, status=404
            )

    return JsonResponse(
        {"success": False, "message": "Metodo nao permitido."}, status=405
    )

# flake8: noqa
import json
from operator import sub

from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, DeleteView, UpdateView

from _itens.models import Estrutura, ItemAcabado as Item
from ppcp.forms import ItemProgramacaoForm, SubItemProgramacaoForm
from ppcp.models import ItemProgramacao, ManufacturingOrder, SubItemProgramacao


class ItemOrderCreateView(CreateView):
    model = ItemProgramacao
    form_class = ItemProgramacaoForm
    template_name = "ppcp/item-order/add_item.html"

    def get_success_url(self):
        return reverse_lazy("order:detail", kwargs={"pk": self.kwargs["pk"]})

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        print("\n" + "=" * 60)
        print(">>> ITEMORDERCREATVIEW - FORM_VALID <<<")
        print("=" * 60)

        # DEBUG: Mostra todos os dados POST
        print("\n[POST DATA]")
        for key, value in self.request.POST.items():
            print(f"  {key}: {value} (type: {type(value).__name__})")

        # DEBUG: Dados do form
        print("\n[FORM DATA]")
        print(f"  form.cleaned_data: {form.cleaned_data}")
        print(f"  form.errors: {form.errors}")

        # DEBUG: Campo item especificamente
        print("\n[CAMPO ITEM]")
        item_value = form.cleaned_data.get("item")
        print(f"  item_value: {item_value}")
        print(f"  item_value type: {type(item_value).__name__}")
        print(f"  item_value is None: {item_value is None}")

        start_at = self.request.POST.get("start_at")
        ends_at = self.request.POST.get("ends_at")

        print(f"\n[DATAS]")
        print(f"  start_at: {start_at}")
        print(f"  ends_at: {ends_at}")

        item_programado = form.save(commit=False)

        print(f"\n[ITEM_PROGRAMADO ANTES DE SALVAR]")
        print(f"  item_programado.item: {item_programado.item}")
        print(f"  item_programado.quantidade: {item_programado.quantidade}")

        # DEBUG: Verifica se a programação existe
        pk_programacao = self.kwargs["pk"]
        print(f"\n[VERIFICANDO PROGRAMAÇÃO]")
        print(f"  PK procurado: {pk_programacao}")
        try:
            programacao = ManufacturingOrder.objects.get(pk=pk_programacao)
            print(f"  ✓ Programação encontrada: {programacao}")
            print(f"    - order_number: {programacao.order_number}")
            print(f"    - status: {programacao.status}")
        except ManufacturingOrder.DoesNotExist:
            print(f"  ✗ ERRO: Programação NÃO existe no banco!")
            messages.error(
                self.request, f"Erro: Programação {pk_programacao} não encontrada!"
            )
            return self.form_invalid(form)

        item_programado.programacao = programacao

        if start_at:
            item_programado.start_at = start_at
        if ends_at:
            item_programado.ends_at = ends_at

        print(f"\n[TENTANDO SALVAR ITEM_PROGRAMADO]")
        print(f"  item: {item_programado.item}")
        if item_programado.item:
            print(f"  item.pk: {item_programado.item.pk}")
        print(f"  programacao: {item_programado.programacao}")
        print(f"  programacao.pk: {item_programado.programacao.pk}")
        print(f"  quantidade: {item_programado.quantidade}")

        # DEBUG: Verifica se o item existe no banco
        if item_programado.item:
            print(f"\n[VERIFICANDO ITEM]")
            try:
                item_db = Item.objects.get(pk=item_programado.item.pk)
                print(f"  ✓ Item existe no banco: {item_db}")
            except Item.DoesNotExist:
                print(
                    f"  ✗ ERRO: Item {item_programado.item.pk} não existe em ItemAcabado!"
                )

        try:
            item_programado.save()
            print("✓ Item salvo com sucesso!")
        except Exception as e:
            print(f"✗ ERRO ao salvar: {str(e)}")
            print(f"  Tipo do erro: {type(e).__name__}")
            import traceback

            print(f"  Traceback: {traceback.format_exc()}")
            messages.error(self.request, f"Erro ao salvar o item: {str(e)}")
            return self.form_invalid(form)

        messages.success(self.request, "Item Programado com Sucesso.")

        item = item_programado.item.pk

        print(f"\n[PROCURANDO ESTRUTURA]")
        print(f"  item.pk: {item}")

        subprodutos = Estrutura.objects.filter(item__pk=item).select_related("subitem")

        print(f"  Estruturas encontradas: {subprodutos.count()}")

        list_subprodutos = []

        for subitem in subprodutos:
            produto_programado = item_programado
            subproduto = subitem
            programacao = item_programado.programacao
            q_item = item_programado.quantidade
            q_s_pre = subitem.qntde_pre
            q_s_usi = subitem.qntde_usi
            q_s_lix = subitem.qntde_lix

            list_subprodutos.append(
                SubItemProgramacao(
                    produto_programado=produto_programado,
                    subproduto=subproduto.subitem,
                    programacao=programacao,
                    qtde_pre=q_item * q_s_pre,
                    qtde_usi=q_item * q_s_usi,
                    qtde_lix=q_item * q_s_lix,
                )
            )

        print(f"\n[CRIANDO SUBITENS]")
        print(f"  Total de subitens a criar: {len(list_subprodutos)}")

        if len(list_subprodutos) > 0:
            try:
                SubItemProgramacao.objects.bulk_create(list_subprodutos)
                print("✓ Subitens criados com sucesso!")
            except Exception as e:
                print(f"✗ ERRO ao criar subitens: {str(e)}")
                messages.warning(
                    self.request, f"Item salvo, mas sem subitens: {str(e)}"
                )

        print("=" * 60 + "\n")
        return super().form_valid(form)

    def form_invalid(self, form):
        print("\n" + "=" * 60)
        print(">>> ITEMORDERCREATVIEW - FORM_INVALID <<<")
        print("=" * 60)
        print("\n[ERROS DO FORMULÁRIO]")
        for field, errors in form.errors.items():
            print(f"  {field}: {errors}")
            for error in errors:
                messages.error(self.request, f"{field}: {error}")
        print("=" * 60 + "\n")
        return super().form_invalid(form)

    def get_initial(self):
        initial = super().get_initial()
        initial["order_pk"] = self.kwargs["pk"]
        initial["term"] = ""
        order_prod = get_object_or_404(ManufacturingOrder, pk=self.kwargs["pk"])
        initial["order_number"] = order_prod.pk

        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        order_prod = get_object_or_404(ManufacturingOrder, pk=self.kwargs["pk"])

        form_action = reverse("order:add_item", kwargs={"pk": order_prod.pk})
        ajax_url = reverse_lazy("order:add_item", kwargs={"pk": self.kwargs["pk"]})

        context.update(
            {
                "order_prod": order_prod,
                "form_action": form_action,
                "ajax_url": ajax_url,
            }
        )

        return context

    def get(self, request, *args, **kwargs):
        term = request.GET.get("term")

        if term:
            itens = Item.objects.filter(
                Q(item_cod__icontains=term) | Q(item_desc__icontains=term)
            )
            data = [{"id": item.pk, "text": item.item_desc} for item in itens]
            return JsonResponse(data, safe=False)
        return super().get(request, *args, **kwargs)


class SubItemOrderUpdateView(UpdateView):
    model = SubItemProgramacao
    form_class = SubItemProgramacaoForm
    template_name = "ppcp/item-order/update_subitem.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        sub_programado = SubItemProgramacao.objects.get(pk=self.kwargs["pk"])
        form_action = reverse_lazy(
            "order:update_subitem",
            kwargs={
                "pk": sub_programado.pk,
            },
        )

        ctx.update(
            {
                "sub_programado": sub_programado,
                "form_action": form_action,
            }
        )

        return ctx

    def get_success_url(self):
        sub_programado = SubItemProgramacao.objects.get(pk=self.kwargs["pk"])
        order_pk = sub_programado.programacao.order_number  # type: ignore
        item_pk = sub_programado.produto_programado.pk  # type: ignore

        return reverse_lazy(
            "order:update_item",
            kwargs={
                "pk": item_pk,
                "order_number": order_pk,
            },
        )


class SubItemDeleteView(DeleteView):
    model = SubItemProgramacao
    template_name = "ppcp/item-order/delete_subitem.html"

    def get_success_url(self):
        sub_programado = SubItemProgramacao.objects.get(pk=self.kwargs["pk"])
        order_pk = sub_programado.programacao.order_number  # type: ignore
        item_pk = sub_programado.produto_programado.pk  # type: ignore
        return reverse_lazy(
            "order:update_item", kwargs={"pk": item_pk, "order_number": order_pk}
        )


class ItemOrderUpdateView(UpdateView):
    model = ItemProgramacao
    form_class = ItemProgramacaoForm
    template_name = "ppcp/item-order/update_item.html"

    def get_initial(self):
        initial = super().get_initial()
        initial["qtde_original"] = ""
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        item_pk = self.kwargs["pk"]
        form_action = reverse_lazy(
            "order:update_item",
            kwargs={"pk": item_pk, "order_number": self.kwargs["order_number"]},
        )

        order_prod = get_object_or_404(
            ManufacturingOrder, order_number=self.kwargs["order_number"]
        )

        subitem_list = (
            SubItemProgramacao.objects.all()
            .filter(produto_programado__pk=self.kwargs["pk"])
            .filter(programacao__order_number=self.kwargs["order_number"])
        )

        context.update(
            {
                "item_pk": item_pk,
                "order_prod": order_prod,
                "form_action": form_action,
                "subitem_list": subitem_list,
            }
        )
        return context

    def get_success_url(self):
        order_prod = get_object_or_404(
            ManufacturingOrder, order_number=self.kwargs["order_number"]
        )
        return reverse_lazy("order:detail", kwargs={"pk": order_prod.pk})

    def form_valid(self, form):
        starts_at = self.request.POST.get("data_start_input")
        ends_at = self.request.POST.get("data_end_input")

        item_programado = form.save(commit=False)
        if starts_at:
            item_programado.start_at = starts_at
        if ends_at:
            item_programado.ends_at = ends_at

        item_programado.save()

        # Atualizar os subitens (filhos) conforme a nova quantidade do item pai
        subitens = SubItemProgramacao.objects.filter(
            produto_programado=item_programado, programacao=item_programado.programacao
        )

        # Pegue a estrutura para saber os fatores de multiplicação
        estruturas = Estrutura.objects.filter(item=item_programado.item)
        estrutura_map = {e.subitem.pk: e for e in estruturas}

        for subitem in subitens:
            estrutura = estrutura_map.get(subitem.subproduto.pk)
            if estrutura:
                subitem.qtde_pre = item_programado.quantidade * estrutura.qntde_pre
                subitem.qtde_usi = item_programado.quantidade * estrutura.qntde_usi
                subitem.qtde_lix = item_programado.quantidade * estrutura.qntde_lix
                subitem.save()

        messages.success(self.request, "Item e subitens atualizados com sucesso")
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)


class ItemOrderDeleteView(DeleteView):
    model = ItemProgramacao
    template_name = "ppcp/item-order/delete_item.html"

    def get_success_url(self):
        order_prod = get_object_or_404(
            ManufacturingOrder, order_number=self.kwargs["order_number"]
        )
        return reverse_lazy("order:detail", kwargs={"pk": order_prod.pk})


# @csrf_exempt
def c_quantidade(request):
    id_item = request.POST.get("id_item")
    id_programacao = request.POST.get("id_programação")
    qtde_alterada = request.POST.get("qtde_alterada")

    item = get_object_or_404(ItemProgramacao, pk=id_item)

    if item.quantidade != qtde_alterada:
        data = {
            "qtde_original": item.quantidade,
            "qtde_alterada": qtde_alterada,
            "is_altered": True,
        }
        return JsonResponse(data)

    data = {"is_altered": False}
    return JsonResponse(data)


def a_quantidade(request):
    if request.method == "POST":
        data = json.loads(request.body)
        pks = data.get("pks")
        n_qtde = data.get("n_qtde")
        id_item_pai = data.get("id_item")

        item_programado = get_object_or_404(ItemProgramacao, pk=id_item_pai)

        item_pain_pk = item_programado.item.pk  # type: ignore

        subprodutos = Estrutura.objects.all().filter(item__pk=item_pain_pk)

        list_new_qtde = []

        for chave, subproduto in zip(pks, subprodutos):
            sub_programados = SubItemProgramacao.objects.get(pk=chave)

            qtde_original = item_programado.quantidade

            qtde_pre_estrut = subproduto.qntde_pre
            qtde_usi_estrut = subproduto.qntde_usi
            qtde_lix_estrut = subproduto.qntde_lix

            alter_pre = int(qtde_pre_estrut) * int(n_qtde)  # type: ignore
            alter_usi = int(qtde_usi_estrut) * int(n_qtde)  # type: ignore
            alter_lix = int(qtde_lix_estrut) * int(n_qtde)  # type: ignore

            sub_programados.qtde_pre = alter_pre
            sub_programados.qtde_usi = alter_usi
            sub_programados.qtde_lix = alter_lix

            sub_programados.save()

            list_new_qtde.append({"pk": chave, "qtde": alter_pre})

        data = json.dumps(list_new_qtde)
        return JsonResponse(data, safe=False)
    else:
        return JsonResponse({"erro": "Método não permitido"})

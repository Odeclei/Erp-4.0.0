# flake8: noqa
# type: ignore
import datetime
import json

from django.apps import apps
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy

from apont.models import Apont_Type, Motive
from cad_item.models import Estrutura
from ppcp.models import ItemProgramacao, SubItemProgramacao
from rule.models import Machines, MacId


def get_template_url(request): ...


def select_model_by_machine_id(machine_id):
    machine = get_object_or_404(Machines, pk=machine_id)

    machine_code = machine.code
    machine_formatado = f"{machine_code[0].upper()}{
        machine_code[1:].lower()}"
    model_nm = machine_formatado.replace("-", "_")

    model = apps.get_model("apont", model_nm)
    return model


def select_pai(barcode, programacao):
    if len(barcode) == 13:
        produto_pai = f"{barcode[-7:-2]}"
    elif len(barcode) == 16:
        produto_pai = f"{barcode[-10:-2]}"

    try:
        produto = get_object_or_404(
            ItemProgramacao,
            item__semi_code=produto_pai,
            programacao__order_number=programacao,
        )
        return produto
    except ItemProgramacao.DoesNotExist:
        return None


def select_sub(barcode, programacao):
    if len(barcode) == 13:
        subproduto_code = f"{barcode[-7:]}"
    elif len(barcode) == 16:
        subproduto_code = f"{barcode[-10:]}"
    try:
        subproduto = get_object_or_404(
            SubItemProgramacao,
            subproduto__subitem_cod=subproduto_code,
            programacao__order_number=programacao,
        )
        return subproduto
    except SubItemProgramacao.DoesNotExist:
        return None


def adicionar_apontamento(maquina_id, apontamento_id):
    try:
        with open("apontamentos.json", "r") as f:
            dados = json.load(f)
    except FileNotFoundError:
        dados = {}

    if maquina_id not in dados:
        dados[maquina_id] = []

    dados[maquina_id].append(apontamento_id)

    with open("apontamentos.json", "w") as f:
        json.dump(dados, f, indent=4)


def remover_apontamento(maquina_id, apontamento_id):
    try:
        with open("apontamentos.json", "r") as f:
            dados = json.load(f)
    except FileNotFoundError:
        return

    if maquina_id in dados:
        dados[maquina_id] = [id for id in dados[maquina_id] if id != apontamento_id]

    with open("apontamentos.json", "w") as f:
        json.dump(dados, f, indent=4)


def ReadBarcodeView(request):
    if request.method == "GET":

        form_action = reverse_lazy("apont:read_barcode")

        context = {
            "form_action": form_action,
        }

        return render(
            request,
            "apont/index.html",
        )

    if request.method == "POST":
        barcode = request.POST.get("barcode_inicial")
        machine_id = request.POST.get("machine_id")

        data_atual = datetime.datetime.now()
        data = data_atual.strftime("%Y-%m-%d")
        hora = data_atual.strftime("%H:%M:%S")

        programacao = barcode[0:4]
        ano = barcode[4:6]
        produto = select_pai(barcode, programacao)
        subproduto = select_sub(barcode, programacao)
        operador = request.user

        dados = {
            "data": data,
            "ano": ano,
            "programacao": programacao,
            "produto_pai": produto,
            "produto_apontado": subproduto,
            "hora_inicio_setup": hora,
            "user": operador,
        }

        model = select_model_by_machine_id(machine_id)
        novo_apontamento = model(**dados)
        novo_apontamento.save()
        id_apont = novo_apontamento.pk

        context = {
            "item_prog": produto.pk,
            "subitem_prog": subproduto.pk,
            "barcode": barcode,
            "id_apont": id_apont,
            "machine_id": machine_id,
        }

        adicionar_apontamento(machine_id, id_apont)
        request.session["dados"] = context
        return redirect("apont:start_setup")

    return render(
        request,
        "apont/index.html",
    )


def IniciarSetupView(request):
    if request.method == "GET":
        context_data = request.session.get("dados", {})
        # request.session['dados'] = {}

        item_prog_pk = context_data.get("item_prog")
        subitem_prog_pk = context_data.get("subitem_prog")
        machine_id = context_data.get("machine_id")

        item_prog = ItemProgramacao.objects.get(pk=item_prog_pk)
        subitem_prog = SubItemProgramacao.objects.get(pk=subitem_prog_pk)
        barcode = context_data.get("barcode")
        id_apont = context_data.get("id_apont")
        form_action = reverse_lazy("apont:start_setup")
        apont_type = Apont_Type.objects.all()
        rework_motive = Motive.objects.all()

        maquina = Machines.objects.get(pk=machine_id)
        setor = maquina.sector

        estrutura = Estrutura.objects.filter(item__pk=item_prog.item.pk)

        qtde_item_day = item_prog.item.qtd_per_day
        qtde_total_peças = 0

        if setor.name == "Usinagem":
            for item in estrutura:
                x = int(item.qntde_usi) * int(qtde_item_day)
                qtde_total_peças += x
        elif setor.name == "Lixacao":
            for item in estrutura:
                x = int(item.qntde_lix) * int(qtde_item_day)
                qtde_total_peças += x
        elif setor.name == "Preparacao":
            for item in estrutura:
                x = int(item.qntde_pre) * int(qtde_item_day)
                qtde_total_peças += x
        else:
            print("deu erro view IniciarSetup, parte da soma dos subiens")

        context = {
            "item_prog": item_prog,
            "subitem_prog": subitem_prog,
            "barcode": barcode,
            "id_apont": id_apont,
            "form_action": form_action,
            "apont_type": apont_type,
            "rework_motive": rework_motive,
        }

        return render(request, "apont/apont2.html", context)

    if request.method == "POST":
        dados_form = request.POST
        id_apont = dados_form["id_apont"]
        apont_type = dados_form["apont_type"]
        motive_value = dados_form["motive_value"]
        machine_id = dados_form["maquina_id"]

        model = select_model_by_machine_id(machine_id)

        apont = Apont_Type.objects.get(apont_type=apont_type)

        motive = None

        if motive_value:
            motive = Motive.objects.get(pk=motive_value)

        data_atual = datetime.datetime.now()
        hora = data_atual.strftime("%H:%M:%S")

        apontamentos = model.objects.get(pk=id_apont)

        apontamentos.hora_inicio_producao = hora  # type: ignore
        apontamentos.tipo_apontamento = apont  # type: ignore
        apontamentos.motivo = motive  # type: ignore
        apontamentos.save()

        return JsonResponse({"Atualizado": "ok"})
    return JsonResponse({"carregado": "Ok"})


def FimProducaoView(request):
    if request.method == "POST":

        dados_form = request.POST

        qtde_boa = dados_form["qtde_boa"]
        qtde_ruim = dados_form["qtde_ruim"]
        id_apont = dados_form["id_apont"]
        maquina_id = dados_form["maquina_id"]

        qtde_refugo = 0
        if qtde_ruim:
            qtde_refugo = qtde_ruim

        data_atual = datetime.datetime.now()
        hora = data_atual.strftime("%H:%M:%S")

        model = select_model_by_machine_id(maquina_id)

        apontamento = model.objects.get(pk=id_apont)
        apontamento.hora_final_producao = hora  # type: ignore
        apontamento.qtde_boa = int(qtde_boa)  # type: ignore
        apontamento.refugo = int(qtde_ruim)  # type: ignore
        apontamento.status = "concluido"  # type:ignore

        apontamento.save()

        apont_id = apontamento.pk

        remover_apontamento(maquina_id, apont_id)

        return JsonResponse({"message": "Dados salvos com sucesso"})
    else:
        return render(request, "apont/index.html")

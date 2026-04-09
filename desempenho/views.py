from datetime import date, timedelta
from django.shortcuts import render
from django.http import JsonResponse
from django.views.generic import View, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Avg, Sum, Count

from desempenho.models import (
    IndicadorDesempenho,
    ResumoDesempenhoSetor,
    ResumoDesempenhoGrupo
)
from desempenho.services import DesempenhoService
from rule.models import Machines, Sectors, Group


class DashboardOEEView(LoginRequiredMixin, TemplateView):
    """Dashboard principal de OEE"""
    template_name = "desempenho/dashboard.html"
    context_object_name = "dados"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        hoje = date.today()

        # KPI's do dia
        indicadores_hoje = IndicadorDesempenho.objects.filter(data=hoje)

        oee_media = indicadores_hoje.aggregate(Avg("oee"))["oee__avg"] or 0
        disponibilidade_media = indicadores_hoje.aggregate(Avg("disponibilidade"))["disponibilidade__avg"] or 0
        performance_media = indicadores_hoje.aggregate(Avg("performance"))["performance__avg"] or 0
        qualidade_media = indicadores_hoje.aggregate(Avg("qualidade"))["qualidade__avg"] or 0

        qtde_maquinas = indicadores_hoje.count()
        qtde_produzida = indicadores_hoje.aggregate(Sum("qtde_produzida"))["qtde_produzida__sum"] or 0
        qtde_refugo = indicadores_hoje.aggregate(Sum("qtde_refugo"))["qtde_refugo__sum"] or 0

        # Máquinas com melhor e pior OEE
        melhor_oee = DesempenhoService.obter_maquinas_com_melhor_oee(hoje, 5)
        pior_oee = DesempenhoService.obter_maquinas_com_pior_oee(hoje, 5)

        # Tendência dos últimos 7 dias
        data_inicio = hoje - timedelta(days=7)
        indicadores_7dias = IndicadorDesempenho.objects.filter(
            data__gte=data_inicio
        ).order_by("data")

        tendencia_oee = []
        for dia in range(7):
            data_dia = data_inicio + timedelta(days=dia)
            oee_dia = indicadores_7dias.filter(data=data_dia).aggregate(Avg("oee"))["oee__avg"] or 0
            tendencia_oee.append({
                "data": data_dia.strftime("%d/%m"),
                "oee": round(oee_dia, 1)
            })

        context.update({
            "oee_media": round(oee_media, 1),
            "disponibilidade_media": round(disponibilidade_media, 1),
            "performance_media": round(performance_media, 1),
            "qualidade_media": round(qualidade_media, 1),
            "qtde_maquinas": qtde_maquinas,
            "qtde_produzida": qtde_produzida,
            "qtde_refugo": qtde_refugo,
            "melhor_oee": melhor_oee,
            "pior_oee": pior_oee,
            "tendencia_oee": tendencia_oee,
            "titulo": "Dashboard OEE",
        })

        return context


class APIDesempenhoMaquinaView(View):
    """API REST que retorna indicadores de uma máquina"""

    def get(self, request, machine_id):
        """
        Retorna indicadores de uma máquina em JSON
        Params: dias (default 7)
        """
        dias = int(request.GET.get("dias", 7))
        
        try:
            machine = Machines.objects.get(pk=machine_id)
        except Machines.DoesNotExist:
            return JsonResponse({"error": "Máquina não encontrada"}, status=404)

        data_inicio = date.today() - timedelta(days=dias)
        indicadores = IndicadorDesempenho.objects.filter(
            machine=machine,
            data__gte=data_inicio
        ).order_by("data")

        dados = {
            "machine": {
                "id": machine.id,
                "code": machine.code,
                "name": machine.name,
                "setor": machine.workStation.sector.name if machine.workStation else "-",
            },
            "indicadores": [
                {
                    "data": ind.data.strftime("%d/%m/%Y"),
                    "oee": round(ind.oee, 2),
                    "disponibilidade": round(ind.disponibilidade, 2),
                    "performance": round(ind.performance, 2),
                    "qualidade": round(ind.qualidade, 2),
                    "qtde_produzida": ind.qtde_produzida,
                    "qtde_refugo": ind.qtde_refugo,
                }
                for ind in indicadores
            ]
        }

        return JsonResponse(dados, safe=False)


class APIDesempenhoSetorView(View):
    """API REST que retorna resumo agregado de um setor"""

    def get(self, request, setor_id):
        """
        Retorna indicadores agregados de um setor em JSON
        Params: dias (default 7)
        """
        dias = int(request.GET.get("dias", 7))
        
        try:
            setor = Sectors.objects.get(pk=setor_id)
        except Sectors.DoesNotExist:
            return JsonResponse({"error": "Setor não encontrado"}, status=404)

        data_inicio = date.today() - timedelta(days=dias)
        resumos = ResumoDesempenhoSetor.objects.filter(
            setor=setor,
            data__gte=data_inicio
        ).order_by("data")

        dados = {
            "setor": {
                "id": setor.id,
                "name": setor.name,
                "grupo": setor.group.name if setor.group else "-",
            },
            "resumos": [
                {
                    "data": res.data.strftime("%d/%m/%Y"),
                    "oee_media": round(res.oee_media, 2),
                    "disponibilidade_media": round(res.disponibilidade_media, 2),
                    "performance_media": round(res.performance_media, 2),
                    "qualidade_media": round(res.qualidade_media, 2),
                    "qtde_maquinas": res.qtde_maquinas,
                    "qtde_produzida_total": res.qtde_produzida_total,
                }
                for res in resumos
            ]
        }

        return JsonResponse(dados, safe=False)


class APIDesempenhoGrupoView(View):
    """API REST que retorna resumo agregado de um grupo"""

    def get(self, request, grupo_id):
        """
        Retorna indicadores agregados de um grupo em JSON
        Params: dias (default 7)
        """
        dias = int(request.GET.get("dias", 7))
        
        try:
            grupo = Group.objects.get(pk=grupo_id)
        except Group.DoesNotExist:
            return JsonResponse({"error": "Grupo não encontrado"}, status=404)

        data_inicio = date.today() - timedelta(days=dias)
        resumos = ResumoDesempenhoGrupo.objects.filter(
            grupo=grupo,
            data__gte=data_inicio
        ).order_by("data")

        dados = {
            "grupo": {
                "id": grupo.id,
                "name": grupo.name,
            },
            "resumos": [
                {
                    "data": res.data.strftime("%d/%m/%Y"),
                    "oee_media": round(res.oee_media, 2),
                    "disponibilidade_media": round(res.disponibilidade_media, 2),
                    "performance_media": round(res.performance_media, 2),
                    "qualidade_media": round(res.qualidade_media, 2),
                    "qtde_maquinas": res.qtde_maquinas,
                    "qtde_setores": res.qtde_setores,
                    "qtde_produzida_total": res.qtde_produzida_total,
                }
                for res in resumos
            ]
        }

        return JsonResponse(dados, safe=False)


class APIDesempenhoHojeView(View):
    """API REST que retorna indicadores consolidados de HOJE"""

    def get(self, request):
        """
        Retorna KPI's agregados do dia em JSON
        """
        hoje = date.today()
        indicadores_hoje = IndicadorDesempenho.objects.filter(data=hoje)

        # Estatísticas consolidadas
        stats = indicadores_hoje.aggregate(
            oee_media=Avg("oee"),
            disp_media=Avg("disponibilidade"),
            perf_media=Avg("performance"),
            qual_media=Avg("qualidade"),
            qtde_maquinas=Count("id"),
            qtde_produzida=Sum("qtde_produzida"),
            qtde_refugo=Sum("qtde_refugo"),
        )

        # Dados por setor
        setores = Sectors.objects.filter(machines__active=True).distinct()
        dados_setores = []
        for setor in setores:
            resumo = ResumoDesempenhoSetor.objects.filter(setor=setor, data=hoje).first()
            if resumo:
                dados_setores.append({
                    "setor": setor.name,
                    "oee": round(resumo.oee_media, 2),
                    "maquinas": resumo.qtde_maquinas,
                })

        dados = {
            "data": hoje.strftime("%d/%m/%Y"),
            "kpis": {
                "oee_media": round(stats["oee_media"] or 0, 2),
                "disponibilidade_media": round(stats["disp_media"] or 0, 2),
                "performance_media": round(stats["perf_media"] or 0, 2),
                "qualidade_media": round(stats["qual_media"] or 0, 2),
            },
            "producao": {
                "qtde_maquinas_ativas": stats["qtde_maquinas"] or 0,
                "qtde_produzida": stats["qtde_produzida"] or 0,
                "qtde_refugo": stats["qtde_refugo"] or 0,
            },
            "setores": dados_setores,
        }

        return JsonResponse(dados, safe=False)

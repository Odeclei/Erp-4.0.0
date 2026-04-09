"""
Django management command para popular resumos de desempenho por setor e grupo.
Calcula agregações baseadas nos indicadores individuais das máquinas.

Uso: python manage.py populate_resumo_desempenho
"""

from datetime import timedelta

from django.core.management.base import BaseCommand
from django.db import transaction
from django.db.models import Avg, Count
from django.utils import timezone

from desempenho.models import (
    IndicadorDesempenho,
    ResumoDesempenhoSetor,
    ResumoDesempenhoGrupo,
)
from rule.models import Machines, Group


class Command(BaseCommand):
    help = "Popular resumos de desempenho por setor e grupo"

    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("📊 Gerando resumos de desempenho..."))
        self.stdout.write("")

        # Parâmetros
        data_final = timezone.now().date()
        data_inicio = data_final - timedelta(days=30)

        # Obter todas as datas com dados
        datas_com_dados = (
            IndicadorDesempenho.objects.filter(data__gte=data_inicio, data__lte=data_final)
            .values_list("data", flat=True)
            .distinct()
            .order_by("data")
        )

        if not datas_com_dados.exists():
            self.stdout.write(
                self.style.ERROR("❌ Nenhum dado de IndicadorDesempenho encontrado!")
            )
            return

        self.stdout.write(
            self.style.SUCCESS(
                f"📅 Processando {datas_com_dados.count()} dias com dados"
            )
        )
        self.stdout.write("")

        # RESUMOS POR SETOR
        self.stdout.write(self.style.WARNING("📍 Agregando por setor..."))
        resumos_setor = 0

        for data in datas_com_dados:
            # Agrupar máquinas por setor
            setores_ids = Machines.objects.filter(
                indicadores_desempenho__data=data
            ).values_list("workStation__sector_id", flat=True).distinct()

            for setor_id in setores_ids:
                # Calcular médias das máquinas do setor para o dia
                agregados = IndicadorDesempenho.objects.filter(
                    machine__workStation__sector_id=setor_id, data=data
                ).aggregate(
                    disponibilidade=Avg("disponibilidade"),
                    performance=Avg("performance"),
                    qualidade=Avg("qualidade"),
                    oee=Avg("oee"),
                    qtde_maquinas=Count("machine", distinct=True),
                    qtde_produzida=Avg("qtde_produzida"),
                )

                # Garantir que todos os valores existem
                for key in ["disponibilidade", "performance", "qualidade", "oee", "qtde_produzida"]:
                    if agregados[key] is None:
                        agregados[key] = 0

                # Obter setor
                setor_obj = Machines.objects.filter(workStation__sector_id=setor_id).first()
                if setor_obj and setor_obj.workStation and setor_obj.workStation.sector:
                    resumo, created = ResumoDesempenhoSetor.objects.update_or_create(
                        setor=setor_obj.workStation.sector,
                        data=data,
                        defaults={
                            "disponibilidade_media": round(agregados["disponibilidade"], 2),
                            "performance_media": round(agregados["performance"], 2),
                            "qualidade_media": round(agregados["qualidade"], 2),
                            "oee_media": round(agregados["oee"], 2),
                            "qtde_maquinas": agregados["qtde_maquinas"],
                            "qtde_produzida_total": int(agregados["qtde_produzida"] * agregados["qtde_maquinas"]),
                        },
                    )
                    if created:
                        resumos_setor += 1

        self.stdout.write(f"   ✓ {resumos_setor} resumos criados por setor")
        self.stdout.write("")

        # RESUMOS POR GRUPO
        self.stdout.write(self.style.WARNING("📍 Agregando por grupo..."))
        resumos_grupo = 0

        for data in datas_com_dados:
            # Agrupar máquinas por grupo
            grupos_ids = Machines.objects.filter(
                indicadores_desempenho__data=data
            ).values_list("workStation__sector__group_id", flat=True).distinct()

            for grupo_id in grupos_ids:
                if not grupo_id:
                    continue
                    
                # Calcular médias das máquinas do grupo para o dia
                agregados = IndicadorDesempenho.objects.filter(
                    machine__workStation__sector__group_id=grupo_id, data=data
                ).aggregate(
                    disponibilidade=Avg("disponibilidade"),
                    performance=Avg("performance"),
                    qualidade=Avg("qualidade"),
                    oee=Avg("oee"),
                    qtde_maquinas=Count("machine", distinct=True),
                    qtde_setores=Count("machine__workStation__sector", distinct=True),
                    qtde_produzida=Avg("qtde_produzida"),
                )

                # Garantir que todos os valores existem
                for key in ["disponibilidade", "performance", "qualidade", "oee", "qtde_produzida"]:
                    if agregados[key] is None:
                        agregados[key] = 0

                # Obter grupo
                grupo = Group.objects.filter(id=grupo_id).first()
                if grupo:
                    resumo, created = ResumoDesempenhoGrupo.objects.update_or_create(
                        grupo=grupo,
                        data=data,
                        defaults={
                            "disponibilidade_media": round(agregados["disponibilidade"], 2),
                            "performance_media": round(agregados["performance"], 2),
                            "qualidade_media": round(agregados["qualidade"], 2),
                            "oee_media": round(agregados["oee"], 2),
                            "qtde_maquinas": agregados["qtde_maquinas"],
                            "qtde_setores": agregados["qtde_setores"],
                            "qtde_produzida_total": int(agregados["qtde_produzida"] * agregados["qtde_maquinas"]),
                        },
                    )
                    if created:
                        resumos_grupo += 1

        self.stdout.write(f"   ✓ {resumos_grupo} resumos criados por grupo")
        self.stdout.write("")

        self.stdout.write(self.style.SUCCESS("✅ Resumos de desempenho populados!"))
        self.stdout.write("")
        self.stdout.write(self.style.WARNING("📊 RESUMO:"))
        self.stdout.write(f"  • Total de resumos por setor: {resumos_setor}")
        self.stdout.write(f"  • Total de resumos por grupo: {resumos_grupo}")
        self.stdout.write(f"  • Período: {data_inicio} até {data_final}")
        self.stdout.write("")
        self.stdout.write(
            self.style.SUCCESS("🚀 Dashboard pronto com agregações completas!")
        )

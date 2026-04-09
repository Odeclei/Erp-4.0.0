"""
Django management command para popular histórico simulado de OEE.
Cria dados reais para os últimos 30 dias - útil para demonstração.

Uso: python manage.py populate_oee_history
"""

import random
from datetime import timedelta

from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from desempenho.models import IndicadorDesempenho
from rule.models import Machines


class Command(BaseCommand):
    help = "Popular histórico simulado de OEE para demonstração"

    @staticmethod
    def _gerar_valor_realista(media: float, variacao: float = 10) -> float:
        """
        Gera valor realista com distribuição normal.

        Args:
            media: Valor médio esperado (0-100)
            variacao: Desvio padrão (0-100)

        Returns:
            Valor entre 0 e 100
        """
        valor = random.gauss(media, variacao)
        return max(0, min(100, valor))

    @staticmethod
    def _gerar_metricas(machine_code: str) -> dict:
        """
        Gera métricas realistas por tipo de máquina.

        Diferentes máquinas têm diferentes eficiências.
        """
        # Perfis de eficiência por máquina
        perfis = {
            "CNC": {"disp": 85, "perf": 90, "qual": 94},  # CNC é confiável
            "TORN": {"disp": 80, "perf": 85, "qual": 91},  # Torno tem mais paradas
            "MONT": {"disp": 75, "perf": 80, "qual": 88},  # Montagem manual é variável
            "AUTO": {
                "disp": 88,
                "perf": 92,
                "qual": 96,
            },  # Linha automática é eficiente
            "PINT": {"disp": 78, "perf": 82, "qual": 85},  # Pintura é sensível
            "LIXA": {"disp": 82, "perf": 86, "qual": 90},  # Lixamento moderado
        }

        # Encontrar o perfil baseado no prefixo do código
        perfil = {"disp": 80, "perf": 85, "qual": 90}  # Padrão
        for prefixo, p in perfis.items():
            if machine_code.startswith(prefixo):
                perfil = p
                break

        return {
            "disponibilidade": Command._gerar_valor_realista(
                perfil["disp"], variacao=8
            ),
            "performance": Command._gerar_valor_realista(perfil["perf"], variacao=7),
            "qualidade": Command._gerar_valor_realista(perfil["qual"], variacao=6),
        }

    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("📊 Gerando histórico simulado de OEE..."))
        self.stdout.write("")

        # Parâmetros
        dias_retroativo = 30  # Últimos 30 dias
        data_final = timezone.now().date()
        data_inicio = data_final - timedelta(days=dias_retroativo)

        # Obter máquinas ativas
        maquinas = Machines.objects.filter(active=True).order_by("code")

        if not maquinas.exists():
            self.stdout.write(self.style.ERROR("❌ Nenhuma máquina ativa encontrada!"))
            return

        self.stdout.write(
            self.style.SUCCESS(
                f"📅 Período: {data_inicio} até {data_final} ({dias_retroativo} dias)"
            )
        )
        self.stdout.write(f"🤖 Máquinas: {maquinas.count()}")
        self.stdout.write("")

        total_registros = 0
        registros_por_maquina = {}

        # Gerar dados para cada máquina e cada dia
        for machine in maquinas:
            registros_criados = 0
            self.stdout.write(f"   {machine.code}: ", ending="")

            data_atual = data_inicio
            while data_atual <= data_final:
                # Gerar métricas realistas
                metricas = self._gerar_metricas(machine.code)

                # Calcular OEE
                oee = (
                    (metricas["disponibilidade"] / 100)
                    * (metricas["performance"] / 100)
                    * (metricas["qualidade"] / 100)
                    * 100
                )

                # Criar ou atualizar indicador
                indicador, created = IndicadorDesempenho.objects.update_or_create(
                    machine=machine,
                    data=data_atual,
                    defaults={
                        "disponibilidade": round(metricas["disponibilidade"], 2),
                        "performance": round(metricas["performance"], 2),
                        "qualidade": round(metricas["qualidade"], 2),
                        "oee": round(oee, 2),
                        # Dados brutos simulados
                        "tempo_total_disponivel_minutos": 540,  # 9 horas
                        "tempo_parado_minutos": int(
                            540 * (100 - metricas["disponibilidade"]) / 100
                        ),
                        "tempo_producao_minutos": int(
                            540 * metricas["disponibilidade"] / 100
                        ),
                        "qtde_programada": random.randint(80, 200),
                        "qtde_produzida": random.randint(70, 195),
                        "qtde_refugo": random.randint(0, 15),
                        "qtde_retrabalho": random.randint(0, 10),
                        "calculado_por": "simulação",
                    },
                )

                if created:
                    registros_criados += 1

                data_atual += timedelta(days=1)

            registros_por_maquina[machine.code] = registros_criados
            total_registros += registros_criados
            self.stdout.write(f"✓ {registros_criados} registros")

        self.stdout.write("")
        self.stdout.write(
            self.style.SUCCESS("✅ Histórico de OEE populado com sucesso!")
        )
        self.stdout.write("")
        self.stdout.write(self.style.WARNING("📈 RESUMO DOS DADOS GERADOS:"))
        self.stdout.write(f"  • Total de registros: {total_registros}")
        self.stdout.write(f"  • Período: {dias_retroativo} dias")
        self.stdout.write(f"  • Máquinas: {maquinas.count()}")
        self.stdout.write("")
        self.stdout.write(self.style.WARNING("📊 Registros por máquina:"))
        for codigo in sorted(registros_por_maquina.keys()):
            qtde = registros_por_maquina[codigo]
            self.stdout.write(f"  • {codigo}: {qtde} registros")
        self.stdout.write("")
        self.stdout.write(self.style.SUCCESS("🚀 Dados prontos para o Dashboard OEE!"))
        self.stdout.write(
            self.style.WARNING(
                "💡 Acesse /desempenho/dashboard/ para visualizar os dados"
            )
        )

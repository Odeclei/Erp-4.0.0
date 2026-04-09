# flake8: noqa
"""
Serviço de cálculo de indicadores de desempenho OEE (Overall Equipment Effectiveness)

OEE = Disponibilidade × Performance × Qualidade

Disponibilidade: Tempo produtivo / Tempo total disponível
Performance: Quantidade produzida / Quantidade teórica
Qualidade: Peças boas / Total de peças produzidas
"""

from datetime import datetime, date, timedelta
from django.db.models import Sum, Avg, Count, Q
from django.db import transaction

from apont.models import RegistroApontamento, Stops
from desempenho.models import (
    IndicadorDesempenho,
    ResumoDesempenhoSetor,
    ResumoDesempenhoGrupo,
)
from rule.models import Machines, Sectors, Group, Turno
from _itens.models import Estrutura


class DesempenhoService:
    """Serviço centralizado para cálculo de indicadores de desempenho"""

    # Padrão: 60 peças/hora (ajustar conforme necessário)
    VELOCIDADE_PRODUCAO_PADRAO = 60.0  # peças/hora
    HORAS_TURNO_PADRAO = 9.0  # 9 horas padrão

    @staticmethod
    def _obter_velocidade_producao(apontamento: RegistroApontamento) -> float:
        """
        Calcula a velocidade de produção esperada para um apontamento específico.
        
        Se o apontamento é de um subproduto (sub-peça):
        - Busca o item acabado relacionado
        - Encontra a quantidade de sub-peças necessárias
        - Calcula: (qtd_item_dia × qtd_subpeça) / 9 horas
        
        Se não tiver subproduto, usa velocidade padrão.
        
        Args:
            apontamento: RegistroApontamento com dados a processar
            
        Returns:
            float: Velocidade em peças/hora
            
        Exemplo:
            Item: Sapato, 100/dia (100/9 = 11.11 pc/hr)
            SubPeça: Pé Traseiro, 2 por Sapato
            Velocidade Pé = (100 × 2) / 9 = 22.22 pc/hr
        """
        try:
            # Se não tem subproduto, usa padrão
            if not apontamento.subproduto:
                return DesempenhoService.VELOCIDADE_PRODUCAO_PADRAO
            
            # Obter informações do subproduto
            sub_item_prog = apontamento.subproduto  # SubItemProgramacao
            item_prog = sub_item_prog.produto_programado  # ItemProgramacao
            item_acabado = item_prog.item  # ItemAcabado
            
            # Obter a quantidade diária do item acabado
            qtd_item_dia = item_acabado.qtd_per_day
            if not qtd_item_dia or qtd_item_dia <= 0:
                return DesempenhoService.VELOCIDADE_PRODUCAO_PADRAO
            
            # Procurar a relação de quantidade na tabela Estrutura
            # (quantas sub-peças são necessárias por item acabado)
            try:
                estrutura = Estrutura.objects.get(
                    item=item_acabado,
                    subitem=sub_item_prog.subproduto
                )
                
                # Determinar qual fase está sendo executada (pré, usinagem ou lixamento)
                # Usar a quantidade apropriada da fase
                qntde_subpeca = estrutura.qntde_usi  # padrão: usinagem
                
                if not qntde_subpeca or qntde_subpeca <= 0:
                    return DesempenhoService.VELOCIDADE_PRODUCAO_PADRAO
                
                # Calcular: quantidade de subpeças por dia / 9 horas
                qtd_subpeca_dia = qtd_item_dia * qntde_subpeca
                velocidade = qtd_subpeca_dia / DesempenhoService.HORAS_TURNO_PADRAO
                
                return velocidade
                
            except Estrutura.DoesNotExist:
                # Se não encontrar relação, usa padrão
                return DesempenhoService.VELOCIDADE_PRODUCAO_PADRAO
                
        except Exception:
            # Em caso de erro, retorna padrão
            return DesempenhoService.VELOCIDADE_PRODUCAO_PADRAO

    @staticmethod
    def calcular_indicadores_maquina(
        machine: Machines, data: date
    ) -> IndicadorDesempenho:
        """
        Calcula todos os indicadores (Disponibilidade, Performance, Qualidade, OEE) para uma máquina em um dia

        Args:
            machine: Instância de Machines
            data: Data para cálculo

        Returns:
            IndicadorDesempenho com os índices calculados
        """
        # Obter todos os apontamentos do dia
        apontamentos = RegistroApontamento.objects.filter(
            machine=machine, data=data, status="concluido"
        )

        # Obter todas as paradas do dia
        paradas = Stops.objects.filter(machine=machine, date__date=data)

        # Calcular tempo disponível do turno
        tempo_total_minutos = DesempenhoService._calcular_tempo_turno(machine, data)

        # 1. DISPONIBILIDADE (Tempo efetivo / Tempo total)
        tempo_parado_segundos = paradas.aggregate(Sum("duration"))["duration__sum"] or 0
        tempo_parado_minutos = tempo_parado_segundos / 60
        tempo_funcional_minutos = tempo_total_minutos - tempo_parado_minutos
        disponibilidade = (
            (tempo_funcional_minutos / tempo_total_minutos * 100)
            if tempo_total_minutos > 0
            else 0
        )

        # 2. PERFORMANCE (Quantidade produzida / Quantidade teórica esperada)
        # Calcular performance de forma precisa iterando por cada apontamento
        # Para considerar a velocidade específica de cada subproduto
        qtde_produzida_total = 0
        qtde_teorica_total = 0
        qtde_programada_total = 0
        tempo_producao_minutos_total = 0
        
        for apontamento in apontamentos:
            # Obter quantidade produzida deste apontamento
            qtde_boa = apontamento.qtde_produzida_boa or 0
            qtde_produzida_total += qtde_boa
            
            # Obter quantidade programada
            qtde_programada_total += apontamento.qtde_programada or 0
            
            # Obter tempo de produção deste apontamento em horas
            tempo_producao_min = apontamento.get_tempo_producao_minutos()
            tempo_producao_minutos_total += tempo_producao_min or 0
            tempo_producao_hrs = tempo_producao_min / 60.0 if tempo_producao_min else 0
            
            # Obter velocidade de produção esperada para este apontamento
            velocidade = DesempenhoService._obter_velocidade_producao(apontamento)
            
            # Calcular quantidade teórica para este apontamento
            qtde_teorica = tempo_producao_hrs * velocidade
            qtde_teorica_total += qtde_teorica
        
        performance = (
            (qtde_produzida_total / qtde_teorica_total * 100)
            if qtde_teorica_total > 0
            else 0
        )

        # 3. QUALIDADE (Peças boas / Total de peças)
        qtde_refugo = (
            apontamentos.aggregate(Sum("qtde_refugo"))["qtde_refugo__sum"] or 0
        )
        qtde_retrabalho = (
            apontamentos.aggregate(Sum("qtde_retrabalho"))["qtde_retrabalho__sum"] or 0
        )
        qtde_total = qtde_produzida_total + qtde_refugo + qtde_retrabalho

        qualidade = (qtde_produzida_total / qtde_total * 100) if qtde_total > 0 else 0

        # 4. OEE
        oee = (disponibilidade / 100) * (performance / 100) * (qualidade / 100) * 100

        # Criar ou atualizar indicador
        indicador, created = IndicadorDesempenho.objects.update_or_create(
            machine=machine,
            data=data,
            defaults={
                "disponibilidade": round(disponibilidade, 2),
                "performance": round(performance, 2),
                "qualidade": round(qualidade, 2),
                "oee": round(oee, 2),
                "tempo_total_disponivel_minutos": tempo_total_minutos,
                "tempo_parado_minutos": tempo_parado_minutos,
                "tempo_producao_minutos": tempo_producao_minutos_total,
                "qtde_programada": qtde_programada_total,
                "qtde_produzida": qtde_produzida_total,
                "qtde_refugo": qtde_refugo,
                "qtde_retrabalho": qtde_retrabalho,
                "calculado_por": "sistema",
            },
        )

        return indicador

    @staticmethod
    def calcular_indicadores_todas_maquinas(data: date) -> int:
        """
        Calcula indicadores para TODAS as máquinas de um dia

        Args:
            data: Data para cálculo

        Returns:
            Quantidade de máquinas processadas
        """
        maquinas = Machines.objects.filter(active=True)
        count = 0

        for machine in maquinas:
            DesempenhoService.calcular_indicadores_maquina(machine, data)
            count += 1

        return count

    @staticmethod
    def calcular_resumo_setor(setor: Sectors, data: date) -> ResumoDesempenhoSetor:
        """
        Calcula resumo agregado de desempenho para um setor

        Args:
            setor: Instância de Sectors
            data: Data para cálculo

        Returns:
            ResumoDesempenhoSetor com médias agregadas
        """
        # Obter todas as máquinas do setor
        maquinas = Machines.objects.filter(workStation__sector=setor, active=True)

        # Obter indicadores de todas as máquinas do setor para a data
        indicadores = IndicadorDesempenho.objects.filter(
            machine__in=maquinas, data=data
        )

        if not indicadores.exists():
            # Se não houver indicadores, calcular para todas as máquinas
            for machine in maquinas:
                DesempenhoService.calcular_indicadores_maquina(machine, data)
            indicadores = IndicadorDesempenho.objects.filter(
                machine__in=maquinas, data=data
            )

        # Calcular médias
        stats = indicadores.aggregate(
            disp_media=Avg("disponibilidade"),
            perf_media=Avg("performance"),
            qual_media=Avg("qualidade"),
            oee_media=Avg("oee"),
            qtde_total=Count("id"),
            qtde_produzida=Sum("qtde_produzida"),
            qtde_programada=Sum("qtde_programada"),
        )

        resumo, created = ResumoDesempenhoSetor.objects.update_or_create(
            setor=setor,
            data=data,
            defaults={
                "disponibilidade_media": round(stats["disp_media"] or 0, 2),
                "performance_media": round(stats["perf_media"] or 0, 2),
                "qualidade_media": round(stats["qual_media"] or 0, 2),
                "oee_media": round(stats["oee_media"] or 0, 2),
                "qtde_maquinas": stats["qtde_total"] or 0,
                "qtde_programada_total": stats["qtde_programada"] or 0,
                "qtde_produzida_total": stats["qtde_produzida"] or 0,
            },
        )

        return resumo

    @staticmethod
    def calcular_resumo_grupo(grupo: Group, data: date) -> ResumoDesempenhoGrupo:
        """
        Calcula resumo agregado de desempenho para um grupo

        Args:
            grupo: Instância de Group
            data: Data para cálculo

        Returns:
            ResumoDesempenhoGrupo com médias agregadas
        """
        # Obter todos os setores do grupo
        setores = Sectors.objects.filter(group=grupo)

        # Calcular resumos de cada setor
        resumos_setores = []
        for setor in setores:
            resumo = DesempenhoService.calcular_resumo_setor(setor, data)
            resumos_setores.append(resumo)

        if not resumos_setores:
            # Se não houver setores, criar um resumo vazio
            resumo, created = ResumoDesempenhoGrupo.objects.update_or_create(
                grupo=grupo,
                data=data,
                defaults={
                    "disponibilidade_media": 0,
                    "performance_media": 0,
                    "qualidade_media": 0,
                    "oee_media": 0,
                    "qtde_maquinas": 0,
                    "qtde_setores": 0,
                    "qtde_produzida_total": 0,
                },
            )
            return resumo

        # Calcular médias dos resumos dos setores
        stats = {
            "disp_media": sum(r.disponibilidade_media for r in resumos_setores)
            / len(resumos_setores),
            "perf_media": sum(r.performance_media for r in resumos_setores)
            / len(resumos_setores),
            "qual_media": sum(r.qualidade_media for r in resumos_setores)
            / len(resumos_setores),
            "oee_media": sum(r.oee_media for r in resumos_setores)
            / len(resumos_setores),
            "qtde_maquinas": sum(r.qtde_maquinas for r in resumos_setores),
            "qtde_setores": len(resumos_setores),
            "qtde_produzida": sum(r.qtde_produzida_total for r in resumos_setores),
        }

        resumo, created = ResumoDesempenhoGrupo.objects.update_or_create(
            grupo=grupo,
            data=data,
            defaults={
                "disponibilidade_media": round(stats["disp_media"], 2),
                "performance_media": round(stats["perf_media"], 2),
                "qualidade_media": round(stats["qual_media"], 2),
                "oee_media": round(stats["oee_media"], 2),
                "qtde_maquinas": stats["qtde_maquinas"],
                "qtde_setores": stats["qtde_setores"],
                "qtde_produzida_total": stats["qtde_produzida"],
            },
        )

        return resumo

    @staticmethod
    def calcular_resumos_todos_grupos(data: date) -> int:
        """
        Calcula resumos para TODOS os grupos de um dia

        Args:
            data: Data para cálculo

        Returns:
            Quantidade de grupos processados
        """
        grupos = Group.objects.all()
        count = 0

        for grupo in grupos:
            DesempenhoService.calcular_resumo_grupo(grupo, data)
            count += 1

        return count

    @staticmethod
    def obter_tendencia_oee_maquina(machine: Machines, dias: int = 7) -> dict:
        """
        Retorna tendência de OEE de uma máquina nos últimos N dias

        Args:
            machine: Instância de Machines
            dias: Quantidade de dias para recuperar (default 7)

        Returns:
            Dict com datas e valores de OEE
        """
        data_inicio = date.today() - timedelta(days=dias)
        indicadores = IndicadorDesempenho.objects.filter(
            machine=machine, data__gte=data_inicio
        ).order_by("data")

        return {
            "machine": machine.code,
            "dados": [
                {
                    "data": ind.data.strftime("%d/%m"),
                    "oee": ind.oee,
                    "disponibilidade": ind.disponibilidade,
                    "performance": ind.performance,
                    "qualidade": ind.qualidade,
                }
                for ind in indicadores
            ],
        }

    @staticmethod
    def obter_maquinas_com_melhor_oee(data: date, limite: int = 5) -> list:
        """
        Retorna as máquinas com melhor OEE em um dia

        Args:
            data: Data para filtro
            limite: Quantidade de máquinas (default 5)

        Returns:
            List de IndicadorDesempenho ordenado por OEE descendente
        """
        return list(
            IndicadorDesempenho.objects.filter(data=data).order_by("-oee")[:limite]
        )

    @staticmethod
    def obter_maquinas_com_pior_oee(data: date, limite: int = 5) -> list:
        """
        Retorna as máquinas com pior OEE em um dia

        Args:
            data: Data para filtro
            limite: Quantidade de máquinas (default 5)

        Returns:
            List de IndicadorDesempenho ordenado por OEE ascendente
        """
        return list(
            IndicadorDesempenho.objects.filter(data=data).order_by("oee")[:limite]
        )

    @staticmethod
    def _calcular_tempo_turno(machine: Machines, data: date) -> float:
        """
        Calcula tempo disponível de trabalho em minutos baseado nos turnos da máquina

        Args:
            machine: Instância de Machines
            data: Data para cálculo

        Returns:
            Tempo total em minutos
        """
        turnos = machine.turnowork.all()

        if not turnos.exists():
            # Se não houver turno configurado, assume 8 horas padrão
            return 480.0  # 8 * 60 minutos

        total_minutos = 0
        for turno in turnos:
            if turno.hora_inicio and turno.hora_fim:
                tempo_turno = (
                    datetime.combine(date.today(), turno.hora_fim)
                    - datetime.combine(date.today(), turno.hora_inicio)
                ).total_seconds() / 60

                # Subtrair almoço se configurado
                if turno.hora_inicio_almoco and turno.hora_fim_almoco:
                    tempo_almoco = (
                        datetime.combine(date.today(), turno.hora_fim_almoco)
                        - datetime.combine(date.today(), turno.hora_inicio_almoco)
                    ).total_seconds() / 60
                    tempo_turno -= tempo_almoco

                total_minutos += tempo_turno

        return max(total_minutos, 0)

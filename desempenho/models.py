from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.timezone import now

from rule.models import Machines, Sectors, WorkStation, Group


class IndicadorDesempenho(models.Model):
    """Indicadores de desempenho consolidados por máquina e data"""

    class Meta:
        verbose_name = "Indicador de Desempenho"
        verbose_name_plural = "Indicadores de Desempenho"
        ordering = ["-data", "machine"]
        unique_together = ("machine", "data")

    # Referência
    machine = models.ForeignKey(
        Machines,
        on_delete=models.CASCADE,
        related_name="indicadores_desempenho",
        verbose_name="Máquina"
    )
    data = models.DateField(verbose_name="Data", default=now)

    # Indicadores calculados (0-100%)
    disponibilidade = models.FloatField(
        verbose_name="Disponibilidade (%)",
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        default=0
    )
    performance = models.FloatField(
        verbose_name="Performance (%)",
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        default=0
    )
    qualidade = models.FloatField(
        verbose_name="Qualidade (%)",
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        default=0
    )
    oee = models.FloatField(
        verbose_name="OEE (%)",
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        default=0
    )

    # Dados brutos para referência
    tempo_total_disponivel_minutos = models.FloatField(default=0, verbose_name="Tempo Total Disponível (min)")
    tempo_parado_minutos = models.FloatField(default=0, verbose_name="Tempo Parado (min)")
    tempo_producao_minutos = models.FloatField(default=0, verbose_name="Tempo Produção (min)")
    qtde_programada = models.IntegerField(default=0, verbose_name="Quantidade Programada")
    qtde_produzida = models.IntegerField(default=0, verbose_name="Quantidade Produzida")
    qtde_refugo = models.IntegerField(default=0, verbose_name="Quantidade Refugo")
    qtde_retrabalho = models.IntegerField(default=0, verbose_name="Quantidade Retrabalho")

    # Auditoria
    calculado_em = models.DateTimeField(auto_now=True, verbose_name="Calculado em")
    calculado_por = models.CharField(max_length=100, default="sistema", verbose_name="Calculado por")

    def __str__(self):
        return f"{self.machine.code} - {self.data.strftime('%d/%m/%Y')} (OEE: {self.oee:.1f}%)"

    @property
    def setor(self):
        """Retorna o setor da máquina"""
        return self.machine.workStation.sector if self.machine.workStation else None

    @property
    def grupo(self):
        """Retorna o grupo do setor"""
        if self.setor:
            return self.setor.group
        return None


class ResumoDesempenhoSetor(models.Model):
    """Resumo agregado de desempenho por setor e data"""

    class Meta:
        verbose_name = "Resumo Setor"
        verbose_name_plural = "Resumos Setor"
        ordering = ["-data", "setor"]
        unique_together = ("setor", "data")

    setor = models.ForeignKey(
        Sectors,
        on_delete=models.CASCADE,
        related_name="resumos_desempenho",
        verbose_name="Setor"
    )
    data = models.DateField(verbose_name="Data", default=now)

    disponibilidade_media = models.FloatField(verbose_name="Disponibilidade Média (%)", default=0)
    performance_media = models.FloatField(verbose_name="Performance Média (%)", default=0)
    qualidade_media = models.FloatField(verbose_name="Qualidade Média (%)", default=0)
    oee_media = models.FloatField(verbose_name="OEE Média (%)", default=0)

    qtde_maquinas = models.IntegerField(default=0, verbose_name="Qty Máquinas")
    qtde_programada_total = models.IntegerField(default=0, verbose_name="Qtde Programada Total")
    qtde_produzida_total = models.IntegerField(default=0, verbose_name="Qtde Produzida Total")

    calculado_em = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.setor.name} - {self.data.strftime('%d/%m/%Y')} (OEE: {self.oee_media:.1f}%)"


class ResumoDesempenhoGrupo(models.Model):
    """Resumo agregado de desempenho por grupo e data"""

    class Meta:
        verbose_name = "Resumo Grupo"
        verbose_name_plural = "Resumos Grupo"
        ordering = ["-data", "grupo"]
        unique_together = ("grupo", "data")

    grupo = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
        related_name="resumos_desempenho",
        verbose_name="Grupo"
    )
    data = models.DateField(verbose_name="Data", default=now)

    disponibilidade_media = models.FloatField(verbose_name="Disponibilidade Média (%)", default=0)
    performance_media = models.FloatField(verbose_name="Performance Média (%)", default=0)
    qualidade_media = models.FloatField(verbose_name="Qualidade Média (%)", default=0)
    oee_media = models.FloatField(verbose_name="OEE Média (%)", default=0)

    qtde_maquinas = models.IntegerField(default=0, verbose_name="Qty Máquinas")
    qtde_setores = models.IntegerField(default=0, verbose_name="Qty Setores")
    qtde_produzida_total = models.IntegerField(default=0, verbose_name="Qtde Produzida Total")

    calculado_em = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.grupo.name} - {self.data.strftime('%d/%m/%Y')} (OEE: {self.oee_media:.1f}%)"

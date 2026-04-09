# flake8: noqa
from django.conf import settings
from django.db import models

from ppcp.models import ItemProgramacao, SubItemProgramacao
from rule.models import Machines


class Apont_Type(models.Model):  # tipo Apontamento Produção
    class Meta:
        verbose_name = "Tipo Apontamento"
        verbose_name_plural = "Tipo Apontamentos"

    apont_type = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.apont_type}"


class Motive(models.Model):  # Motivo de retrabalho
    class Meta:
        verbose_name = "Motivo Retrabalho"
        verbose_name_plural = "Motivo Retrabalhos"

    motive = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.motive}"


class StopsCategory(models.Model):  # Grupo de Parada
    class Meta:
        verbose_name = "Categoria Parada"
        verbose_name_plural = "Categorias Paradas"

    category = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.category}"


class StopsMotive(models.Model):  # Subgrupo de Parada
    class Meta:
        verbose_name = "Subcategoria Parada"
        verbose_name_plural = "Subcategorias Paradas"

    name = models.CharField(max_length=50)
    category = models.ForeignKey(StopsCategory, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name}"


class Stops(models.Model):  # Apontamento de Paradas
    class Meta:
        verbose_name = "Parada de Produção"
        verbose_name_plural = "Paradas de Produção"
        ordering = ["-date"]

    machine = models.ForeignKey(Machines, on_delete=models.CASCADE, related_name="stops")
    date = models.DateTimeField()
    motive = models.ForeignKey(StopsMotive, on_delete=models.SET_NULL, null=True)
    duration = models.PositiveIntegerField()  # valor em segundos
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )

    def __str__(self):
        return f"{self.machine.code} - {self.date.strftime('%d/%m/%Y %H:%M')}"


class RegistroApontamento(models.Model):  # Registro completo de apontamento de produção
    class Meta:
        verbose_name = "Apontamento de Produção"
        verbose_name_plural = "Apontamentos de Produção"
        ordering = ["-data"]
        unique_together = ("machine", "data", "hora_inicio_producao")

    STATUS_CHOICES = [
        ("aberto", "Aberto"),
        ("concluido", "Concluído"),
        ("cancelado", "Cancelado"),
    ]

    machine = models.ForeignKey(Machines, on_delete=models.CASCADE, related_name="apontamentos")
    data = models.DateField(verbose_name="Data do Apontamento")
    
    # Referência à programação
    programacao = models.ForeignKey(
        ItemProgramacao, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        verbose_name="Ordem de Produção"
    )
    subproduto = models.ForeignKey(
        SubItemProgramacao,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="SubItem/Componente"
    )

    # Tempos
    hora_inicio_setup = models.TimeField(verbose_name="Hora Início Setup", null=True, blank=True)
    hora_fim_setup = models.TimeField(verbose_name="Hora Fim Setup", null=True, blank=True)
    hora_inicio_producao = models.TimeField(verbose_name="Hora Início Produção", null=True, blank=True)
    hora_fim_producao = models.TimeField(verbose_name="Hora Fim Produção", null=True, blank=True)

    # Quantidades
    qtde_programada = models.IntegerField(verbose_name="Quantidade Programada", default=0)
    qtde_produzida_boa = models.IntegerField(verbose_name="Quantidade Produzida (Boa)", default=0)
    qtde_refugo = models.IntegerField(verbose_name="Quantidade Refugo", default=0)
    qtde_retrabalho = models.IntegerField(verbose_name="Quantidade Retrabalho", default=0)

    # Classificação
    tipo_apontamento = models.ForeignKey(
        "Apont_Type", 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        verbose_name="Tipo de Apontamento"
    )
    motivo_retrabalho = models.ForeignKey(
        "Motive", 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        verbose_name="Motivo do Retrabalho"
    )

    # Observações
    observacoes = models.TextField(blank=True, null=True, verbose_name="Observações")
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="aberto",
        verbose_name="Status"
    )

    # Auditoria
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Usuário"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.machine.code} - {self.data} - {self.qtde_produzida_boa} peças"

    def get_tempo_setup_minutos(self):
        """Retorna tempo de setup em minutos"""
        if self.hora_inicio_setup and self.hora_fim_setup:
            from datetime import datetime
            tempo = datetime.combine(self.data, self.hora_fim_setup) - datetime.combine(self.data, self.hora_inicio_setup)
            return tempo.total_seconds() / 60
        return 0

    def get_tempo_producao_minutos(self):
        """Retorna tempo de produção em minutos"""
        if self.hora_inicio_producao and self.hora_fim_producao:
            from datetime import datetime
            tempo = datetime.combine(self.data, self.hora_fim_producao) - datetime.combine(self.data, self.hora_inicio_producao)
            return tempo.total_seconds() / 60
        return 0

    def get_tempo_total_minutos(self):
        """Retorna tempo total (setup + produção) em minutos"""
        return self.get_tempo_setup_minutos() + self.get_tempo_producao_minutos()

    def get_total_refugo_retrabalho(self):
        """Retorna total de peças não-conformes"""
        return self.qtde_refugo + self.qtde_retrabalho

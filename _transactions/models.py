from django.db import models
from django.conf import settings
from rule.models import WorkStation
from _operadores.models import Operator
from _itens.models import ItemAcabado
from _resources.models import ApontType, MotivoRetrabalho


class Apontamentos(models.Model):
    class Meta:
        verbose_name = "Apontamento"
        verbose_name_plural = "Apontamentos"

    date = models.DateTimeField(auto_now_add=True)
    workstation = models.ForeignKey(
        WorkStation, on_delete=models.CASCADE, null=True, blank=True
    )
    operador = models.ForeignKey(
        Operator,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="apont_operador",
    )
    produto = models.ForeignKey(
        ItemAcabado, on_delete=models.CASCADE, null=True, blank=True
    )
    qtde_boa = models.FloatField(default=0)
    qtde_refugo = models.FloatField(default=0)
    tipo_apontamento = models.ForeignKey(
        ApontType, on_delete=models.CASCADE, null=True, blank=True
    )
    datetime_start = models.DateTimeField(null=True, blank=True)
    datetime_end = models.DateTimeField(null=True, blank=True)
    duration = models.DurationField(null=True, blank=True)
    tempo_hr = models.FloatField(default=0)
    tempo_seg = models.FloatField(default=0)
    code_read = models.CharField(max_length=100, null=True, blank=True)
    programacao_ppcp = models.CharField(max_length=100, null=True, blank=True)
    programacao_comercial = models.CharField(max_length=100, null=True, blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="apont_created_by",
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="apont_updated_by",
    )
    updated_at = models.DateTimeField(auto_now=True)
    afeta_oee = models.BooleanField(default=True)
    show_relatorio = models.BooleanField(default=True)
    observations = models.TextField(null=True, blank=True)
    concluido = models.BooleanField(default=False)


class Stops(models.Model):
    class Meta:
        verbose_name = "Parada"
        verbose_name_plural = "Paradas"

    date = models.DateTimeField(auto_now_add=True)
    workstation = models.ForeignKey(WorkStation, on_delete=models.CASCADE)
    motivo_parada = models.ForeignKey(MotivoRetrabalho, on_delete=models.CASCADE)
    datetime_start = models.DateTimeField()
    datetime_end = models.DateTimeField()
    duration = models.DurationField()
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="stop_created_by",
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="stop_updated_by",
    )
    updated_at = models.DateTimeField(auto_now=True)
    observations = models.TextField(null=True, blank=True)

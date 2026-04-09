from datetime import datetime

from django.conf import settings
from django.db import models
from django.utils.timezone import now

from _itens.models import ItemAcabado
from _itens.models import ItemBase

# Create your models here.


class StatusOrder(models.Model):
    class Meta:
        verbose_name = "Status Programação"
        verbose_name_plural = "Status Programações"

    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


def get_current_year():
    return now().strftime("%y")


class ManufacturingOrder(models.Model):
    order_date = datetime.now()
    # order_year = order_date.strftime("%y")

    order_number = models.CharField(
        max_length=4, null=True, blank=True, verbose_name="Ordem Produção", unique=True
    )
    prog_year = models.CharField(
        max_length=2,
        verbose_name="Ano da Programação",
        help_text="Digitar somente 2 dígitos do ano.",
        null=True,
        blank=True,
        default=get_current_year,
    )
    description = models.TextField(verbose_name="Descrição", null=True, blank=True)
    status = models.ForeignKey(
        StatusOrder, on_delete=models.SET_NULL, null=True, default=None
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="order_created_by",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    changed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="order_updated_by",
    )
    changed_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.order_number


class ItemProgramacao(models.Model):
    item = models.ForeignKey(
        ItemAcabado, on_delete=models.CASCADE, null=True, blank=True
    )
    programacao = models.ForeignKey(
        ManufacturingOrder, on_delete=models.CASCADE, null=True, blank=True
    )
    quantidade = models.PositiveIntegerField()
    start_at = models.DateField(
        blank=True, null=True, verbose_name="Data Prevista Início"
    )
    ends_at = models.DateField(blank=True, null=True, verbose_name="Data Prevista Fim")

    class Meta:
        verbose_name = "Item Programado"
        verbose_name_plural = "Itens Programados"

    def __str__(self):
        item = f"{self.item}"
        return item


class SubItemProgramacao(models.Model):
    class Meta:
        verbose_name = "SubItem Programado"
        verbose_name_plural = "SubItens Programados"

    produto_programado = models.ForeignKey(
        ItemProgramacao, on_delete=models.CASCADE, null=True, blank=True
    )
    subproduto = models.ForeignKey(
        ItemBase, on_delete=models.CASCADE, null=True, blank=True
    )
    programacao = models.ForeignKey(
        ManufacturingOrder, on_delete=models.CASCADE, null=True, blank=True
    )
    qtde_pre = models.PositiveIntegerField(blank=True, null=True)
    qtde_usi = models.PositiveIntegerField(blank=True, null=True)
    qtde_lix = models.PositiveIntegerField(blank=True, null=True)

    def __str__(self):
        desc = f"{self.subproduto}"

        return desc


class Estoque(models.Model):
    item = models.ForeignKey(
        ItemAcabado, on_delete=models.CASCADE, null=True, blank=True
    )
    qtde = models.IntegerField()
    local = models.CharField(max_length=50)

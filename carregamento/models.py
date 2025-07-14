from django.db import models

from cad_item.models import Finish, Item
from clientes.models import Clientes


class Proformas(models.Model):
    class Meta:
        verbose_name = 'Proforma'
        verbose_name_plural = 'Proformas'

    proforma_number = models.CharField(
        max_length=50, unique=True,
    )
    cliente = models.ForeignKey(
        Clientes, on_delete=models.DO_NOTHING
    )
    container_number = models.CharField(
        max_length=50, default=None, null=True, blank=True,
    )
    lacre_number = models.CharField(
        max_length=50, default=None, null=True, blank=True,
    )

    def __str__(self) -> str:
        prof = f'{self.proforma_number} - {self.cliente}'
        return prof


class ItemProforma(models.Model):
    class Meta:
        verbose_name = 'Item Proforma'
        verbose_name_plural = 'Itens Proforma'

    proforma = models.ForeignKey(
        Proformas, on_delete=models.DO_NOTHING
    )
    item = models.ForeignKey(
        Item, on_delete=models.DO_NOTHING
    )
    finish = models.ForeignKey(
        Finish, on_delete=models.DO_NOTHING
    )
    quantity = models.IntegerField()


class Carregamento(models.Model):
    class Meta:
        verbose_name = 'Carregamento'
        verbose_name_plural = 'Carregamentos'

    proforma_data = models.ForeignKey(Proformas, on_delete=models.DO_NOTHING)
    item = models.ForeignKey(ItemProforma, on_delete=models.DO_NOTHING)
    data_inicio = models.DateTimeField(
        auto_now_add=True)
    data_fim = models.DateTimeField(
        auto_now=True)
    qtde_carregada = models.IntegerField()

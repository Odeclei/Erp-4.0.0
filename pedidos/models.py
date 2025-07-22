from enum import auto
from django.db import models

# Create your models here.
from cad_item.models import Finish, Item
from clientes.models import Clientes


class Pedidos(models.Model):
    class Meta:
        verbose_name = "Pedido"
        verbose_name_plural = "Pedidos"

    STATUS_CHOICES = [
        ("OPE", "Aberto"),
        ("LOD", "Carregando"),
        ("CAN", "Cancelado"),
        ("FIN", "Concluído"),
    ]

    pedido_number = models.CharField(
        max_length=50,
        unique=True,
    )
    pedido_cliente = models.CharField(
        max_length=50,
        default="--",
        null=True,
        blank=True,
    )
    cliente = models.ForeignKey(Clientes, on_delete=models.DO_NOTHING)
    cargo_number = models.CharField(
        max_length=50,
        default="--",
        null=True,
        blank=True,
    )
    lacre_number = models.CharField(
        max_length=50,
        default="--",
        null=True,
        blank=True,
    )
    status = models.CharField(
        max_length=3,  # Ajuste o tamanho máximo se as siglas forem maiores
        choices=STATUS_CHOICES,
        default="OPE",
        verbose_name="Status",
    )
    data_inicio = models.DateTimeField(null=True, blank=True)
    data_fim = models.DateTimeField(null=True, blank=True)

    def __str__(self) -> str:
        prof = f"{self.pedido_number} - {self.cliente}"
        return prof


class ItemPedido(models.Model):
    class Meta:
        verbose_name = "Item Pedido"
        verbose_name_plural = "Itens Pedidos"

    proforma = models.ForeignKey(Pedidos, on_delete=models.DO_NOTHING)
    item = models.ForeignKey(Item, on_delete=models.DO_NOTHING)
    finish = models.ForeignKey(Finish, on_delete=models.DO_NOTHING)
    quantity = models.IntegerField()

    def __str__(self) -> str:
        prof = f"{self.proforma.pedido_number} - {self.item.name_prod}"
        return prof

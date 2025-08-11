from django.db import models
from pedidos.models import Pedidos, ItemPedido


class Carregamento(models.Model):
    class Meta:
        verbose_name = "Carregamento"
        verbose_name_plural = "Carregamentos"

    pedido_data = models.ForeignKey(Pedidos, on_delete=models.DO_NOTHING)
    item = models.ForeignKey(ItemPedido, on_delete=models.DO_NOTHING)
    data_inicio = models.DateTimeField(auto_now_add=True)
    data_fim = models.DateTimeField(blank=True, null=True)
    qtde_carregada = models.FloatField(default=0, null=True, blank=True)
    operador = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        cargo_name = f"{self.pedido_data.pedido_number} - {self.pedido_data.cliente}"
        return cargo_name


class BarcodeProcessed(models.Model):
    class Meta:
        verbose_name = "Código Processado"
        verbose_name_plural = "Códigos Processados"
        ordering = ["-data_processado"]
        indexes = [
            models.Index(fields=["item"]),
            models.Index(fields=["carregamento"]),
        ]

    codigo_completo = models.CharField(max_length=100, unique=True)
    carregamento = models.ForeignKey(
        Carregamento,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="processsed_barcodes",
    )
    item = models.ForeignKey(
        ItemPedido, on_delete=models.SET_NULL, null=True, blank=True
    )
    data_processado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.codigo_completo

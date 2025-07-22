from django.db import models
from pedidos.models import Pedidos, ItemPedido


class Carregamento(models.Model):
    class Meta:
        verbose_name = "Carregamento"
        verbose_name_plural = "Carregamentos"

    pedido_data = models.ForeignKey(Pedidos, on_delete=models.DO_NOTHING)
    item = models.ForeignKey(ItemPedido, on_delete=models.DO_NOTHING)
    data_inicio = models.DateTimeField(auto_now_add=True)
    data_fim = models.DateTimeField(auto_now=True)
    qtde_carregada = models.IntegerField()
    operador = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        cargo_name = f"{self.pedido_data.pedido_number} - {self.pedido_data.cliente}"
        return cargo_name

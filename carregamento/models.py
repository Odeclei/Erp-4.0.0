from django.db import models
from pedidos.models import Pedidos, ItemPedido


class Carregamento(models.Model):
    class Meta:
        verbose_name = "Carregamento"
        verbose_name_plural = "Carregamentos"

    proforma_data = models.ForeignKey(Pedidos, on_delete=models.DO_NOTHING)
    item = models.ForeignKey(ItemPedido, on_delete=models.DO_NOTHING)
    data_inicio = models.DateTimeField(auto_now_add=True)
    data_fim = models.DateTimeField(auto_now=True)
    qtde_carregada = models.IntegerField()

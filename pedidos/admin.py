from django.contrib import admin
from clientes.views import PER_PAGE
from pedidos import models
from import_export import resources
from import_export.admin import ImportExportModelAdmin

# Register your models here.


class PedidoResource(resources.ModelResource):
    class Meta:
        model = models.Pedidos


class ItemPedidoResource(resources.ModelResource):
    class Meta:
        model = models.ItemPedido


@admin.register(models.Pedidos)
class PedidosAdmin(ImportExportModelAdmin):
    resource_classes = [PedidoResource]
    list_display = (
        "id",
        "pk",
        "pedido_number",
        "cliente",
        "pedido_cliente",
        "status",
        "pedido_editable",
    )
    ordering = ("-pedido_number",)
    list_editable = (
        "status",
        "pedido_editable",
    )
    search_fields = (
        "pedido_number",
        "pedido_cliente",
        "cliente",
    )
    list_per_page = PER_PAGE
    list_filter = ("status",)
    ordering = ("-pedido_number",)


@admin.register(models.ItemPedido)
class ItemProformaAdmin(ImportExportModelAdmin):
    resource_classes = [ItemPedidoResource]
    list_display = (
        "id",
        "proforma",
        "item",
        "finish",
        "quantity",
    )
    list_editable = ("quantity",)
    list_display_links = (
        "id",
        "proforma",
    )
    list_per_page = PER_PAGE
    list_filter = ("proforma",)
    search_fields = (
        "proforma",
        "item",
    )

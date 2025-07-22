from django.contrib import admin
from clientes.views import PER_PAGE
from pedidos import models

# Register your models here.


@admin.register(models.Pedidos)
class ProformasAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "pk",
        "pedido_number",
        "cliente",
        "pedido_cliente",
        "status",
    )
    ordering = ("-pedido_number",)
    list_editable = ("status",)
    search_fields = (
        "pedido_number",
        "pedido_cliente",
        "cliente",
    )
    list_per_page = PER_PAGE
    list_filter = ("status",)
    ordering = ("-pedido_number",)


@admin.register(models.ItemPedido)
class ItemProformaAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "proforma",
        "item",
        "finish",
        "quantity",
    )
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

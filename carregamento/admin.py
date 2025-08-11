from django.contrib import admin

from carregamento import models


@admin.register(models.Carregamento)
class CarregamentoAdmin(admin.ModelAdmin):
    list_display = ("pk", "pedido_data", "item", "qtde_carregada", "operador")
    list_display_links = ("pedido_data",)
    list_per_page = 50
    list_filter = ("pedido_data__status",)
    search_fields = (
        "pedido_data__pedido_number",
        "pedido_data__pedido_cliente",
        "pedido_data__cliente__nome_fantasia",
        "item__item__item_cod",
        "item__item__name_abrev",
    )


@admin.register(models.BarcodeProcessed)
class BarcodeProcessedAdmin(admin.ModelAdmin):
    list_display = ("codigo_completo", "data_processado")

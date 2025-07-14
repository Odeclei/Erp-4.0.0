from django.contrib import admin

from carregamento import models


@admin.register(models.Proformas)
class ProformasAdmin(admin.ModelAdmin):
    list_display = 'proforma_number', 'cliente'
    ordering = '-proforma_number',
    search_fields = (
        'proforma_number', 'cliente',
    )


@admin.register(models.ItemProforma)
class ItemProformaAdmin(admin.ModelAdmin):
    ...


@admin.register(models.Carregamento)
class CarregamentoAdmin(admin.ModelAdmin):
    ...

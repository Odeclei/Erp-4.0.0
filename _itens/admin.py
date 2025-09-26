from pyexpat import model
from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from _itens import models


class FamilyResource(resources.ModelResource):
    class Meta:
        model = models.FamilyProd


@admin.register(models.FamilyProd)
class FamilyProdAdmin(ImportExportModelAdmin):
    resources_classes = [FamilyResource]
    list_display = (
        "refer",
        "name",
    )
    search_fields = (
        "refer",
        "name",
    )
    ordering = ("refer",)


class ItemResource(resources.ModelResource):
    class Meta:
        model = models.ItemAcabado


class EstruturainLine(admin.TabularInline):
    model = models.Estrutura
    extra = 1


@admin.register(models.ItemAcabado)
class ItemAcabadoAdmin(ImportExportModelAdmin):
    resource_classes = [ItemResource]
    list_display = (
        "item_cod",
        "item_name",
        "qtd_per_day",
        "is_active",
    )
    search_fields = (
        "item_cod",
        "item_name",
    )
    ordering = ("item_cod",)
    list_editable = (
        "qtd_per_day",
        "is_active",
    )
    inlines = [EstruturainLine]

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.select_related("family", "created_by", "updated_by")
        queryset = queryset.prefetch_related("subitens")
        return queryset


@admin.register(models.ComponentesGroup)
class ComponentesGroupAdmin(admin.ModelAdmin):
    list_display = ("group", "name")


@admin.register(models.Componentes)
class ComponentesAdmin(admin.ModelAdmin):
    list_display = (
        "codigo",
        "name",
        "unidade_medida",
    )


class ItemBaseResource(resources.ModelResource):
    class Meta:
        model = models.ItemBase


@admin.register(models.ItemBase)
class ItemBaseAdmin(ImportExportModelAdmin):
    list_display = (
        "itembase_cod",
        "itembase_name",
        "ficha_tecnica",
        "variation",
        "componente",
        "comprimento",
        "largura",
        "espessura",
    )
    resource_classes = [ItemBaseResource]
    search_fields = (
        "itembase_cod",
        "itembase_name",
    )
    ordering = ("-itembase_cod",)

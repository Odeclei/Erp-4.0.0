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


@admin.register(models.ItemAcabado)
class ItemAcabadoAdmin(ImportExportModelAdmin):
    resource_classes = [ItemResource]

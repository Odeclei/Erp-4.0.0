from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from cad_item import models


class Childinline(admin.TabularInline):
    model = models.Estrutura
    extra = 1


@admin.register(models.FamilyProd)
class FamilyProdAdmin(admin.ModelAdmin):
    list_display = ("description",)
    ordering = ("description",)


class ItemResource(resources.ModelResource):
    class Meta:
        model = models.Item


@admin.register(models.Item)
class ItemAdmin(ImportExportModelAdmin):
    resource_classes = [ItemResource]
    list_display = (
        "pk",
        "item_cod",
        "name_prod",
        "is_active",
        "qtde_volume"
    )
    list_editable = ('qtde_volume',)
    ordering = ("-pk",)
    search_fields = (
        "item_cod",
        "name_prod",
    )
    list_per_page = 50
    list_filter = (
        "family",
        "is_active",
    )
    readonly_fields = (
        "created_at",
        "created_by",
        "updated_at",
        "updated_by",
    )
    inlines = [Childinline]

    def save_model(self, request, obj, form, change):
        if change:
            obj.updated_by = request.user
        else:
            obj.created_by = request.user
        obj.save()


class MaterialResource(resources.ModelResource):
    class Meta:
        model = models.Material


@admin.register(models.Material)
class MaterialAdmin(ImportExportModelAdmin):
    resource_classes = [MaterialResource]


class SubitemResource(resources.ModelResource):
    class Meta:
        model = models.SubItem


@admin.register(models.SubItem)
class SubItemAdmin(ImportExportModelAdmin):
    resource_classes = [SubitemResource]
    list_display = (
        "subitem_cod",
        "name_subitem",
        "is_active",
    )
    ordering = ("-subitem_cod",)
    search_fields = (
        "subitem_cod",
        "name_subitem",
    )
    list_per_page = 50


@admin.register(models.Estrutura)
class EstruturaAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "item",
        "subitem",
        "qntde_pre",
        "qntde_usi",
        "qntde_lix",
    )


@admin.register(models.Finish)
class FinishAdmin(admin.ModelAdmin):
    list_display = (
        "code_finish",
        "name_finish",
    )

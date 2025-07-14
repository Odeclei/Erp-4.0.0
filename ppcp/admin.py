# flake8: noqa
from django.contrib import admin

from ppcp import models

# Register your models here.


@admin.register(models.StatusOrder)
class StatusOrderAdmin(admin.ModelAdmin):
    ...


@admin.register(models.ManufacturingOrder)
class ManufacturingOrderAdmin(admin.ModelAdmin):
    list_display = 'order_number', 'description', 'status',
    ordering = '-pk',
    search_fields = 'order_number',
    list_filter = 'status',

    def save_model(self, request, obj, form, change):
        if change:
            obj.order_updated_by = request.user
        else:
            obj.order_created_by = request.user
        obj.save()


@admin.register(models.ItemProgramacao)
class ItemProgramacaoAdmin(admin.ModelAdmin):
    list_display = (
        'pk', 'id', 'item', 'programacao', 'quantidade', 'start_at', 'ends_at',
    )


@admin.register(models.SubItemProgramacao)
class SubItemProgramacaoAdmin(admin.ModelAdmin):
    list_display = 'pk', 'id', 'produto_programado', 'subproduto', 'programacao'

from django.contrib import admin

from _resources import models


# Register your models here.
@admin.register(models.Unidade_Medida)
class UnidadeMedidaAdmin(admin.ModelAdmin):
    list_display = ("sigla", "descricao")
    search_fields = ("sigla", "descricao")
    ordering = ("sigla",)

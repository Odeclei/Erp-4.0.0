# flake8: noqa
from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from clientes import models
from clientes.views import PER_PAGE

# Register your models here.


class ClientesResource(models.ClientesResource):
    class Meta:
        model = models.Clientes


@admin.register(models.Clientes)
class ClientesAdmin(ImportExportModelAdmin):
    resource_classes = [ClientesResource]
    list_display = (
        "id",
        "nome_fantasia",
        "market",
    )
    list_display_links = (
        "id",
        "nome_fantasia",
    )
    list_per_page = PER_PAGE
    search_fields = (
        "cnpj",
        "nome_fantasia",
        "razao_social",
    )
    list_filter = ("market",)
    ordering = ("nome_fantasia",)

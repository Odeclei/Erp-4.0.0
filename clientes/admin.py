# flake8: noqa
from django.contrib import admin

from clientes import models

# Register your models here.


@admin.register(models.Clientes)
class ClientesAdmin(admin.ModelAdmin):
    list_display = 'nome_fantasia', 'market',
    search_fields = 'cnpj', 'nome_fantasia', 'razao_social',
    list_filter = 'market',
    ordering = 'nome_fantasia',

    
from django.contrib import admin

from carregamento import models


@admin.register(models.Carregamento)
class CarregamentoAdmin(admin.ModelAdmin): ...

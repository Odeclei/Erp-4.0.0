
from django.contrib import admin

from rule import models


# Register your models here.
@admin.register(models.Company)
class CompanyAdmin(admin.ModelAdmin):
    ...


@admin.register(models.Sectors)
class SectorAdmin(admin.ModelAdmin):
    ...


@admin.register(models.Turno)
class TurnoAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'hora_inicio', 'hora_inicio_almoco',
                    'hora_fim_almoco',)
    ordering = '-pk',


@admin.register(models.Machines)
class MachinesAdmin(admin.ModelAdmin):
    list_display = 'code', 'name', 'sector'
    ordering = 'code',


@admin.register(models.MacId)
class MacIdAdmin(admin.ModelAdmin):
    list_display = 'mac_id', 'name', 'machine',
    search_fields = 'mac_id', 'name', 'machine',

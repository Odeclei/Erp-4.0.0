from django.contrib import admin

from rule import models


# Register your models here.
@admin.register(models.Company)
class CompanyAdmin(admin.ModelAdmin): ...


@admin.register(models.Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "company",
    )


@admin.register(models.Sectors)
class SectorAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "group",
    )


@admin.register(models.WorkStation)
class WorkStationAdmin(admin.ModelAdmin):
    list_display = (
        "description",
        "sector",
        "active",
    )
    list_editable = ("active",)
    list_filter = ("sector", "active")


@admin.register(models.Machines)
class MachinesAdmin(admin.ModelAdmin):
    list_display = "code", "name", "workStation"
    list_filter = "workStation", "turnowork"
    ordering = ("code",)


@admin.register(models.Turno)
class TurnoAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "name",
        "hora_inicio",
        "hora_fim",
        "hora_inicio_almoco",
        "hora_fim_almoco",
    )
    ordering = ("-pk",)


@admin.register(models.MacId)
class MacIdAdmin(admin.ModelAdmin):
    list_display = (
        "mac_id",
        "name",
        "machine",
        "workstation",
    )
    search_fields = (
        "mac_id",
        "name",
        "workstation",
    )

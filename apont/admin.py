from django.contrib import admin
from django.utils.html import format_html
from apont import models


@admin.register(models.Apont_Type)
class Apont_TypeAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Motive)
class MotiveAdmin(admin.ModelAdmin):
    pass


@admin.register(models.StopsCategory)
class StopsCategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(models.StopsMotive)
class StopsMotiveAdmin(admin.ModelAdmin):
    list_display = ("name", "category")
    ordering = ("category", "name")


@admin.register(models.Stops)
class StopsAdmin(admin.ModelAdmin):
    list_display = ("machine", "data_formatada", "motive", "duracao_minutos", "user")
    list_filter = ("date", "machine__workStation__sector", "machine", "motive__category")
    search_fields = ("machine__code", "machine__name")
    date_hierarchy = "date"
    ordering = ("-date",)

    fieldsets = (
        (
            "Informações Básicas",
            {"fields": ("machine", "date", "motive", "duration")},
        ),
        (
            "Auditoria",
            {"fields": ("user",), "classes": ("collapse",)},
        ),
    )

    def data_formatada(self, obj):
        return obj.date.strftime("%d/%m/%Y %H:%M")

    data_formatada.short_description = "Data/Hora"

    def duracao_minutos(self, obj):
        minutos = obj.duration / 60
        return f"{minutos:.1f} min"

    duracao_minutos.short_description = "Duração"


@admin.register(models.RegistroApontamento)
class RegistroApontamentoAdmin(admin.ModelAdmin):
    list_display = (
        "machine",
        "data",
        "qtde_colored",
        "qualidade_colored",
        "status",
        "user",
    )
    list_filter = ("data", "machine__workStation__sector", "machine", "status")
    search_fields = ("machine__code", "machine__name")
    readonly_fields = ("created_at", "updated_at")
    date_hierarchy = "data"
    ordering = ("-data", "-created_at")

    fieldsets = (
        (
            "Informações Básicas",
            {
                "fields": (
                    "machine",
                    "data",
                    "programacao",
                    "subproduto",
                    "status",
                )
            },
        ),
        (
            "Tempos",
            {
                "fields": (
                    "hora_inicio_setup",
                    "hora_fim_setup",
                    "hora_inicio_producao",
                    "hora_fim_producao",
                ),
                "classes": ("collapse",),
            },
        ),
        (
            "Quantidades",
            {
                "fields": (
                    "qtde_programada",
                    "qtde_produzida_boa",
                    "qtde_refugo",
                    "qtde_retrabalho",
                ),
            },
        ),
        (
            "Classificação",
            {
                "fields": (
                    "tipo_apontamento",
                    "motivo_retrabalho",
                ),
            },
        ),
        (
            "Observações",
            {
                "fields": ("observacoes",),
                "classes": ("collapse",),
            },
        ),
        (
            "Auditoria",
            {
                "fields": ("user", "created_at", "updated_at"),
                "classes": ("collapse",),
            },
        ),
    )

    def qtde_colored(self, obj):
        """Exibe quantidade produzida com cor"""
        if obj.qtde_produzida_boa > 0:
            return format_html(
                '<span style="color: green; font-weight: bold;">{} ✓</span>',
                obj.qtde_produzida_boa,
            )
        return "-"

    qtde_colored.short_description = "Qtde Boa"

    def qualidade_colored(self, obj):
        """Exibe taxa de qualidade com cor"""
        total = obj.qtde_produzida_boa + obj.qtde_refugo + obj.qtde_retrabalho
        if total > 0:
            qualidade_pct = (obj.qtde_produzida_boa / total) * 100
            if qualidade_pct >= 95:
                color = "green"
            elif qualidade_pct >= 80:
                color = "orange"
            else:
                color = "red"

            return format_html(
                '<span style="color: {}; font-weight: bold;">{:.1f}%</span>',
                color,
                qualidade_pct,
            )
        return "-"

    qualidade_colored.short_description = "Qualidade"

from django.contrib import admin
from django.utils.html import format_html
from desempenho.models import (
    IndicadorDesempenho,
    ResumoDesempenhoSetor,
    ResumoDesempenhoGrupo
)
from desempenho.services import DesempenhoService


def recalcular_oee(modeladmin, request, queryset):
    """Action para recalcular OEE dos indicadores selecionados"""
    count = 0
    for indicador in queryset:
        DesempenhoService.calcular_indicadores_maquina(indicador.machine, indicador.data)
        count += 1
    modeladmin.message_user(request, f"{count} indicadores recalculados com sucesso!")


recalcular_oee.short_description = "🔄 Recalcular OEE selecionado"


@admin.register(IndicadorDesempenho)
class IndicadorDesempenhoAdmin(admin.ModelAdmin):
    list_display = (
        "machine",
        "data",
        "oee_colored",
        "disponibilidade",
        "performance",
        "qualidade",
        "qtde_produzida",
        "qtde_refugo",
    )
    list_filter = ("data", "machine__workStation__sector", "machine")
    search_fields = ("machine__code", "machine__name")
    readonly_fields = (
        "disponibilidade",
        "performance",
        "qualidade",
        "oee",
        "tempo_total_disponivel_minutos",
        "tempo_parado_minutos",
        "tempo_producao_minutos",
        "qtde_programada",
        "qtde_produzida",
        "qtde_refugo",
        "qtde_retrabalho",
        "calculado_em",
    )
    date_hierarchy = "data"
    ordering = ("-data", "machine")
    actions = [recalcular_oee]

    fieldsets = (
        (
            "Informações Básicas",
            {"fields": ("machine", "data", "calculado_em", "calculado_por")},
        ),
        (
            "Indicadores Calculados (%)",
            {
                "fields": (
                    "oee",
                    "disponibilidade",
                    "performance",
                    "qualidade",
                ),
            },
        ),
        (
            "Dados Brutos - Tempos",
            {
                "fields": (
                    "tempo_total_disponivel_minutos",
                    "tempo_parado_minutos",
                    "tempo_producao_minutos",
                ),
                "classes": ("collapse",),
            },
        ),
        (
            "Dados Brutos - Quantidades",
            {
                "fields": (
                    "qtde_programada",
                    "qtde_produzida",
                    "qtde_refugo",
                    "qtde_retrabalho",
                ),
                "classes": ("collapse",),
            },
        ),
    )

    def oee_colored(self, obj):
        """Exibe OEE com cor baseada no valor"""
        if obj.oee >= 85:
            color = "green"
            status = "✓ Excelente"
        elif obj.oee >= 70:
            color = "orange"
            status = "⚠ Bom"
        else:
            color = "red"
            status = "✗ Ruim"

        return format_html(
            '<span style="color: {}; font-weight: bold;">{:.1f}% - {}</span>',
            color,
            obj.oee,
            status,
        )

    oee_colored.short_description = "OEE"

    def has_add_permission(self, request):
        # Os indicadores são calculados automaticamente, não devem ser criados manualmente
        return False


@admin.register(ResumoDesempenhoSetor)
class ResumoDesempenhoSetorAdmin(admin.ModelAdmin):
    list_display = (
        "setor",
        "data",
        "oee_colored",
        "disponibilidade_media",
        "performance_media",
        "qualidade_media",
        "qtde_maquinas",
    )
    list_filter = ("data", "setor")
    search_fields = ("setor__name",)
    readonly_fields = (
        "disponibilidade_media",
        "performance_media",
        "qualidade_media",
        "oee_media",
        "calculado_em",
    )
    date_hierarchy = "data"
    ordering = ("-data", "setor")

    fieldsets = (
        (
            "Informações Básicas",
            {"fields": ("setor", "data", "qtde_maquinas", "calculado_em")},
        ),
        (
            "Indicadores Médios (%)",
            {
                "fields": (
                    "oee_media",
                    "disponibilidade_media",
                    "performance_media",
                    "qualidade_media",
                ),
            },
        ),
        (
            "Dados de Produção",
            {
                "fields": (
                    "qtde_programada_total",
                    "qtde_produzida_total",
                ),
                "classes": ("collapse",),
            },
        ),
    )

    def oee_colored(self, obj):
        """Exibe OEE com cor baseada no valor"""
        if obj.oee_media >= 85:
            color = "green"
            status = "✓ Excelente"
        elif obj.oee_media >= 70:
            color = "orange"
            status = "⚠ Bom"
        else:
            color = "red"
            status = "✗ Ruim"

        return format_html(
            '<span style="color: {}; font-weight: bold;">{:.1f}% - {}</span>',
            color,
            obj.oee_media,
            status,
        )

    oee_colored.short_description = "OEE Médio"

    def has_add_permission(self, request):
        return False


@admin.register(ResumoDesempenhoGrupo)
class ResumoDesempenhoGrupoAdmin(admin.ModelAdmin):
    list_display = (
        "grupo",
        "data",
        "oee_colored",
        "disponibilidade_media",
        "performance_media",
        "qualidade_media",
        "qtde_maquinas",
    )
    list_filter = ("data", "grupo")
    search_fields = ("grupo__name",)
    readonly_fields = (
        "disponibilidade_media",
        "performance_media",
        "qualidade_media",
        "oee_media",
        "calculado_em",
    )
    date_hierarchy = "data"
    ordering = ("-data", "grupo")

    fieldsets = (
        (
            "Informações Básicas",
            {"fields": ("grupo", "data", "qtde_maquinas", "qtde_setores", "calculado_em")},
        ),
        (
            "Indicadores Médios (%)",
            {
                "fields": (
                    "oee_media",
                    "disponibilidade_media",
                    "performance_media",
                    "qualidade_media",
                ),
            },
        ),
        (
            "Dados de Produção",
            {
                "fields": ("qtde_produzida_total",),
                "classes": ("collapse",),
            },
        ),
    )

    def oee_colored(self, obj):
        """Exibe OEE com cor baseada no valor"""
        if obj.oee_media >= 85:
            color = "green"
            status = "✓ Excelente"
        elif obj.oee_media >= 70:
            color = "orange"
            status = "⚠ Bom"
        else:
            color = "red"
            status = "✗ Ruim"

        return format_html(
            '<span style="color: {}; font-weight: bold;">{:.1f}% - {}</span>',
            color,
            obj.oee_media,
            status,
        )

    oee_colored.short_description = "OEE Médio"

    def has_add_permission(self, request):
        return False

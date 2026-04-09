from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from _itens import models


class FamilyResource(resources.ModelResource):
    class Meta:
        model = models.FamilyProd


@admin.register(models.FamilyProd)
class FamilyProdAdmin(ImportExportModelAdmin):
    resources_classes = [FamilyResource]
    list_display = (
        "refer",
        "description",
    )
    search_fields = (
        "refer",
        "name",
    )
    ordering = ("refer",)


class ItemResource(resources.ModelResource):
    class Meta:
        model = models.ItemAcabado


class EstruturainLine(admin.TabularInline):
    model = models.Estrutura
    extra = 1


@admin.register(models.ItemAcabado)
class ItemAcabadoAdmin(ImportExportModelAdmin):
    resource_classes = [ItemResource]
    list_display = (
        "item_cod",
        "item_name",
        "qtd_per_day",
        "is_active",
    )
    search_fields = (
        "item_cod",
        "item_name",
    )
    ordering = ("item_cod",)
    list_editable = (
        "qtd_per_day",
        "is_active",
    )
    inlines = [EstruturainLine]

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.select_related("family", "created_by", "updated_by")
        queryset = queryset.prefetch_related("subitens")
        return queryset


@admin.register(models.ComponentesGroup)
class ComponentesGroupAdmin(admin.ModelAdmin):
    list_display = ("group", "name")


class ComponentesResource(resources.ModelResource):
    class Meta:
        model = models.Componentes


@admin.register(models.Componentes)
class ComponentesAdmin(ImportExportModelAdmin):
    resource_classes = [ComponentesResource]
    list_display = (
        "codigo",
        "name",
        "grupo",
        "tipo_compra",
        "unidade_medida",
    )
    list_filter = ("tipo_compra", "grupo")
    search_fields = ("codigo", "name")
    ordering = ("codigo",)
    fieldsets = (
        (
            "Informações Básicas",
            {"fields": ("codigo", "name", "grupo", "unidade_medida")},
        ),
        (
            "Controle de Compra",
            {
                "fields": ("tipo_compra", "qtde_minima", "prazo_entrega_dias"),
                "classes": ("collapse",),
            },
        ),
    )


class ComposicaoInsumoInline(admin.TabularInline):
    model = models.ComposicaoInsumo
    extra = 1


class ItemBaseResource(resources.ModelResource):
    class Meta:
        model = models.ItemBase


@admin.register(models.ItemBase)
class ItemBaseAdmin(ImportExportModelAdmin):
    list_display = (
        "itembase_cod",
        "itembase_name",
        "ficha_tecnica",
        "variation",
        "componente",
        "comprimento",
        "largura",
        "espessura",
    )
    resource_classes = [ItemBaseResource]
    search_fields = (
        "itembase_cod",
        "itembase_name",
    )
    ordering = ("-itembase_cod",)
    inlines = [ComposicaoInsumoInline]


class InsumoGroupResource(resources.ModelResource):
    class Meta:
        model = models.InsumoGroup


@admin.register(models.InsumoGroup)
class InsumoGroupAdmin(ImportExportModelAdmin):
    list_display = ("codigo", "nome")
    resource_classes = [InsumoGroupResource]
    search_fields = ("codigo", "nome")
    ordering = ("codigo",)


class InsumoResource(resources.ModelResource):
    class Meta:
        model = models.Insumo


@admin.register(models.Insumo)
class InsumoAdmin(ImportExportModelAdmin):
    resource_classes = [InsumoResource]
    list_display = (
        "codigo",
        "nome",
        "tipo",
        "grupo",
        "especificacao",
        "estoque_minimo",
        "is_active",
    )
    list_filter = ("tipo", "grupo", "is_active")
    search_fields = ("codigo", "nome", "especificacao")
    ordering = ("codigo",)
    list_editable = ("is_active",)
    fieldsets = (
        (
            "Informações Básicas",
            {"fields": ("codigo", "nome", "tipo", "grupo", "unidade_medida")},
        ),
        (
            "Especificações",
            {
                "fields": ("especificacao", "estoque_minimo"),
            },
        ),
        (
            "Outros",
            {
                "fields": ("observacoes", "is_active"),
            },
        ),
    )


class ComponenteProgramacaoResource(resources.ModelResource):
    class Meta:
        model = models.ComponenteProgramacao


@admin.register(models.ComponenteProgramacao)
class ComponenteProgramacaoAdmin(ImportExportModelAdmin):
    resource_classes = [ComponenteProgramacaoResource]
    list_display = (
        "item_acabado",
        "componente",
        "quantidade",
    )
    search_fields = ("item_acabado__item_cod", "componente__codigo")
    ordering = ("item_acabado__item_cod",)

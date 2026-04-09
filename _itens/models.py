from django import forms
from django.conf import settings
from django.db import models

from _resources.models import Unidade_Medida


class FamilyProd(models.Model):
    class Meta:
        verbose_name = "Família Produto"
        verbose_name_plural = "Familia Produto"

    refer = models.CharField(
        max_length=20, unique=True, verbose_name="Código Família Comercial"
    )
    description = models.CharField(max_length=100, verbose_name="Nome Família")

    def save(self, *args, **kwargs):
        self.description = self.description.upper()
        super(FamilyProd, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return self.description


class ItemAcabado(models.Model):
    class Meta:
        verbose_name = "Item"
        verbose_name_plural = "Itens"

    item_cod = models.CharField(
        max_length=20,
        unique=True,
    )
    item_desc = models.CharField(max_length=100, verbose_name="Nome Produto")
    item_name = models.CharField(max_length=50, verbose_name="Nome Resumido")
    semi_code = models.CharField(
        max_length=50,
        verbose_name="Referência Semiacabado",
        help_text='Digitar código sem ponto "."',
        blank=True,
        null=True,
    )

    qtd_per_day = models.IntegerField(verbose_name="Peças ao dia")
    is_active = models.BooleanField(default=True, verbose_name="Ativo")
    family = models.ForeignKey(
        FamilyProd,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Família Produto",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="itemacab_created_by",
    )
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="itemacab_updated_by",
    )
    qtde_volume = models.FloatField(
        blank=True,
        null=True,
        help_text="""
            Quantidade de volumes por item:
            - 1 item = 1 volume: digite 1
            - 1 item = 2 volumes: digite 2
            - 2 itens = 1 volume: digite 0,5
        """,
    )
    subitens = models.ManyToManyField(
        "ItemBase", through="Estrutura", related_name="subprodutos"
    )

    def save(self, *args, **kwargs):
        self.item_desc = self.item_desc.upper()
        self.item_name = self.item_name.upper()
        super(ItemAcabado, self).save(*args, **kwargs)

    def clean(self):
        # Validation logic from clean_item_cod
        if len(str(self.item_cod)) < 14:
            raise forms.ValidationError("Formato código invalido", code="invalid")
        return super().clean()

    def obter_subprodutos_e_quantidades(self):
        subprodutos = Estrutura.objects.filter(item=self).select_related("subitem")
        subprodutos_quantidade = []
        if subprodutos:
            for estrutura in subprodutos:
                subprodutos_quantidade.append(
                    {
                        "subproduto": estrutura.subitem,
                        "quantidade": estrutura.qntde_pre,
                    }
                )
        return subprodutos_quantidade

    def __str__(self) -> str:
        item = f"{self.item_cod} - {self.item_desc}"
        return item


class InsumoGroup(models.Model):
    """Categorias de insumos: Madeiras, Tecidos, Espumas, Hardware, etc"""

    class Meta:
        verbose_name = "Grupo Insumo"
        verbose_name_plural = "Grupos Insumos"

    codigo = models.CharField(max_length=20, unique=True)
    nome = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.codigo} - {self.nome}"


class Insumo(models.Model):
    """
    Matérias-primas e insumos básicos usados para fabricar ItemBase:
    - Madeiras: pinus, tauari, mdf 15mm
    - Tecidos brutos
    - Espumas
    - Hardware padrão
    """

    class Meta:
        verbose_name = "Insumo - MP"
        verbose_name_plural = "Insumos - MP"

    TIPO_CHOICES = [
        ("madeira", "Madeira"),
        ("tecido", "Tecido"),
        ("espuma", "Espuma"),
        ("hardware", "Hardware"),
        ("pintura", "Pintura/Acabamento"),
        ("outro", "Outro"),
    ]

    codigo = models.CharField(max_length=30, unique=True, verbose_name="Código Insumo")
    nome = models.CharField(max_length=150, verbose_name="Nome/Descrição")
    tipo = models.CharField(
        max_length=20, choices=TIPO_CHOICES, verbose_name="Tipo de Insumo"
    )
    grupo = models.ForeignKey(
        InsumoGroup,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Grupo",
    )
    unidade_medida = models.ForeignKey(
        Unidade_Medida,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Unidade de Medida",
    )
    especificacao = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name="Especificação (ex: 15mm, 1,5m, etc)",
    )
    estoque_minimo = models.FloatField(
        null=True,
        blank=True,
        verbose_name="Estoque Mínimo",
        help_text="Quantidade mínima para disparar reposição",
    )
    observacoes = models.TextField(null=True, blank=True, verbose_name="Observações")
    is_active = models.BooleanField(default=True, verbose_name="Ativo")

    def save(self, *args, **kwargs):
        self.nome = self.nome.upper()
        super(Insumo, self).save(*args, **kwargs)

    def __str__(self):
        especif = f" ({self.especificacao})" if self.especificacao else ""
        return f"{self.codigo} - {self.nome}{especif}"


class ComponentesGroup(models.Model):
    class Meta:
        verbose_name = "Grupo Componentes"
        verbose_name_plural = "Grupos Componentes"

    group = models.CharField(max_length=15, unique=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name}"


class Componentes(models.Model):
    class Meta:
        verbose_name = "Componente"
        verbose_name_plural = "Componentes"

    TIPO_COMPRA_CHOICES = [
        ("estoque", "Mantém em Estoque"),
        ("demanda", "Compra sob Demanda"),
    ]

    codigo = models.CharField(max_length=15, unique=True)
    name = models.CharField(max_length=100)
    grupo = models.ForeignKey(ComponentesGroup, on_delete=models.CASCADE)
    unidade_medida = models.ForeignKey(
        Unidade_Medida, on_delete=models.CASCADE, null=True, blank=True
    )

    # Controle de estoque
    tipo_compra = models.CharField(
        max_length=10,
        choices=TIPO_COMPRA_CHOICES,
        default="demanda",
        verbose_name="Tipo de Compra",
    )
    qtde_minima = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name="Quantidade Mínima em Estoque",
        help_text="Deixar em branco para compra sob demanda",
    )
    prazo_entrega_dias = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name="Prazo de Entrega (dias)",
        help_text="Dias necessários para recebimento do fornecedor",
    )

    def __str__(self):
        return f"{self.codigo} - {self.name}"


class ItemBase(models.Model):
    class Meta:
        verbose_name = "Item Base - KIT"
        verbose_name_plural = "Itens Base - KIT"

    itembase_cod = models.CharField(max_length=20, unique=True, verbose_name="Código")
    itembase_name = models.CharField(max_length=100, verbose_name="Nome Sub-Item")
    ficha_tecnica = models.ImageField(
        upload_to="assets/ficha_tecnica/%Y%m/", default="", blank=True
    )
    variation = models.CharField(
        max_length=50, null=True, blank=True, verbose_name="Variação"
    )
    componente = models.ForeignKey(
        Componentes,
        verbose_name=("Componente"),
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    comprimento = models.FloatField(
        verbose_name="Comprimento (mm)", null=True, blank=True
    )
    largura = models.FloatField(
        null=True,
        blank=True,
        verbose_name="Largura (mm)",
    )
    espessura = models.FloatField(
        null=True,
        blank=True,
        verbose_name="Espessura (mm)",
    )
    observation = models.TextField(verbose_name="Observações   ", null=True, blank=True)

    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        self.itembase_name = self.itembase_name.upper()
        super(ItemBase, self).save(*args, **kwargs)

    insumos = models.ManyToManyField(
        Insumo, through="ComposicaoInsumo", related_name="itemsbases"
    )

    def __str__(self) -> str:
        item = f"{self.itembase_cod} - {self.itembase_name}"
        return item


class ComposicaoInsumo(models.Model):
    """
    Define quais insumos são necessários para fabricar um ItemBase
    e em que quantidade
    """

    class Meta:
        verbose_name = "Composição de Insumo"
        verbose_name_plural = "Composições de Insumo"
        unique_together = ("itembase", "insumo")

    itembase = models.ForeignKey(
        ItemBase, on_delete=models.CASCADE, related_name="composicao_insumos"
    )
    insumo = models.ForeignKey(
        Insumo, on_delete=models.CASCADE, related_name="composicoes"
    )
    quantidade = models.FloatField(verbose_name="Quantidade Necessária")
    observacoes = models.CharField(
        max_length=100, null=True, blank=True, verbose_name="Observações"
    )

    def __str__(self):
        return (
            f"{self.itembase.itembase_cod} → {self.insumo.codigo} ({self.quantidade})"
        )


class Estrutura(models.Model):
    item = models.ForeignKey(
        ItemAcabado, on_delete=models.SET_NULL, null=True, blank=True
    )
    subitem = models.ForeignKey(
        ItemBase, on_delete=models.SET_NULL, null=True, blank=True
    )
    qntde_pre = models.PositiveIntegerField(null=True)
    qntde_usi = models.PositiveIntegerField(null=True)
    qntde_lix = models.PositiveIntegerField(null=True)

    class Meta:
        unique_together = ("item", "subitem")

    def __str__(self) -> str:
        item_cod = self.item.item_cod if self.item else "N/A"
        subitem_cod = self.subitem.itembase_cod if self.subitem else "N/A"
        string = f"{item_cod} - {subitem_cod}"
        return string


class ComponenteProgramacao(models.Model):
    """
    Links entre ItemAcabado e Componentes Comprados
    Similar a Estrutura, mas para items comprados (tecido, espuma, ferragem, etc)
    """

    class Meta:
        verbose_name = "Componente Programado"
        verbose_name_plural = "Componentes Programados"
        unique_together = ("item_acabado", "componente")

    item_acabado = models.ForeignKey(
        ItemAcabado, on_delete=models.CASCADE, related_name="componentes_comprados"
    )
    componente = models.ForeignKey(
        Componentes, on_delete=models.CASCADE, related_name="programacoes"
    )
    quantidade = models.PositiveIntegerField(verbose_name="Quantidade por Unidade")

    def __str__(self) -> str:
        return f"{self.item_acabado.item_cod} → {self.componente.codigo}"


class Finish(models.Model):
    class Meta:
        verbose_name = "Acabamento"
        verbose_name_plural = "Acabamentos"

    code_finish = models.CharField(verbose_name="Código", max_length=50)
    name_finish = models.CharField(verbose_name="Nome", max_length=50)

    def __str__(self) -> str:
        return self.name_finish

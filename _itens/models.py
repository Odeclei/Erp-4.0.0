from django.db import models
from django.conf import settings
from django import forms
from _resources.models import Unidade_Medida


class FamilyProd(models.Model):
    class Meta:
        verbose_name = "Família Produto"
        verbose_name_plural = "Familia Produto"

    refer = models.CharField(
        max_length=20, unique=True, verbose_name="Código Família Comercial"
    )
    name = models.CharField(max_length=100, verbose_name="Nome Família")

    def save(self, *args, **kwargs):
        self.name = self.name.upper()
        super(FamilyProd, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name


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
        subprodutos = Estrutura.objects.filter(produto=self).select_related("item_base")
        subprodutos_quantidade = []
        if subprodutos:
            for estrutura in subprodutos:
                subprodutos_quantidade.append(
                    {
                        "subproduto": estrutura.item_base,
                        "quantiade": estrutura.qntde_pre,
                    }
                )
        return subprodutos_quantidade

    def __str__(self) -> str:
        item = f"{self.item_cod} - {self.item_desc}"
        return item


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

    codigo = models.CharField(max_length=15, unique=True)
    name = models.CharField(max_length=100)
    grupo = models.ForeignKey(ComponentesGroup, on_delete=models.CASCADE)
    unidade_medida = models.ForeignKey(
        Unidade_Medida, on_delete=models.CASCADE, null=True, blank=True
    )

    def __str__(self):
        return f"{self.codigo} - {self.name}"


class ItemBase(models.Model):
    class Meta:
        verbose_name = "Item Base"
        verbose_name_plural = "Itens Base"

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

    def __str__(self) -> str:
        item = f"{self.itembase_cod} - {self.itembase_name}"
        return item


class Estrutura(models.Model):
    item_acab = models.ForeignKey(
        ItemAcabado, on_delete=models.SET_NULL, null=True, blank=True
    )
    item_base = models.ForeignKey(
        ItemBase, on_delete=models.SET_NULL, null=True, blank=True
    )
    qntde_pre = models.PositiveIntegerField(null=True)
    qntde_usi = models.PositiveIntegerField(null=True)
    qntde_lix = models.PositiveIntegerField(null=True)

    class Meta:
        unique_together = ("item_acab", "item_base")

    def __str__(self) -> str:
        item_acab_cod = self.item_acab.item_cod if self.item_acab else "N/A"
        item_base_cod = self.item_base.itembase_cod if self.item_base else "N/A"
        string = f"{item_acab_cod} - {item_base_cod}"
        return string


class Finish(models.Model):
    class Meta:
        verbose_name = "Acabamento"
        verbose_name_plural = "Acabamentos"

    code_finish = models.CharField(verbose_name="Código", max_length=50)
    name_finish = models.CharField(verbose_name="Nome", max_length=50)

    def __str__(self) -> str:
        return self.name_finish

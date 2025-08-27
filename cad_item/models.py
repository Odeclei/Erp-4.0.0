# flake8: noqa
from django import forms
from django.contrib.auth.models import User
from django.db import models


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


class Item(models.Model):
    class Meta:
        verbose_name = "Item"
        verbose_name_plural = "Itens"

    item_cod = models.CharField(
        max_length=20,
        unique=True,
    )
    name_prod = models.CharField(max_length=100, verbose_name="Nome Produto")
    name_abrev = models.CharField(max_length=50, verbose_name="Nome Resumido")
    semi_code = models.CharField(
        max_length=50,
        verbose_name="Referência Semiacabado",
        help_text='Digitar código sem ponto "."',
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
        User,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="created_by",
    )
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="updated_by",
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
        "SubItem", through="Estrutura", related_name="subprodutos"
    )

    def save(self, *args, **kwargs):
        self.name_prod = self.name_prod.upper()
        self.name_prod = self.name_prod.upper()
        self.name_abrev = self.name_abrev.upper()
        super(Item, self).save(*args, **kwargs)

    def clean(self):
        # Validation logic from clean_item_cod
        if len(str(self.item_cod)) < 14:
            raise forms.ValidationError("Formato código invalido", code="invalid")
        return super().clean()

    def obter_subprodutos_e_quantidades(self):
        subprodutos = Estrutura.objects.filter(produto=self)
        subprodutos_quantidade = [
            {
                "subproduto": estrutura.subprodutos,  # type: ignore
                "quantidade": estrutura.qntde_pre,
            }
            for estrutura in subprodutos
        ]
        return subprodutos_quantidade

    def __str__(self) -> str:
        item = f"{self.item_cod} - {self.name_prod}"
        return item


class Material(models.Model):
    MATERIAL_CHOICES = [("Madeiras", ("Madeira")), ("Chapas", ("Chapas"))]
    material_code = models.CharField(max_length=15, unique=True)
    material_description = models.CharField(max_length=100)
    material_group = models.CharField(
        max_length=50, choices=MATERIAL_CHOICES, default="Madeiras"
    )
    unidade_medida = models.CharField(
        max_length=50,
        default="cm",
        choices=[
            ("m³", "Metros Cúbicos"),
            ("m²", "Metros Quadrados"),
            ("ml", "Metro Linear"),
        ],
    )

    def __str__(self):
        return f"{self.material_code} - {self.material_description}"


class SubItem(models.Model):
    class Meta:
        verbose_name = "Sub-Item"
        verbose_name_plural = "Sub-Itens"

    subitem_cod = models.CharField(max_length=20, unique=True, verbose_name="Código")
    name_subitem = models.CharField(max_length=100, verbose_name="Nome Sub-Item")
    observation = models.TextField(verbose_name="Observações   ", null=True, blank=True)
    # code_father = models.ManyToManyField(
    #     Item, through='FichaTecnica', related_name='code_semi_item')
    ficha_tecnica = models.ImageField(
        upload_to="assets/ficha_tecnica/%Y%m/", default="", blank=True
    )
    variation = models.CharField(
        max_length=50, null=True, blank=True, verbose_name="Variação"
    )
    material = models.ForeignKey(
        Material,
        verbose_name=("Material"),
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    comprimento = models.DecimalField(
        max_digits=10,
        decimal_places=0,
        null=True,
        blank=True,
        verbose_name="Comprimento (mm)",
    )
    largura = models.DecimalField(
        max_digits=10,
        decimal_places=0,
        null=True,
        blank=True,
        verbose_name="Largura (mm)",
    )
    espessura = models.DecimalField(
        max_digits=10,
        decimal_places=0,
        null=True,
        blank=True,
        verbose_name="Espessura (mm)",
    )

    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        self.name_subitem = self.name_subitem.upper()
        super(SubItem, self).save(*args, **kwargs)

    def __str__(self) -> str:
        item = f"{self.subitem_cod} - {self.name_subitem}"
        return item


class Estrutura(models.Model):
    item = models.ForeignKey(Item, on_delete=models.SET_NULL, null=True, blank=True)
    subitem = models.ForeignKey(
        SubItem, on_delete=models.SET_NULL, null=True, blank=True
    )
    qntde_pre = models.PositiveIntegerField(null=True)
    qntde_usi = models.PositiveIntegerField(null=True)
    qntde_lix = models.PositiveIntegerField(null=True)

    class Meta:
        unique_together = ("item", "subitem")

    def __str__(self) -> str:
        return super().__str__()


class Finish(models.Model):
    class Meta:
        verbose_name = "Acabamento"
        verbose_name_plural = "Acabamentos"

    code_finish = models.CharField(verbose_name="Código", max_length=50)
    name_finish = models.CharField(verbose_name="Nome", max_length=50)

    def __str__(self) -> str:
        return self.name_finish

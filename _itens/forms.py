from django import forms

from _itens.models import (
    ItemAcabado,
    FamilyProd,
    Componentes,
    ItemBase,
    Estrutura,
    Finish,
)

COMMON_INPUT_ATTRS = {
    "class": "form-control form-control-lg border border-success pt-3"
}


class ItemAcabadoForm(forms.ModelForm):

    class Meta:
        model = ItemAcabado
        fields = [
            "item_cod",
            "item_desc",
            "item_name",
            "qtd_per_day",
            "qtde_volume",
            "family",
            "is_active",
        ]

        widgets = {
            "item_cod": forms.TextInput(attrs=COMMON_INPUT_ATTRS),
            "item_desc": forms.TextInput(attrs=COMMON_INPUT_ATTRS),
            "item_name": forms.TextInput(attrs=COMMON_INPUT_ATTRS),
            "qtd_per_day": forms.NumberInput(attrs=COMMON_INPUT_ATTRS),
            "family": forms.Select(attrs={"type": "hidden"}),
            "qtde_volume": forms.NumberInput(attrs=COMMON_INPUT_ATTRS),
        }
        help_texts = {
            "item_cod": "Formato: 000.0000.00.00",
        }


class FamilyForm(forms.ModelForm):
    class Meta:
        model = FamilyProd
        fields = (
            "refer",
            "name",
        )


class ComponentesForm(forms.ModelForm):
    class Meta:
        model = Componentes
        fields = "__all__"


class ItemBaseForm(forms.ModelForm):
    class Meta:
        model = ItemBase
        fields = "__all__"


class EstruturaForm(forms.ModelForm):
    class Meta:
        model = Estrutura
        fields = "__all__"


class FinishForm(forms.ModelForm):
    class Meta:
        model = Finish
        fields = "__all__"

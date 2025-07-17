# flake8: noqa
from django import forms

from cad_item.models import Estrutura, FamilyProd, Item, SubItem


class ItemForm(forms.ModelForm):
    # The item_cod field is defined in the model; customize its widget in Meta if needed.

    class Meta:
        model = Item
        fields = (
            "item_cod",
            "name_prod",
            "name_abrev",
            "semi_code",
            "qtd_per_day",
            "is_active",
            "family",
        )
        widgets = {
            "family": forms.Select(attrs={"type": "hidden"}),
            "item_cod": forms.TextInput(
                attrs={
                    "class": "col-7 form-control form-control-lg",
                }
            ),
            "name_prod": forms.TextInput(
                attrs={
                    "class": "col-18 form-control form-control-lg",
                }
            ),
            "name_abrev": forms.TextInput(
                attrs={
                    "class": "col-18 form-control form-control-lg",
                }
            ),
            "semi_code": forms.TextInput(
                attrs={
                    "class": "col-18 form-control form-control-lg",
                }
            ),
            "qtd_per_day": forms.NumberInput(
                attrs={
                    "class": "col-18 form-control form-control-lg",
                    "min": 0,
                    "step": 1,
                }
            ),
            "family": forms.Select(
                attrs={
                    "class": "col-18 form-control form-control-lg",
                }
            ),
        }
        labels = {
            "item_cod": "Código do Item",
            "name_prod": "Nome do Item",
            "name_abrev": "Nome Abreviado",
            "semi_code": "Código Semi Acabado",
            "qtd_per_day": "Quantidade por Dia",
            "is_active": "Ativo",
            "family": "Família do Produto",
        }
        help_texts = {"item_cod": 'Formato código = "000.0000.00.00"'}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["family"].queryset = FamilyProd.objects.all()  # type: ignore


class FamiliForm(forms.ModelForm):
    class Meta:
        model = FamilyProd
        fields = (
            "refer",
            "description",
        )


class SubItemForm(forms.ModelForm):
    class Meta:
        model = SubItem
        fields = (
            "subitem_cod",
            "name_subitem",
            "observation",
            "ficha_tecnica",
            "variation",
            "is_active",
            "material",
            "comprimento",
            "largura",
            "espessura",
        )
        widgets = {}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Opcional: Adicionar classes CSS para estilização
        self.fields["material"].widget.attrs.update(
            {"class": "col-18 col-md-18 grid-item"}
        )
        self.fields["ficha_tecnica"].widget.attrs.update(
            {"class": "col-18 col-md-18 grid-item"}
        )
        self.fields["name_subitem"].widget.attrs.update({"class": "form-control"})
        self.fields["largura"].widget.attrs.update({"class": "form-control"})
        self.fields["comprimento"].widget.attrs.update({"class": "form-control"})
        self.fields["espessura"].widget.attrs.update({"class": "form-control"})


class EstruturaForm(forms.ModelForm):
    class Meta:
        model = Estrutura
        fields = "item", "subitem", "qntde_pre", "qntde_usi", "qntde_lix"

        widgets = {
            "item": forms.HiddenInput(),  # campo oculto
            "subitem": forms.Select(
                attrs={"class": "form-control form-control-lg select2"}
            ),
            "qntde_pre": forms.NumberInput(
                attrs={"class": "form-control form-control-lg"}
            ),
            "qntde_usi": forms.NumberInput(
                attrs={"class": "form-control form-control-lg"}
            ),
            "qntde_lix": forms.NumberInput(
                attrs={"class": "form-control form-control-lg"}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if "subitem" in self.data:
            self.fields["subitem"].queryset = SubItem.objects.all()  # type: ignore

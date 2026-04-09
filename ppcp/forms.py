from django import forms

from ppcp.models import ItemProgramacao, ManufacturingOrder, SubItemProgramacao


class ManufacturingOrderForm(forms.ModelForm):
    class Meta:
        model = ManufacturingOrder
        fields = (
            "order_number",
            "prog_year",
            "description",
            "status",
        )


class ItemProgramacaoForm(forms.ModelForm):
    class Meta:
        model = ItemProgramacao
        fields = ["item", "quantidade"]
        widgets = {
            "item": forms.HiddenInput(),
            "quantidade": forms.NumberInput(
                attrs={
                    "class": "form-control form-control-lg",
                    "min": "1",
                }
            ),
        }

    def clean_item(self):
        item = self.cleaned_data.get("item")
        print("\n[FORM.CLEAN_ITEM]")
        print(f"  item value: {item}")
        print(f"  item type: {type(item).__name__}")
        print(f"  item is None: {item is None}")
        if item is None:
            print("  ✗ Item é None!")
        else:
            print(f"  ✓ Item tem valor: {item}")
        return item

    def clean(self):
        print("\n[FORM.CLEAN]")
        print(f"  cleaned_data keys: {list(self.cleaned_data.keys())}")
        print(f"  cleaned_data: {self.cleaned_data}")
        cleaned_data = super().clean()

        item = cleaned_data.get("item")
        quantidade = cleaned_data.get("quantidade")

        print(f"  item: {item}")
        print(f"  quantidade: {quantidade}")

        return cleaned_data


class SubItemProgramacaoForm(forms.ModelForm):
    class Meta:
        model = SubItemProgramacao
        fields = (
            "produto_programado",
            "subproduto",
            "programacao",
            "qtde_pre",
            "qtde_usi",
            "qtde_lix",
        )

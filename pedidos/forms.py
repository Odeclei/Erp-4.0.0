from calendar import c
import code
from django import forms
from pedidos.models import Pedidos, ItemPedido, Finish
from cad_item.models import Finish as CadItemFinish


class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedidos
        fields = (
            "pedido_number",
            "pedido_cliente",
            "cliente",
            "cargo_number",
            "lacre_number",
            "status",
            "ucc_label",
        )

        widgets = {
            "pedido_number": forms.TextInput(
                attrs={
                    "class": "form-control form-control-lg border border-success pt-3",
                }
            ),
            "pedido_cliente": forms.TextInput(
                attrs={
                    "class": "form-control form-control-lg border border-success pt-3",
                }
            ),
            "cliente": forms.Select(
                attrs={
                    "class": "form-control form-control-lg border border-success pt-3",
                }
            ),
            "cargo_number": forms.TextInput(
                attrs={
                    "class": "form-control form-control-lg border border-success pt-3",
                }
            ),
            "lacre_number": forms.TextInput(
                attrs={
                    "class": "form-control form-control-lg border border-success pt-3",
                }
            ),
            "status": forms.Select(
                attrs={
                    "class": "form-control form-control-lg border border-success pt-3",
                }
            ),
            "ucc_label": forms.CheckboxInput(
                attrs={
                    "class": "mx-2 form-check-input form-control-lg border border-success",
                    "style": "height: 2rem;width: 5rem;",
                    "role": "switch",
                }
            ),
        }
        labels = {
            "pedido_number": "Número do Pedido",
            "pedido_cliente": "Pedido Cliente",
            "cliente": "Cliente",
            "cargo_number": "Número do Cargamento",
            "lacre_number": "Número do Lacre",
            "status": "Status",
            "ucc_label": "Etiqueta UCC",
        }


class ItemPedidoForm(forms.ModelForm):
    finish_custom = forms.CharField(max_length=255, required=False)

    class Meta:
        model = ItemPedido
        fields = (
            "proforma",
            "item",
            "finish",
            "quantity",
            "observation",
        )

        def clean(self):
            cleaned_data = super().clean()
            proforma = cleaned_data.get("proforma")
            finish_custom_value = cleaned_data.get("finish_custom")

            if finish_custom_value:
                try:
                    finish_obj = CadItemFinish.objects.get(
                        name_finish=finish_custom_value
                    )
                except CadItemFinish.DoesNotExist:
                    finish_obj = CadItemFinish.objects.create(
                        code_finish=proforma, name_finish=finish_custom_value.upper()
                    )

                cleaned_data["finish"] = finish_obj
            return cleaned_data

        widgets = {
            "proforma": forms.TextInput(
                attrs={
                    "class": "form-control form-control-lg border border-succes  pt-3",
                    "readonly": True,
                }
            ),
            "item": forms.Select(
                attrs={
                    "class": "form-control form-control-lg border border-success bg-primary-subtle pt-3"
                }
            ),
            "finish": forms.Select(
                attrs={
                    "class": "form-control form-control-lg border border-success bg-primary-subtle pt-3"
                }
            ),
            "quantity": forms.NumberInput(
                attrs={
                    "class": "form-control form-control-lg border border-success bg-primary-subtle pt-3"
                }
            ),
            "observation": forms.Textarea(
                attrs={
                    "class": "form-control form-control-lg border border-success bg-primary-subtle pt-3"
                }
            ),
        }

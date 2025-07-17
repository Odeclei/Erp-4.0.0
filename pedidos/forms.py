from django import forms
from pedidos.models import Pedidos, ItemPedido


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
        }
        labels = {
            "pedido_number": "Número do Pedido",
            "pedido_cliente": "Pedido Cliente",
            "cliente": "Cliente",
            "cargo_number": "Número do Cargamento",
            "lacre_number": "Número do Lacre",
            "status": "Status",
        }


class ItemPedidoForm(forms.ModelForm):
    class Meta:
        model = ItemPedido
        fields = ("proforma", "item", "finish", "quantity")

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
        }

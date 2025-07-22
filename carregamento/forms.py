from cProfile import label
from django import forms

from carregamento.models import Carregamento


class CarregamentoForm(forms.ModelForm):
    class Meta:
        model = Carregamento
        fields = (
            "pedido_data",
            "item",
            "qtde_carregada",
            "operador",
        )

        widgets = {
            "pedido_data": forms.Select(
                attrs={
                    "class": "form-control form-control-lg border border-success bg-primary-subtle pt-3"
                }
            ),
            "item": forms.Select(
                attrs={
                    "class": "form-control form-control-lg border border-success bg-primary-subtle pt-3"
                }
            ),
            "qtde_carregada": forms.NumberInput(
                attrs={
                    "class": "form-control form-control-lg border border-success bg-primary-subtle pt-3"
                }
            ),
            "operador": forms.TextInput(
                attrs={
                    "class": "form-control form-control-lg border border-success bg-primary-subtle pt-3",
                    "hidden": True,
                }
            ),
        }
        labels = {
            "pedido_data": "Pedido",
            "item": "Item",
            "qtde_carregada": "Qtde Carregada",
            "operador": "Operador",
        }

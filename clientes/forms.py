from django import forms
from clientes.models import Clientes


class ClienteForm(forms.ModelForm):

    class Meta:
        model = Clientes
        fields = (
            "cnpj",
            "razao_social",
            "nome_fantasia",
            "address",
            "bairro",
            "city",
            "state",
            "country",
            "e_mail",
            "market",
        )
        widgets = {
            "cnpj": forms.TextInput(
                attrs={
                    "class": "form-control form-control-lg border border-success pt-3",
                }
            ),
            "razao_social": forms.TextInput(
                attrs={
                    "class": "form-control form-control-lg border border-success pt-3",
                }
            ),
            "nome_fantasia": forms.TextInput(
                attrs={
                    "class": "form-control form-control-lg border border-success pt-3",
                }
            ),
            "address": forms.TextInput(
                attrs={
                    "class": "form-control form-control-lg border border-success pt-3",
                }
            ),
            "bairro": forms.TextInput(
                attrs={
                    "class": "form-control form-control-lg border border-success pt-3",
                }
            ),
            "city": forms.TextInput(
                attrs={
                    "class": "form-control form-control-lg border border-success pt-3",
                }
            ),
            "state": forms.TextInput(
                attrs={
                    "class": "form-control form-control-lg border border-success pt-3",
                }
            ),
            "country": forms.TextInput(
                attrs={
                    "class": "form-control form-control-lg border border-success pt-3",
                }
            ),
            "e_mail": forms.TextInput(
                attrs={
                    "class": "form-control form-control-lg border border-success pt-3",
                }
            ),
            "market": forms.Select(
                attrs={
                    "class": "form-control form-control-lg border border-success pt-3",
                }
            ),
        }
        labels = {
            "cnpj": "CNPJ",
            "razao_social": "Razão Social",
            "nome_fantasia": "Nome Fantasia",
            "address": "Endereço",
            "bairro": "Bairro",
            "city": "Cidade",
            "state": "Estado",
            "country": "País",
            "e_mail": "E-mail",
            "market": "Mercado",
        }

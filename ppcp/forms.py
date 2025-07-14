from django import forms

from cad_item.models import Item
from ppcp.models import ItemProgramacao, ManufacturingOrder, SubItemProgramacao


class ManufacturingOrderForm(forms.ModelForm):
    class Meta:
        model = ManufacturingOrder
        fields = ("order_number", "prog_year", "description", "status",)


class ItemProgramacaoForm(forms.ModelForm):
    class Meta:
        model = ItemProgramacao
        fields = ("item", "programacao", 'quantidade', 'start_at', 'ends_at',)

        widgets = {

            'item': forms.Select(
                attrs={
                    'class': 'form-select form-select-lg',
                }
            ),
            'programacao': forms.Select(
                attrs={'readonly': True}
            ),
            'quantidade': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'onchange': 'altera_quantidade()',
                }
            ),
            'start_at': forms.DateInput(
                format=('%Y-%m-%d'),
                attrs={
                    'class': 'form-group form-control',
                    'placeholder': 'Selecionar Data Inicio',
                    'type': 'date',
                }
            ),

            'ends_at': forms.DateInput(
                format=('%Y-%m-%d'),
                attrs={
                    'class': 'form-group form-control',
                    'placeholder': 'Selecionar Data Entrega',
                    'type': 'date',
                }
            ),
        }


class SubItemProgramacaoForm(forms.ModelForm):
    class Meta:
        model = SubItemProgramacao
        fields = ('produto_programado', 'subproduto',
                  'programacao', 'qtde_pre', 'qtde_usi', 'qtde_lix',
                  )

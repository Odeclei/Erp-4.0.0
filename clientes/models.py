# flake8: noqa
from django.db import models
from django.forms import ChoiceField

# Create your models here.




class Clientes(models.Model):
    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'

    MARKET_CHOICES = [
        ('M.I.', 'Mercado Interno'),
        ('M.E.', 'Mercado Externo'),
    ]

    cnpj = models.CharField(max_length=20, unique= True)
    razao_social = models.CharField(
        max_length=100, default="", blank=True, null=True
    )
    nome_fantasia =models.CharField(max_length=50)
    address = models.CharField(max_length=100)
    bairro = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    e_mail = models.EmailField(max_length=254)
    market = models.CharField(
        choices=MARKET_CHOICES,
        default='M.I.',
        max_length=50,
    )



    def __str__(self) -> str:
        return self.nome_fantasia

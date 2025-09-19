# flake8: noqa
from django.conf import settings
from django.db import models

from cad_item.models import Item
from ppcp.models import ItemProgramacao, SubItemProgramacao
from rule.models import Machines


class Apont_Type(models.Model):  # tipo Apontamento Produção
    class Meta:
        verbose_name = "Tipo Apontamento"
        verbose_name_plural = "Tipo Apontamentos"

    apont_type = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.apont_type}"


class Motive(models.Model):  # Motivo de retrabalho
    class Meta:
        verbose_name = "Motivo Retrabalho"
        verbose_name_plural = "Motivo Retrabalhos"

    motive = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.motive}"


class StopsCategory(models.Model):  # Grupo de Parada
    class Meta:
        verbose_name = "Categoria Parada"
        verbose_name_plural = "Categorias Paradas"

    category = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.category}"


class StopsMotive(models.Model):  # Subgrupo de Parada
    class Meta:
        verbose_name = "Subcategoria Parada"
        verbose_name_plural = "Subcategorias Paradas"

    name = models.CharField(max_length=50)
    category = models.ForeignKey(StopsCategory, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name}"


class Stops(models.Model):  # Apontamento de Paradas
    machine = models.ForeignKey(Machines, on_delete=models.CASCADE)
    date = models.DateTimeField()
    motive = models.ForeignKey(StopsMotive, on_delete=models.SET_NULL, null=True)
    duration = models.PositiveIntegerField()  # valor em segundos
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )


# class MaquinaBase(models.Model):
#     data = models.DateField()
#     ano = models.CharField(max_length=2, blank=True)
#     programacao = models.CharField(max_length=100)
#     produto_pai = models.ForeignKey(ItemProgramacao, on_delete=models.RESTRICT)
#     produto_apontado = models.ForeignKey(SubItemProgramacao, on_delete=models.RESTRICT)
#     hora_inicio_setup = models.TimeField()
#     hora_inicio_producao = models.TimeField(null=True, blank=True)
#     hora_final_producao = models.TimeField(null=True, blank=True)
#     qtde_boa = models.IntegerField(null=True, blank=True)
#     refugo = models.IntegerField(null=True, blank=True)
#     tipo_apontamento = models.ForeignKey(
#         "Apont_Type", on_delete=models.SET_NULL, null=True, blank=True
#     )
#     motivo = models.ForeignKey(
#         "Motive", on_delete=models.SET_NULL, null=True, blank=True
#     )
#     user = models.ForeignKey(
#         settings.AUTH_USER_MODEL,
#         on_delete=models.SET_NULL,
#         blank=True,
#         null=True,
#     )
#     status = models.CharField(
#         max_length=20,
#         choices=[("aberto", "Aberto"), ("concluido", "Concluído")],
#         default="aberto",
#     )

#     class Meta:
#         abstract = True


# class Pre_f_015(MaquinaBase): ...


# class Pre_f_017(MaquinaBase): ...


# class Pre_f_016(MaquinaBase): ...


# class Usi_f_020(MaquinaBase): ...


# class Usi_f_021(MaquinaBase): ...


# class Usi_f_004(MaquinaBase): ...

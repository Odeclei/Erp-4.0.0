from django.db import models


class ApontType(models.Model):
    class Meta:
        verbose_name = "Tipo de Apontamento"
        verbose_name_plural = "Tipos de Apontamentos"

    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class MotivoRetrabalho(models.Model):
    class Meta:
        verbose_name = "Motivo de Retrabalho"
        verbose_name_plural = "Motivos de Retrabalho"

    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class StopsCategory(models.Model):
    class Meta:
        verbose_name = "Categoria de Parada"
        verbose_name_plural = "Categorias de Paradas"

    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class StopsMotive(models.Model):
    class Meta:
        verbose_name = "Motivo de Parada"
        verbose_name_plural = "Motivos de Paradas"

    name = models.CharField(max_length=100)
    category = models.ForeignKey(StopsCategory, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Unidade_Medida(models.Model):
    class Meta:
        verbose_name = "Unidade de Medida"
        verbose_name_plural = "Unidades de Medida"

    sigla = models.CharField(max_length=10, unique=True)
    descricao = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.sigla

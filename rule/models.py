from platform import machine
from tabnanny import verbose
from click import group
from django.db import models


# Create your models here.
class Company(models.Model):
    class Meta:
        verbose_name = "Empresa"
        verbose_name_plural = "Empresas"

    name = models.CharField(max_length=100)
    fantasy_name = models.CharField(max_length=100)
    cnpj = models.CharField(max_length=100)
    street = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    country = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.fantasy_name}"


class Group(models.Model):
    class Meta:
        verbose_name = "Grupo"
        verbose_name_plural = "Grupos"

    name = models.CharField(max_length=50)
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        null=True,
    )

    def __str__(self):
        return f"{self.name}"


class Sectors(models.Model):
    class Meta:
        verbose_name = "Setor"
        verbose_name_plural = "Setores"

    name = models.CharField(max_length=50)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.name}"


class WorkStation(models.Model):
    class Meta:
        verbose_name = "Posto de Trabalho"
        verbose_name_plural = "Postos de Trabalho"

    description = models.CharField(max_length=50)
    sector = models.ForeignKey(
        Sectors,
        on_delete=models.CASCADE,
        null=True,
    )
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.description}"


class Machines(models.Model):
    class Meta:
        verbose_name = "Máquina"
        verbose_name_plural = "Máquinas"

    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=50)
    workStation = models.ForeignKey(
        WorkStation,
        on_delete=models.CASCADE,
        null=True,
    )
    turnowork = models.ManyToManyField("Turno", blank=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.code}"


class MacId(models.Model):
    mac_id = models.CharField(max_length=50)
    ip_adress = models.GenericIPAddressField(unique=True, blank=True, null=True)
    name = models.CharField(max_length=50)
    machine = models.ForeignKey(
        Machines,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    workstation = models.ForeignKey(
        "WorkStation",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    active = models.BooleanField(default=True)

    class Meta:
        unique_together = ("mac_id", "machine")

    def __str__(self):
        return f"{self.mac_id}"


class Turno(models.Model):
    class Meta:
        verbose_name = "Turno"
        verbose_name_plural = "Turnos"

    name = models.CharField(max_length=50)
    hora_inicio = models.TimeField(blank=True, null=True)
    hora_fim = models.TimeField(blank=True, null=True)
    hora_inicio_almoco = models.TimeField(blank=True, null=True)
    hora_fim_almoco = models.TimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.name}"

from django.db import models


# Create your models here.
class Company(models.Model):
    class Meta:
        verbose_name = 'Company'
        verbose_name_plural = 'Companyes'

    name = models.CharField(max_length=100)
    fantasy_name = models.CharField(max_length=100)
    cnpj = models.CharField(max_length=100)
    street = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    country = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.fantasy_name}'


class Sectors(models.Model):
    class Meta:
        verbose_name = 'Sector'
        verbose_name_plural = 'Sectors'

    name = models.CharField(max_length=50)
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE,
        null=True,
    )

    def __str__(self):
        return f'{self.name}'


class Machines(models.Model):
    class Meta:
        verbose_name = 'Machine'
        verbose_name_plural = 'Machines'
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=50)
    sector = models.ForeignKey(
        Sectors, on_delete=models.CASCADE,
        null=True,
    )
    active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.code}'


class MacId(models.Model):
    mac_id = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    machine = models.ForeignKey(
        Machines, on_delete=models.CASCADE,
        null=True,
    )
    active = models.BooleanField(default=True)

    class Meta:
        unique_together = ('mac_id', 'machine')

    def __str__(self):
        return f'{self.mac_id}'


class Turno(models.Model):
    name = models.CharField(max_length=50)
    hora_inicio = models.TimeField()
    hora_inicio_almoco = models.TimeField()
    hora_fim_almoco = models.TimeField()

    def __str__(self):
        return f'{self.name}'

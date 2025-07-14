from django.db import models


# Create your models here.
class MaquinaBase(models.Model):
    data = models.DateField()
    oee_indice = models.FloatField()
    availability = models.FloatField()
    performance = models.FloatField()
    quality = models.FloatField()

    class Meta:
        abstract = True


class Pre_f_015(MaquinaBase):
    ...


class Pre_f_017(MaquinaBase):
    ...


class Pre_f_016(MaquinaBase):
    ...


class Usi_f_020(MaquinaBase):
    ...


class Usi_f_021(MaquinaBase):
    ...

from django.db import models
from django.contrib.auth.models import AbstractUser

from rule.models import Turno, WorkStation


class Operator(AbstractUser):
    class Meta:
        verbose_name = "Operador"
        verbose_name_plural = "Operadores"

    matricula = models.CharField(max_length=20, unique=True)
    workstation = models.ForeignKey(
        WorkStation, on_delete=models.CASCADE, null=True, blank=True
    )
    turno = models.ForeignKey(Turno, on_delete=models.CASCADE, null=True, blank=True)
    is_superviser = models.BooleanField(default=False)

    def __str__(self):
        return self.get_full_name or self.username

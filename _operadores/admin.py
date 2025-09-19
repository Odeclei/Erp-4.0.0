from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from _operadores.models import Operator


@admin.register(Operator)
class OperatorAdmin(UserAdmin):
    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "is_staff",
        "matricula",
        "workstation",
        "turno",
        "is_superviser",
    )

    fieldsets = UserAdmin.fieldsets + (
        (
            "Informações Adicionais",
            {"fields": ("matricula", "setor", "workstation", "is_superviser")},
        ),
    )

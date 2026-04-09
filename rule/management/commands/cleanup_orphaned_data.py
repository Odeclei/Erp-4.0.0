"""
Django management command para limpar dados órfãos na BOM.
Remove estruturas e componentes com referências nulas.

Uso: python manage.py cleanup_orphaned_data
"""

from django.core.management.base import BaseCommand
from django.db import transaction

from _itens.models import Estrutura, ComponenteProgramacao


class Command(BaseCommand):
    help = "Limpar estruturas e componentes órfãos (com valores nulos)"

    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("🧹 Limpando dados órfãos..."))
        self.stdout.write("")

        # 1. Encontrar estruturas órfãs
        estruturas_orfas = Estrutura.objects.filter(subitem__isnull=True)
        qtde_est = estruturas_orfas.count()

        if qtde_est > 0:
            self.stdout.write(
                self.style.WARNING(f"⚠️  Encontradas {qtde_est} estrutura(s) com subitem=None")
            )
            for est in estruturas_orfas:
                self.stdout.write(
                    f"   ${est.id}: Item {est.item.item_cod} → subitem (None)"
                )
            estruturas_orfas.delete()
            self.stdout.write(
                self.style.SUCCESS(f"   ✓ Deletadas {qtde_est} estrutura(s) órfã(s)")
            )
        else:
            self.stdout.write(
                self.style.SUCCESS("   ✓ Nenhuma estrutura órfã encontrada")
            )

        self.stdout.write("")

        # 2. Encontrar componentes órfãos
        componentes_orfos = ComponenteProgramacao.objects.filter(
            componente__isnull=True
        )
        qtde_comp = componentes_orfos.count()

        if qtde_comp > 0:
            self.stdout.write(
                self.style.WARNING(
                    f"⚠️  Encontrados {qtde_comp} componente(s) com componente=None"
                )
            )
            for comp in componentes_orfos:
                self.stdout.write(
                    f"   ${comp.id}: Item {comp.item_acabado.item_cod} → componente (None)"
                )
            componentes_orfos.delete()
            self.stdout.write(
                self.style.SUCCESS(f"   ✓ Deletados {qtde_comp} componente(s) órfão(s)")
            )
        else:
            self.stdout.write(
                self.style.SUCCESS("   ✓ Nenhum componente órfão encontrado")
            )

        self.stdout.write("")
        self.stdout.write(
            self.style.SUCCESS(
                f"✅ Limpeza concluída: {qtde_est + qtde_comp} registro(s) removido(s)"
            )
        )

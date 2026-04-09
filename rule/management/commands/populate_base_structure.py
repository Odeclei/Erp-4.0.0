"""
Django management command para popular estrutura base genérica no banco de dados.
Cria: Grupos, Setores, Postos, Máquinas, Turnos, Itens, Estruturas.

Uso: python manage.py populate_base_structure
"""

from django.core.management.base import BaseCommand
from django.db import transaction

from rule.models import Group, Sectors, WorkStation, Machines, Turno
from _itens.models import (
    ItemAcabado,
    ItemBase,
    Estrutura,
    FamilyProd,
    InsumoGroup,
    ComponentesGroup,
)
from datetime import time


class Command(BaseCommand):
    help = "Popular estrutura base genérica para produção"

    @staticmethod
    def _criar_turnos():
        """Cria os turnos padrão de trabalho"""
        Command.stdout = None
        
        turnos_dados = [
            {
                "name": "Turno Manhã",
                "hora_inicio": time(7, 0),
                "hora_fim": time(15, 0),
                "hora_inicio_almoco": time(11, 30),
                "hora_fim_almoco": time(12, 30),
            },
            {
                "name": "Turno Tarde",
                "hora_inicio": time(15, 0),
                "hora_fim": time(23, 0),
                "hora_inicio_almoco": time(19, 0),
                "hora_fim_almoco": time(19, 30),
            },
        ]
        
        turnos = []
        for turno_data in turnos_dados:
            turno, created = Turno.objects.get_or_create(
                name=turno_data["name"],
                defaults={
                    "hora_inicio": turno_data["hora_inicio"],
                    "hora_fim": turno_data["hora_fim"],
                    "hora_inicio_almoco": turno_data["hora_inicio_almoco"],
                    "hora_fim_almoco": turno_data["hora_fim_almoco"],
                },
            )
            turnos.append(turno)
            status = "✓ Criado" if created else "✓ Existente"
        
        return turnos

    @staticmethod
    def _criar_grupos():
        """Cria grupos de produção"""
        grupos_dados = [
            {"name": "Usinagem"},
            {"name": "Montagem"},
            {"name": "Acabamento"},
        ]
        
        grupos = []
        for grupo_data in grupos_dados:
            grupo, created = Group.objects.get_or_create(**grupo_data)
            grupos.append(grupo)
        
        return grupos

    @staticmethod
    def _criar_setores(grupos):
        """Cria setores dentro de grupos"""
        setores_dados = [
            {"name": "CNC", "group": grupos[0]},  # Usinagem
            {"name": "Torno", "group": grupos[0]},  # Usinagem
            {"name": "Montagem Manual", "group": grupos[1]},  # Montagem
            {"name": "Montagem Automatizada", "group": grupos[1]},  # Montagem
            {"name": "Pintura", "group": grupos[2]},  # Acabamento
            {"name": "Lixamento", "group": grupos[2]},  # Acabamento
        ]
        
        setores = []
        for setor_data in setores_dados:
            setor, created = Sectors.objects.get_or_create(**setor_data)
            setores.append(setor)
        
        return setores

    @staticmethod
    def _criar_postos(setores):
        """Cria postos de trabalho nos setores"""
        postos_dados = [
            {"description": "CNC 01", "sector": setores[0], "active": True},
            {"description": "CNC 02", "sector": setores[0], "active": True},
            {"description": "Torno 01", "sector": setores[1], "active": True},
            {"description": "Torno 02", "sector": setores[1], "active": True},
            {"description": "Mesa Montagem 01", "sector": setores[2], "active": True},
            {"description": "Mesa Montagem 02", "sector": setores[2], "active": True},
            {"description": "Linha Auto 01", "sector": setores[3], "active": True},
            {"description": "Cabine Pintura 01", "sector": setores[4], "active": True},
            {"description": "Cabine Pintura 02", "sector": setores[4], "active": True},
            {"description": "Lixadeira 01", "sector": setores[5], "active": True},
        ]
        
        postos = []
        for posto_data in postos_dados:
            posto, created = WorkStation.objects.get_or_create(**posto_data)
            postos.append(posto)
        
        return postos

    @staticmethod
    def _criar_maquinas(postos, turnos):
        """Cria máquinas nos postos"""
        maquinas_dados = [
            {"code": "CNC01", "name": "CNC 01", "workStation": postos[0]},
            {"code": "CNC02", "name": "CNC 02", "workStation": postos[1]},
            {"code": "TORN01", "name": "Torno 01", "workStation": postos[2]},
            {"code": "TORN02", "name": "Torno 02", "workStation": postos[3]},
            {"code": "MONT01", "name": "Mesa 01", "workStation": postos[4]},
            {"code": "MONT02", "name": "Mesa 02", "workStation": postos[5]},
            {"code": "AUTO01", "name": "Linha Auto", "workStation": postos[6]},
            {"code": "PINT01", "name": "Pintura 01", "workStation": postos[7]},
            {"code": "PINT02", "name": "Pintura 02", "workStation": postos[8]},
            {"code": "LIXA01", "name": "Lixadeira 01", "workStation": postos[9]},
        ]
        
        maquinas = []
        for maq_data in maquinas_dados:
            maquina, created = Machines.objects.get_or_create(
                code=maq_data["code"],
                defaults={
                    "name": maq_data["name"],
                    "workStation": maq_data["workStation"],
                    "active": True,
                },
            )
            # Adicionar turnos
            maquina.turnowork.set(turnos)
            maquinas.append(maquina)
        
        return maquinas

    @staticmethod
    def _criar_familias():
        """Cria famílias de produtos"""
        familias_dados = [
            {"refer": "FAM-001", "description": "Sapatos"},
            {"refer": "FAM-002", "description": "Bolsas"},
            {"refer": "FAM-003", "description": "Acessórios"},
        ]
        
        familias = []
        for familia_data in familias_dados:
            familia, created = FamilyProd.objects.get_or_create(
                refer=familia_data["refer"],
                defaults={"description": familia_data["description"]},
            )
            familias.append(familia)
        
        return familias

    @staticmethod
    def _criar_items_base():
        """Cria itens base (sub-peças genéricas)"""
        items_base_dados = [
            {"itembase_cod": "PB-001", "itembase_name": "Solado"},
            {"itembase_cod": "PB-002", "itembase_name": "Pé Traseiro"},
            {"itembase_cod": "PB-003", "itembase_name": "Pé Dianteiro"},
            {"itembase_cod": "PB-004", "itembase_name": "Língüeta"},
            {"itembase_cod": "PB-005", "itembase_name": "Ilhóses"},
            {"itembase_cod": "AC-001", "itembase_name": "Etiqueta"},
            {"itembase_cod": "AC-002", "itembase_name": "Caixa"},
        ]
        
        items = []
        for item_data in items_base_dados:
            item, created = ItemBase.objects.get_or_create(**item_data)
            items.append(item)
        
        return items

    @staticmethod
    def _criar_items_acabados(familia, items_base):
        """Cria itens acabados com base em items_base"""
        items_acabados_dados = [
            {
                "item_cod": "SA-001",
                "item_name": "Sapato A",
                "item_desc": "Sapato casual modelo A",
                "qtd_per_day": 100,
                "family": familia,
            },
            {
                "item_cod": "SA-002",
                "item_name": "Sapato B",
                "item_desc": "Sapato formal modelo B",
                "qtd_per_day": 80,
                "family": familia,
            },
            {
                "item_cod": "SA-003",
                "item_name": "Sapato C",
                "item_desc": "Sapato esporte modelo C",
                "qtd_per_day": 120,
                "family": familia,
            },
        ]
        
        items = []
        for item_data in items_acabados_dados:
            item, created = ItemAcabado.objects.get_or_create(
                item_cod=item_data["item_cod"],
                defaults={
                    "item_name": item_data["item_name"],
                    "item_desc": item_data["item_desc"],
                    "qtd_per_day": item_data["qtd_per_day"],
                    "family": item_data["family"],
                    "is_active": True,
                },
            )
            items.append(item)
        
        return items

    @staticmethod
    def _criar_estruturas(items_acabados, items_base):
        """Cria estruturas (BOM - Bill of Materials)"""
        estruturas_dados = [
            # Sapato A: 1 solado, 2 pés, 1 língüeta, 1 ilhóses, 1 etiqueta, 1 caixa
            {
                "item": items_acabados[0],
                "subitem": items_base[0],
                "qntde_pre": 1,
                "qntde_usi": 1,
                "qntde_lix": 1,
            },
            {
                "item": items_acabados[0],
                "subitem": items_base[1],
                "qntde_pre": 2,
                "qntde_usi": 2,
                "qntde_lix": 2,
            },
            {
                "item": items_acabados[0],
                "subitem": items_base[2],
                "qntde_pre": 2,
                "qntde_usi": 2,
                "qntde_lix": 2,
            },
            {
                "item": items_acabados[0],
                "subitem": items_base[3],
                "qntde_pre": 1,
                "qntde_usi": 1,
                "qntde_lix": 1,
            },
            {
                "item": items_acabados[0],
                "subitem": items_base[4],
                "qntde_pre": 0,
                "qntde_usi": 1,
                "qntde_lix": 1,
            },
            # Acessórios finais
            {
                "item": items_acabados[0],
                "subitem": items_base[5],
                "qntde_pre": 0,
                "qntde_usi": 0,
                "qntde_lix": 1,
            },
            {
                "item": items_acabados[0],
                "subitem": items_base[6],
                "qntde_pre": 0,
                "qntde_usi": 0,
                "qntde_lix": 1,
            },
            # Sapato B (similar)
            {
                "item": items_acabados[1],
                "subitem": items_base[0],
                "qntde_pre": 1,
                "qntde_usi": 1,
                "qntde_lix": 1,
            },
            {
                "item": items_acabados[1],
                "subitem": items_base[1],
                "qntde_pre": 2,
                "qntde_usi": 2,
                "qntde_lix": 2,
            },
            # Sapato C (similar)
            {
                "item": items_acabados[2],
                "subitem": items_base[0],
                "qntde_pre": 1,
                "qntde_usi": 1,
                "qntde_lix": 1,
            },
            {
                "item": items_acabados[2],
                "subitem": items_base[1],
                "qntde_pre": 2,
                "qntde_usi": 2,
                "qntde_lix": 2,
            },
        ]
        
        estruturas = []
        for estrutura_data in estruturas_dados:
            estrutura, created = Estrutura.objects.get_or_create(
                item=estrutura_data["item"],
                subitem=estrutura_data["subitem"],
                defaults={
                    "qntde_pre": estrutura_data["qntde_pre"],
                    "qntde_usi": estrutura_data["qntde_usi"],
                    "qntde_lix": estrutura_data["qntde_lix"],
                },
            )
            estruturas.append(estrutura)
        
        return estruturas

    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("🔧 Iniciando população da estrutura base..."))
        self.stdout.write("")

        try:
            # 1. Criar Turnos
            self.stdout.write("1️⃣  Criando Turnos...")
            turnos = self._criar_turnos()
            self.stdout.write(
                self.style.SUCCESS(f"   ✓ {len(turnos)} turnos criados/existentes")
            )

            # 2. Criar Grupos
            self.stdout.write("2️⃣  Criando Grupos...")
            grupos = self._criar_grupos()
            self.stdout.write(
                self.style.SUCCESS(f"   ✓ {len(grupos)} grupos criados/existentes")
            )

            # 3. Criar Setores
            self.stdout.write("3️⃣  Criando Setores...")
            setores = self._criar_setores(grupos)
            self.stdout.write(
                self.style.SUCCESS(f"   ✓ {len(setores)} setores criados/existentes")
            )

            # 4. Criar Postos
            self.stdout.write("4️⃣  Criando Postos de Trabalho...")
            postos = self._criar_postos(setores)
            self.stdout.write(
                self.style.SUCCESS(f"   ✓ {len(postos)} postos criados/existentes")
            )

            # 5. Criar Máquinas
            self.stdout.write("5️⃣  Criando Máquinas...")
            maquinas = self._criar_maquinas(postos, turnos)
            self.stdout.write(
                self.style.SUCCESS(f"   ✓ {len(maquinas)} máquinas criadas/existentes")
            )

            # 6. Criar Famílias
            self.stdout.write("6️⃣  Criando Famílias de Produtos...")
            familias = self._criar_familias()
            self.stdout.write(
                self.style.SUCCESS(f"   ✓ {len(familias)} famílias criadas/existentes")
            )

            # 7. Criar Items Base
            self.stdout.write("7️⃣  Criando Itens Base (Sub-peças)...")
            items_base = self._criar_items_base()
            self.stdout.write(
                self.style.SUCCESS(f"   ✓ {len(items_base)} itens base criados/existentes")
            )

            # 8. Criar Items Acabados
            self.stdout.write("8️⃣  Criando Itens Acabados...")
            items_acabados = self._criar_items_acabados(familias[0], items_base)
            self.stdout.write(
                self.style.SUCCESS(
                    f"   ✓ {len(items_acabados)} itens acabados criados/existentes"
                )
            )

            # 9. Criar Estruturas (BOM)
            self.stdout.write("9️⃣  Criando Estruturas (Bill of Materials)...")
            estruturas = self._criar_estruturas(items_acabados, items_base)
            self.stdout.write(
                self.style.SUCCESS(
                    f"   ✓ {len(estruturas)} estruturas criadas/existentes"
                )
            )

            self.stdout.write("")
            self.stdout.write(self.style.SUCCESS("✅ Estrutura base populada com sucesso!"))
            self.stdout.write("")
            self.stdout.write(self.style.WARNING("📊 RESUMO DA ESTRUTURA CRIADA:"))
            self.stdout.write(f"  • Grupos: {len(grupos)} (Usinagem, Montagem, Acabamento)")
            self.stdout.write(f"  • Setores: {len(setores)} (CNC, Torno, Montagem, Linha Auto, Pintura, Lixamento)")
            self.stdout.write(f"  • Postos: {len(postos)}")
            self.stdout.write(f"  • Máquinas: {len(maquinas)}")
            self.stdout.write(f"  • Turnos: {len(turnos)}")
            self.stdout.write(f"  • Famílias: {len(familias)}")
            self.stdout.write(f"  • Itens Base: {len(items_base)}")
            self.stdout.write(f"  • Itens Acabados: {len(items_acabados)}")
            self.stdout.write(f"  • Estruturas (BOM): {len(estruturas)}")
            self.stdout.write("")
            self.stdout.write(self.style.SUCCESS("🚀 Pronto para criar Programações e Ordens de Produção!"))

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f"❌ Erro ao popular estrutura: {str(e)}")
            )
            raise

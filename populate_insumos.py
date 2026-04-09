#!/usr/bin/env python
"""
Script para carregar dados de exemplo de Insumos
Uso:
    cd "/home/odeclei/DEV/MRP James"
    python manage.py shell < populate_insumos.py
"""

from _itens.models import ComposicaoInsumo, Insumo, InsumoGroup, ItemBase
from _resources.models import Unidade_Medida

# Obter ou criar unidades de medida
un_kg, _ = Unidade_Medida.objects.get_or_create(
    sigla="kg", defaults={"descricao": "Quilograma"}
)
un_m, _ = Unidade_Medida.objects.get_or_create(
    sigla="m", defaults={"descricao": "Metro"}
)
un_l, _ = Unidade_Medida.objects.get_or_create(
    sigla="L", defaults={"descricao": "Litro"}
)
un_un, _ = Unidade_Medida.objects.get_or_create(
    sigla="un", defaults={"descricao": "Unidade"}
)

# Criar Grupos de Insumo
grupo_madeiras, _ = InsumoGroup.objects.get_or_create(
    codigo="MADEIRAS", defaults={"nome": "Matérias-Primas - Madeiras"}
)
grupo_tecidos, _ = InsumoGroup.objects.get_or_create(
    codigo="TECIDOS", defaults={"nome": "Matérias-Primas - Tecidos"}
)
grupo_espumas, _ = InsumoGroup.objects.get_or_create(
    codigo="ESPUMAS", defaults={"nome": "Matérias-Primas - Espumas"}
)
grupo_hardware, _ = InsumoGroup.objects.get_or_create(
    codigo="HARDWARE", defaults={"nome": "Matérias-Primas - Hardware"}
)
grupo_pintura, _ = InsumoGroup.objects.get_or_create(
    codigo="PINTURA", defaults={"nome": "Matérias-Primas - Pintura/Acabamento"}
)

# Criar Insumos - Madeiras
ins_pinus40, _ = Insumo.objects.get_or_create(
    codigo="MAD.PINUS.40MM",
    defaults={
        "nome": "Pinus 40mm - Tábua Bruta",
        "tipo": "madeira",
        "grupo": grupo_madeiras,
        "unidade_medida": un_kg,
        "especificacao": "40mm, padrão construtiva",
        "estoque_minimo": 100,
        "observacoes": "Fornecedor: Madeireira ABC. Prazo: 5 dias.",
        "is_active": True,
    },
)

ins_pinus30, _ = Insumo.objects.get_or_create(
    codigo="MAD.PINUS.30MM",
    defaults={
        "nome": "Pinus 30mm",
        "tipo": "madeira",
        "grupo": grupo_madeiras,
        "unidade_medida": un_kg,
        "especificacao": "30mm",
        "estoque_minimo": 80,
        "is_active": True,
    },
)

ins_tauari30, _ = Insumo.objects.get_or_create(
    codigo="MAD.TAUARI.30MM",
    defaults={
        "nome": "Tauari 30mm",
        "tipo": "madeira",
        "grupo": grupo_madeiras,
        "unidade_medida": un_kg,
        "especificacao": "30mm, madeira de lei",
        "estoque_minimo": 60,
        "observacoes": "Madeira mais nobre. Fornecedor: XYZ. Prazo: 10 dias.",
        "is_active": True,
    },
)

ins_mdf15, _ = Insumo.objects.get_or_create(
    codigo="MAD.MDF.15MM",
    defaults={
        "nome": "MDF 15mm",
        "tipo": "madeira",
        "grupo": grupo_madeiras,
        "unidade_medida": un_kg,
        "especificacao": "15mm, placa standard",
        "estoque_minimo": 120,
        "is_active": True,
    },
)

# Criar Insumos - Tecidos
ins_lona_preta, _ = Insumo.objects.get_or_create(
    codigo="TEC.LONA.PRETA",
    defaults={
        "nome": "Tecido Lona Preta",
        "tipo": "tecido",
        "grupo": grupo_tecidos,
        "unidade_medida": un_m,
        "especificacao": "1,5m de largura",
        "estoque_minimo": 50,
        "observacoes": "Resistente, alta durabilidade",
        "is_active": True,
    },
)

ins_suede, _ = Insumo.objects.get_or_create(
    codigo="TEC.SUEDE.CINZA",
    defaults={
        "nome": "Tecido Suede Cinza",
        "tipo": "tecido",
        "grupo": grupo_tecidos,
        "unidade_medida": un_m,
        "especificacao": "1,4m de largura",
        "estoque_minimo": 40,
        "observacoes": "Suede importado, toque macio",
        "is_active": True,
    },
)

# Criar Insumos - Espumas
ins_espuma_d28, _ = Insumo.objects.get_or_create(
    codigo="ESP.D28.ALMOFADA",
    defaults={
        "nome": "Espuma D28 - Almofada",
        "tipo": "espuma",
        "grupo": grupo_espumas,
        "unidade_medida": un_kg,
        "especificacao": "Densidade 28 kg/m³",
        "estoque_minimo": 200,
        "observacoes": "Conforto médio, durável",
        "is_active": True,
    },
)

ins_espuma_hr, _ = Insumo.objects.get_or_create(
    codigo="ESP.HR.ASSENTO",
    defaults={
        "nome": "Espuma HR - Assento",
        "tipo": "espuma",
        "grupo": grupo_espumas,
        "unidade_medida": un_kg,
        "especificacao": "Densidade 45 kg/m³",
        "estoque_minimo": 150,
        "observacoes": "Espuma de alta resiliência",
        "is_active": True,
    },
)

# Criar Insumos - Hardware
ins_parafuso_3x20, _ = Insumo.objects.get_or_create(
    codigo="HAR.PARAF.3X20",
    defaults={
        "nome": "Parafuso 3x20mm",
        "tipo": "hardware",
        "grupo": grupo_hardware,
        "unidade_medida": un_un,
        "especificacao": "3x20mm, zinco",
        "estoque_minimo": 1000,
        "is_active": True,
    },
)

ins_mola_metal, _ = Insumo.objects.get_or_create(
    codigo="HAR.MOLA.METAL",
    defaults={
        "nome": "Mola Espiral Metal",
        "tipo": "hardware",
        "grupo": grupo_hardware,
        "unidade_medida": un_un,
        "especificacao": "Mola de compressão",
        "estoque_minimo": 100,
        "is_active": True,
    },
)

# Criar Insumos - Pintura
ins_verniz_brilho, _ = Insumo.objects.get_or_create(
    codigo="PIN.VERNIZ.BRILHO",
    defaults={
        "nome": "Verniz Brilho",
        "tipo": "pintura",
        "grupo": grupo_pintura,
        "unidade_medida": un_l,
        "especificacao": "Verniz à base de água",
        "estoque_minimo": 20,
        "observacoes": "Secagem rápida, 4 horas",
        "is_active": True,
    },
)

ins_tinta_branca, _ = Insumo.objects.get_or_create(
    codigo="PIN.TINTA.BRANCA",
    defaults={
        "nome": "Tinta Branca Premium",
        "tipo": "pintura",
        "grupo": grupo_pintura,
        "unidade_medida": un_l,
        "especificacao": "Tinta acrílica",
        "estoque_minimo": 30,
        "is_active": True,
    },
)

print("✓ Insumos criados com sucesso!")
print("  - Grupos: 5")
print(f"  - Insumos: {Insumo.objects.count()}")

# Agora associar insumos a alguns ItemBase existentes (exemplo)
# Buscar um ItemBase existente se houver
itembase_list = ItemBase.objects.all()[:2]

if itembase_list:
    print("\n✓ Associando insumos a ItemBase existentes...")
    for ib in itembase_list:
        # Verificar se já tem composição
        if not ib.composicao_insumos.exists():
            # Adicionar alguns insumos padrão
            ComposicaoInsumo.objects.get_or_create(
                itembase=ib,
                insumo=ins_pinus40,
                defaults={"quantidade": 5, "observacoes": "Material principal"},
            )
            ComposicaoInsumo.objects.get_or_create(
                itembase=ib,
                insumo=ins_verniz_brilho,
                defaults={"quantidade": 0.5, "observacoes": "Acabamento"},
            )
            print(f"  ✓ {ib.itembase_cod} - 2 insumos adicionados")
else:
    print("\n⚠ Nenhum ItemBase existente ainda. Cadastre ItemBase primeiro!")

print("\n✓ Dados de exemplo carregados!")
print("\nPróximos passos:")
print("1. Acesse Admin > Insumos para verificar os dados")
print("2. Edite cada ItemBase e adicione os insumos específicos")
print("3. Use Import/Export para carregar seus próprios dados")

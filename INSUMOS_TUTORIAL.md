# 📋 Tutorial: Sistema de Insumos (Matérias-Primas)

## O que você perguntou

> "Item base seria o material utilizado? tipo pinus, tauari, mdf 15mm... entre outros?"

**Resposta:** Não exatamente. Criei um modelo separado para isso: **INSUMO**

---

## 🏗️ Hierarquia Completa

### Camada 1: INSUMO (Matérias-Primas) ⬅️ NOVO!

**Exemplos:**

- `MAD.PINUS.40MM` - Pinus 40mm
- `MAD.TAUARI.30MM` - Tauari 30mm
- `MAD.MDF.15MM` - MDF 15mm
- `TEC.LONA.PRETA` - Lona preta
- `ESP.D28.ALMOFADA` - Espuma D28
- `HAR.PARAF.3X20` - Parafuso 3x20mm
- `VER.BRILHO` - Verniz brilho

↓ (Composição de Insumos)

### Camada 2: ITEMBASE (Peças Produzidas)

**Exemplos:**

- `100.BASE.001` - Pé Traseiro
    - Usa: 5kg de Pinus 40mm
    - Usa: 0,5L de Verniz Brilho
    - Usa: 4x Parafuso 3x20mm

- `100.BASE.002` - Encosto com Mola
    - Usa: 3kg de Espuma D28
    - Usa: 2m de Tecido Lona Preta
    - Usa: 2x Mola espiral

↓ (Estrutura: composição da produção)

### Camada 3: ITEMACABADO (Produto Final)

**Exemplo:** `100.1054.22.01` - SF3 BRASILIS - PRATELEIRA LD

- **Para Pré:** 2x Pé Traseiro + 1x Encosto
- **Para Usinagem:** 1x Pé Traseiro
- **Para Lixamento:** 2x Pé Traseiro

↓ (Componentes Comprados separadamente)

### Camada 4: COMPONENTES (Itens Comprados)

**Exemplos:**

- Puxador cromado
- Tecido estofado
- Mola de conforto
- Rebite

---

## 🎯 Como Usar no Admin

### 1️⃣ Cadastrar Grupos de Insumos

```
Admin > Insumos > Grupos Insumos > [ADD]
Código: MADEIRAS
Nome: Matérias-Primas - Madeiras
```

### 2️⃣ Cadastrar Insumos (Matérias-Primas)

```
Admin > Insumos > Insumos > [ADD]

Informações Básicas:
  Código: MAD.PINUS.40MM
  Nome: Pinus 40mm - Tábua Bruta
  Tipo: Madeira
  Grupo: MADEIRAS
  Unidade de Medida: kg (ou m²)

Especificações:
  Especificação: 40mm
  Estoque Mínimo: 100 (quantidade mínima antes de alertar)

Outros:
  Observações: Fornecedor: Madeireira ABC - Prazo: 5 dias
  Ativo: ✓
```

### 3️⃣ Editar ItemBase e Adicionar Insumos

```
Admin > Itens Base > [Selecione um item] > [Edit]

Na seção "Composição de Insumo" (inline):
  [+] ADD Composição de Insumo
    Insumo: MAD.PINUS.40MM
    Quantidade Necessária: 5
    Observações: (opcional)

  [+] ADD Composição de Insumo
    Insumo: VER.BRILHO
    Quantidade Necessária: 0,5
    Observações: Pintura e acabamento

[Save]
```

---

## 📊 Exemplo Prático: Sofá 3 Lugares

```
Produto Final: 100.1054.22.01 - SF3 BRASILIS

├─ ItemBase: Pé Traseiro (100.BASE.001)
│  ├─ Insumo: Pinus 40mm ─── 5 kg
│  ├─ Insumo: Verniz ────── 0,5 L
│  └─ Insumo: Parafuso 3x20 ── 4 un
│
├─ ItemBase: Encosto (100.BASE.002)
│  ├─ Insumo: Espuma D28 ─── 3 kg
│  ├─ Insumo: Tecido Lona ── 2 m
│  └─ Insumo: Mola ──────── 2 un
│
├─ ItemBase: Assento (100.BASE.003)
│  ├─ Insumo: MDF 15mm ──── 2 m²
│  ├─ Insumo: Espuma ────── 4 kg
│  └─ Insumo: Tecido Lona ── 3 m
│
└─ Componentes (Comprados):
   ├─ Puxador cromado (2 un)
   ├─ Rodinha + mola (4 un)
   └─ Espuma de enchimento (10 kg)
```

---

## 📥 Import/Export (Batch)

### Exportar Insumos para Excel

```
Admin > Insumos > Insumos > [Tab Export]
Formato: XLSX ou CSV
[Download]
```

### Importar Insumos em Lote

Prepare arquivo CSV:

```
codigo,nome,tipo,especificacao
MAD.PINUS.40MM,Pinus 40mm,madeira,40mm
MAD.TAUARI.30MM,Tauari 30mm,madeira,30mm
TEC.LONA.PRETA,Lona Preta,tecido,
ESP.D28,Espuma D28,espuma,
```

Depois:

```
Admin > Insumos > Insumos > [Tab Import]
[Choose File] > insumos.csv
[Validate] > [Import]
```

---

## ✅ Benefícios

**Antes (sem Insumo):**

```
ItemBase = "Encosto com Mola"
Sem saber exatamente:
- quantos kg de espuma usa?
- qual verniz?
- qual tecido?
```

**Depois (com Insumo):**

```
ItemBase: Encosto com Mola
├─ Espuma D28: 3 kg ✓
├─ Tecido Lona: 2 m ✓
├─ Mola: 2 un ✓
└─ Verniz Brilho: 0,5 L ✓

Totalmente rastreável + cálculo automático de custos!
```

---

## 🔧 Próximos Passos

1. **Cadast
   re Insumos** no admin
    - Comece com madeiras
    - Depois tecidos, espumas, hardware

2. **Edite cada ItemBase**
    - Adicione os insumos que usa
    - Indique as quantidades necessárias

3. **Sistema calculará automaticamente:**
    - Custo total de cada ItemBase
    - Custo total de cada ItemAcabado
    - Alertas se falta insumo

4. **Dashboard mostrará:**
    - Insumos com baixo estoque
    - Produtos que não podem ser fabricados
    - Custo de produção por item

---

## 📌 Resumo Rápido

| Nível          | O que é               | Exemplo                      |
| -------------- | --------------------- | ---------------------------- |
| 🌾 Insumo      | Matéria-prima bruta   | Pinus 40mm, Tecido, Parafuso |
| 🏭 ItemBase    | Peça fabricada        | Pé Traseiro, Encosto         |
| 🛋️ ItemAcabado | Produto final         | Sofá 3 Lugares               |
| 🛒 Componentes | Item comprado externo | Puxador, Rodinha             |

---

**Dúvidas?** Consulte este arquivo ou a documentação em `/memories/repo/material-hierarchy.md`

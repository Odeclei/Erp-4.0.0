# 📋 Estrutura Base - Guia de Uso

## Visão Geral

O command `populate_base_structure` cria uma estrutura genérica completa no banco de dados, permitindo que você comece a gerar **Programações e Ordens de Produção** imediatamente.

## ✅ O que foi criado

Ao executar `python manage.py populate_base_structure`, o sistema cria:

### 1. **Organização de Produção**
- **3 Grupos**: Usinagem, Montagem, Acabamento
- **6 Setores**: CNC, Torno, Montagem Manual/Automatizada, Pintura, Lixamento
- **10 Postos de Trabalho**: Máquinas/estações organizadas por setor
- **10 Máquinas**: CNC01-02, TORN01-02, MONT01-02, AUTO01, PINT01-02, LIXA01

### 2. **Turno Padrão**
- **Turno Manhã**: 7h00 às 15h00 (1h30 almoço)
- **Turno Tarde**: 15h00 às 23h00 (30min almoço)

### 3. **Produtos (Itens Acabados)**
```
SA-001: Sapato A
├─ 100 peças/dia
├─ Solado (1×), Pé Traseiro (2×), Pé Dianteiro (2×)
├─ Língüeta, Ilhóses, Etiqueta, Caixa
└─ Família: Sapatos

SA-002: Sapato B (80 peças/dia)
SA-003: Sapato C (120 peças/dia)
```

### 4. **Sub-peças (Itens Base)**
- PB-001: Solado
- PB-002: Pé Traseiro
- PB-003: Pé Dianteiro
- PB-004: Língüeta
- PB-005: Ilhóses
- AC-001: Etiqueta
- AC-002: Caixa

### 5. **Estruturas (Bill of Materials)**
11 relações pré-configuradas entre itens e sub-peças com quantidades por fase:
- **qntde_pre**: Quantidade na fase PRÉ (reaproveitamento)
- **qntde_usi**: Quantidade na fase USINAGEM (transformação)
- **qntde_lix**: Quantidade na fase LIXAMENTO (acabamento)

---

## 🚀 Como usar para criar Programações

### **1️⃣ Via Admin Django**

1. Acesse `/admin/`
2. Navegue até **PPCP > Manufacturing Orders**
3. Clique em **"Add Manufacturing Order"**
4. Preencha:
   - Nome da ordem
   - Data de início/conclusão
   - Status (Aberto, Em Progresso, Concluído)
5. Clique em **Item Programacao** para adicionar itens:
   - Selecione item (SA-001, SA-002, SA-003)
   - Quantidade a produzir
   - Datas de início/fim
6. Clique em **Sub Item Programacao** para detalhar sub-peças:
   - Selecione subproduto (PB-001, PB-002, etc.)
   - Quantidades por fase (pré, usinagem, lixamento)

### **2️⃣ Via Programação Programática**

```python
from ppcp.models import ManufacturingOrder, ItemProgramacao, SubItemProgramacao
from _itens.models import ItemAcabado, ItemBase
from datetime import date

# 1. Criar ordem
ordem = ManufacturingOrder.objects.create(
    name="Produção Sapatos - Abril/2026",
    status="aberto",
    data_inicio=date(2026, 4, 1),
    data_conclusao=date(2026, 4, 30)
)

# 2. Adicionar itens à ordem
item = ItemAcabado.objects.get(item_cod="SA-001")
item_prog = ItemProgramacao.objects.create(
    programacao=ordem,
    item=item,
    qtde_programada=1000,  # total para o mês
    data_inicio_programada=date(2026, 4, 1),
    data_conclusao_programada=date(2026, 4, 15)
)

# 3. Adicionar sub-peças
sub_peça = ItemBase.objects.get(itembase_cod="PB-002")
SubItemProgramacao.objects.create(
    produto_programado=item_prog,
    subproduto=sub_peça,
    qtde_pre=0,      # não precisa na fase PRÉ
    qtde_usi=1000,   # 1000 unidades de montagem
    qtde_lix=1000    # 1000 unidades de acabamento
)
```

### **3️⃣ Registrar Apontamentos Diários**

Após criar as programações, registre a produção diária:

```bash
# Via Admin
/admin/apont/registroapontamento/
```

Registre para cada máquina/dia:
- Máquina: MONT01
- Data: 2026-04-01
- Apontamento: SA-001
- SubPeça: PB-002 (Pé Traseiro)
- Qtde Programada: 200
- Qtde Produzida Boa: 195
- Qtde Refugo: 5
- Tempo: 7:00 às 15:00

---

## 📊 Fluxo Completo de Uso

```
1. Criar Grupos/Setores/Máquinas
   ↓ (Já feito via populate_base_structure)
   ↓
2. Cadastrar Itens Acabados (Produtos)
   ↓ (SA-001, SA-002, SA-003 já existem)
   ↓
3. Cadastrar Itens Base (Sub-peças)
   ↓ (PB-001 até AC-002 já existem)
   ↓
4. Definir Estruturas (Quantidades necessárias)
   ↓ (11 estruturas já configuradas)
   ↓
5. Criar Programação/Ordem de Produção
   ↓ (Defina o que produzir e quando)
   ↓
6. Registrar Apontamentos Diários
   ↓ (Registre quanto foi produzido)
   ↓
7. Calcular OEE
   └─→ python manage.py calcular_oee --dias 7
```

---

## 🔧 Customizações Futuras

Se precisar adicionar mais dados:

1. **Duplicar command**:
   ```bash
   cp rule/management/commands/populate_base_structure.py \
      rule/management/commands/populate_production_data.py
   ```

2. **Editar** com mais grupos, máquinas, produtos, etc.

3. **Executar**:
   ```bash
   python manage.py populate_production_data
   ```

---

## 📝 Notas Importantes

- ✅ O command é **idempotente**: pode rodar múltiplas vezes sem duplicar dados
- ✅ **Turnos de 9 horas** (7:00-15:00 e 15:00-23:00) são padrão
- ✅ **Velocidade de cálculo OEE** agora é dinâmica por subproduto
  - Sapato A: 100/dia → 11.11 peças/hora
  - Pé Traseiro: (100×2)/9 → 22.22 peças/hora
- ⚠️ Para alterar quantidades de sub-peças, edite a tabela `Estrutura` no admin
- ⚠️ Para adicionar novas máquinas, use `/admin/rule/machines/`

---

## 🆘 Troubleshooting

**Q: Erro "Cannot resolve keyword 'name'"**
A: Verifique os nomes dos campos do modelo (use `description`, não `name`)

**Q: As máquinas não aparecem em algumas opções**
A: Certifique-se que `is_active = True` na máquina

**Q: OEE dando 0% ou valores estranhos**
A: Verifique se os apontamentos têm `subproduto` preenchido e se a Estrutura existe

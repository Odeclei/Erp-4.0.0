# 📊 Sistema de Cálculo de OEE - Guia de Uso

## O que foi implementado

### 1. **Modelo de Dados Unificado**

#### Apontamentos de Produção (`RegistroApontamento`)
Cada apontamento registra:
- **Máquina** que realizou o trabalho
- **Data** do apontamento
- **Tempos**: hora início/fim de setup e produção
- **Quantidades**: programada, boa, refugo, retrabalho
- **Classificação**: tipo de apontamento, motivo de retrabalho
- **Status**: aberto, concluído ou cancelado

#### Paradas (`Stops`)
Cada parada registra:
- **Máquina** que parou
- **Data/Hora** exata
- **Motivo**: categoria e subcategoria
- **Duração**: em segundos

#### Indicadores Diários (`IndicadorDesempenho`)
Calculado automaticamente com base em apontamentos e paradas:
```
OEE = Disponibilidade × Performance × Qualidade

Disponibilidade = Tempo funcional / Tempo total × 100%
  ├─ Tempo total = 8h (turno padrão, configurável)
  └─ Tempo funcional = Tempo total - Tempo parado

Performance = Quantidade produzida / Quantidade teórica × 100%
  ├─ Quantidade teórica = Tempo produção (h) × 60 peças/hora
  └─ (60 peças/hora é o padrão, pode ser customizado)

Qualidade = Peças boas / Total de peças × 100%
  ├─ Total = Boas + Refugo + Retrabalho
```

---

## 📱 Acessando o Sistema

### 1. **Dashboard Visual** (Gráficos em tempo real)
```
http://localhost:8000/desempenho/dashboard/
```
Mostra:
- 4 KPIs principais (OEE, Disponibilidade, Performance, Qualidade)
- Tendência dos últimos 7 dias em gráfico
- Top 5 máquinas com melhor OEE
- Top 5 máquinas com pior OEE (para investigar)

### 2. **Admin Django** (CRUD + Relatórios)
```
http://localhost:8000/admin/
```
Seções:
- **Apontamentos > Apontamento de Produção** - Registrar apontamentos do dia
- **Apontamentos > Parada de Produção** - Registrar paradas de máquina
- **Desempenho > Indicador de Desempenho** - Visualizar OEE calculado
- **Desempenho > Resumo Setor** - OEE agregado por setor
- **Desempenho > Resumo Grupo** - OEE agregado por grupo

### 3. **APIs REST** (Para integração com outros sistemas)
```
GET /desempenho/api/hoje/                    # KPIs consolidados do dia
GET /desempenho/api/maquina/<id>/?dias=7    # Histórico de máquina
GET /desempenho/api/setor/<id>/?dias=7      # Histórico de setor
GET /desempenho/api/grupo/<id>/?dias=7      # Histórico de grupo
```

---

## 💻 Usando via Command Line

### Calcular OEE de Hoje
```bash
python manage.py calcular_oee
```

### Calcular OEE dos Últimos 7 Dias
```bash
python manage.py calcular_oee --dias 7
```

### Calcular OEE de Data Específica
```bash
python manage.py calcular_oee --data 2026-04-01
```

### Calcular OEE de Máquina Específica
```bash
python manage.py calcular_oee --maquina 1
```

### Calcular Resumo de Grupo Específico
```bash
python manage.py calcular_oee --grupo 1
```

---

## 🎯 Fluxo de Uso Típico

### Dia do Trabalho (Operário)
1. **Às 17h** (fim do turno): Abrir Django Admin
2. Ir para "Apontamento de Produção"
3. Adicionar registros do dia:
   - Máquina: PE-f-015
   - Data: Hoje
   - Hora início produção: 08:00
   - Hora fim produção: 16:00
   - Qtde programada: 50
   - Qtde produzida (boa): 48
   - Qtde refugo: 2
   - Status: Concluído
4. Se houve pausas, adicionar em "Parada de Produção"

### No Mesmo Dia (Gerente)
1. Executar: `python manage.py calcular_oee`
2. Acessar Dashboard: `/desempenho/dashboard/`
3. Visualizar OEE do dia
4. Se OEE < 70%, investigar máquinas com pior performance

### Análise Semanal/Mensal
1. Acessar Dashboard
2. Gráfico mostra tendência automática
3. Clique em setor/máquina específica para detalhar
4. Use API para exportar dados para BI/Excel

---

## 🔧 Configurações

### Velocidade de Produção Padrão (peças/hora)
**Arquivo:** `desempenho/services.py`
**Propriedade:** `VELOCIDADE_PRODUCAO_PADRAO = 60.0`

Para mudar:
```python
# desempenho/services.py
class DesempenhoService:
    VELOCIDADE_PRODUCAO_PADRAO = 100.0  # Altere para sua realidade
```

### Limite Mínimo de OEE para "Excelente"
Automático no dashboard:
- ✓ Excelente: >= 85%
- ⚠️ Bom: >= 70%
- ✗ Ruim: < 70%

---

## 📊 Exemplo de Resposta de API

```json
GET /desempenho/api/hoje/

{
  "data": "09/04/2026",
  "kpis": {
    "oee_media": 82.5,
    "disponibilidade_media": 90.2,
    "performance_media": 94.1,
    "qualidade_media": 96.8
  },
  "producao": {
    "qtde_maquinas_ativas": 5,
    "qtde_produzida": 245,
    "qtde_refugo": 8
  },
  "setores": [
    {
      "setor": "Preparação",
      "oee": 85.3,
      "maquinas": 2
    },
    {
      "setor": "Usinagem",
      "oee": 79.7,
      "maquinas": 3
    }
  ]
}
```

---

## ✨ Próximos Passos para Impressionar Investidor

### Fase 2: Relatórios Avançados (Próxima semana)
- [ ] Relatório em PDF com gráficos
- [ ] Exportar para Excel com histórico de 30 dias
- [ ] Comparativo período anterior (mês passado vs este mês)
- [ ] Alertas automáticos (email quando OEE < 70%)

### Fase 3: Machine Learning (Futuro)
- [ ] Previsão de quebras baseada em padrões históricos
- [ ] Recomendação automática de ações (ex: "máquina X precisa revisão")
- [ ] Otimização de sequência de produção

### Fase 4: Integração
- [ ] Sincronizar com ERP/SAP
- [ ] Webhook para notificações em tempo real
- [ ] Grafana/Tableau para BI empresarial

---

## 🆘 Troubleshooting

### OEE aparece zerado no dashboard
**Solução:** Execute `python manage.py calcular_oee` para popular dados

### Máquina não aparece no Dashboard
**Verificar:** Machine está marcada como `active=True` em rule/Machines

### Performance baixa com muitos dados
**Solução:** Use índices em desempenho/models.py
```python
class IndicadorDesempenho(models.Model):
    class Meta:
        indexes = [
            models.Index(fields=['machine', '-data']),
        ]
```

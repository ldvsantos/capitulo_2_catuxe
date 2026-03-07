# Diagnóstico do Estado Atual e Próximos Passos da Pesquisa

**Artigo 2 — Meta-análise Quantitativa das Dimensões de Vulnerabilidade Biocultural**  
**Data do diagnóstico:** 03 de março de 2026 (atualizado — pipeline completo)

---

## 1. Estado Atual — O que já está pronto

| Estágio | Artefato | Status |
|---|---|---|
| Busca automatizada | `08_busca_scopus_wos.py` → 365 registros (193 Scopus + 172 WoS) | ✅ Completo |
| Deduplicação | 117 duplicatas removidas → 193 únicos | ✅ Completo |
| Triagem semântica | 48 estudos elegíveis (de 193); 1 excluído na codificação (ID=36) → **47 finais** | ✅ Completo |
| Obtenção de PDFs | 39 PDFs obtidos (40 arquivos na pasta) | ✅ Parcial |
| Extração estruturada | `bd_extracao_PREENCHIDO.xlsx` com 288 linhas (48 × 6 dim), 27 colunas | ✅ Completo |
| Codificação qualitativa | `bd_codificacao_qualitativa.xlsx` com 205/205 registros (100%) | ✅ **COMPLETO** |
| Conversão quali → lnRR | `31_converter_quali_para_lnRR.py` → 222 registros, k=37/dim | ✅ **COMPLETO** |
| Integração multi-tier | `02b_integrar_evidencia_mista.R` → `bd_lnRR_misto.rds` | ✅ **COMPLETO** |
| Meta-análise por dimensão | `03_meta_analise_dimensao.R` → `resultados_por_dimensao.rds` | ✅ **COMPLETO** |
| Meta-regressão | `04_meta_regressao.R` → `meta_regressao.rds` | ✅ **COMPLETO** |
| Viés e sensibilidade | `05_vies_sensibilidade.R` → funnel plots, trim-and-fill, LOO | ✅ **COMPLETO** |
| Forest plots | `06_forest_plots.R` → 8 PDFs + 1 PNG | ✅ **COMPLETO** |
| Outputs ISB | `07_outputs_ISB.R` → ranking, heterogeneidade, fuzzy | ✅ **COMPLETO** |
| Diagrama PRISMA | Gerado em PDF/PNG/SVG/HTML (PT e EN) | ✅ Completo |
| Manuscrito LaTeX | Intro, Métodos completos, Resultados parciais, Conclusão | ⏳ ~85% |
| Modelo bayesiano | `03b_modelo_bayesiano_brms.R` | ⏳ Opcional (requer Stan) |

### ✅ Gargalo Crítico RESOLVIDO

O pipeline multi-tier converteu toda a evidência qualitativa em tamanhos de efeito (lnRR):

| Métrica | Valor |
|---|---|
| Total estudos finais | **47** (48 − 1 excluído ID=36) |
| Registros convertidos | **222** na etapa legada, posteriormente rearticulados para a arquitetura V1–V8 |
| T1 (mean±SD direto) | 18 (5 estudos) |
| T2a (p-value → lnRR) | 21 |
| T2b (ANOVA → lnRR) | 21 |
| T3 (ordinal com tabelas) | 74 |
| T4 (qualitativo puro) | 88 |
| Status por dimensão | **Todas confirmatórias (k=37)** |

### Resultados-Chave da Meta-Análise

| Dimensão | lnRR | IC 95% | I² | Interpretação |
|---|---|---|---|---|
| V1 Erosão Intergeracional | −0.017 | [−0.24, 0.21] | 14.8% | Neutro (NS) |
| V2 Complexidade Biocultural | +0.045 | [−0.07, 0.16] | 2.4% | Neutro (NS) |
| V3 Singularidade Territorial | +0.072 | [−0.09, 0.23] | 6.1% | Neutro (NS) |
| V4 Status de Documentação | +0.007 | [−0.21, 0.22] | 7.6% | Neutro (NS) |
| **V5 Vulnerabilidade Jurídica** | **−0.279** | **[−0.49, −0.06]** | **30.7%** | **Vulnerabilidade significativa** |
| V6 Organização Social | +0.172 | [−0.05, 0.40] | 8.4% | Marginal (NS, p≈0.13) |

---

## 2. Classificação Final dos 47 Estudos por Tier de Evidência

| Tier | Significado | Registros (222 total) | % |
|---|---|:---:|:---:|
| T1 | mean±SD direto → lnRR | 18 | 8.1% |
| T2a | p-value → z → d → lnRR | 21 | 9.5% |
| T2b | ANOVA threshold p → lnRR | 21 | 9.5% |
| T3 | Ordinal com tabela cruzada → lnOR → lnRR | 74 | 33.3% |
| T4 | Qualitativo puro → ordinal → lnOR → lnRR (σ×1.5) | 88 | 39.6% |

**Nota:** ID=36 excluído da codificação (dados insuficientes). O total de 222 registros refere-se à etapa legada de conversão, anterior à consolidação final da arquitetura V1–V8.

### Estudos T1 (mean±SD direto)

| ID | Dims | Detalhes |
|---|---|---|
| 18 | V1, V2 | SOC%, slope accuracy (Nord et al.) |
| 20 | V2-V6 | Ethnobotanical knowledge scores |
| 31 | V1, V2, V5, V6 | Land-cover diversity (Frascaroli) |
| 45 | Multidimensional | Farm diversity metrics |
| 47 | Multidimensional | Farm/food security (Rodriguez-Cruz) |

---

## 3. Próximos Passos (ordem de prioridade)

### ✅ FASE 1 — Completar base de evidência — CONCLUÍDA

- ✅ Codificação qualitativa: 205/205 registros (100%)
- ✅ Classificação multi-tier: T1–T4 atribuída a todos os registros
- ✅ PDFs sem acesso tratados como T4 com inflação de variância
- ✅ ID=36 excluído (dados insuficientes)

### ✅ FASE 2 — Pipeline Estatístico — CONCLUÍDA

- ✅ Script 31: conversão quali → lnRR (222 registros)
- ✅ Script 02b: integração multi-tier → `bd_lnRR_misto.rds`
- ✅ Script 03: meta-análise por dimensão (modelo rma.mv 3 níveis)
- ✅ Script 04: meta-regressão (Tipo_Intervencao + Regiao + Tipo_Comunidade)
- ✅ Script 05: viés de publicação + sensibilidade (tier, ρ, LOO, trimfill)
- ✅ Script 06: forest plots (8 PDFs + 1 PNG)
- ✅ Script 07: outputs ISB (ranking, heterogeneidade, fuzzy)
- ⛔ Script 02: MICE desativado (94% missing — impraticável)
- ⏳ Script 03b: modelo bayesiano (opcional, requer Stan/tidybayes)

### ⏳ FASE 3 — Completar Manuscrito

**Passo 1. Atualizar Resultados (§3.2–3.5)** ⭐ PRÓXIMO  
Substituir texto placeholder por resultados reais:
- Rankings de $\overline{lnRR}$ por dimensão (V1–V8) — dados em `resultados_por_dimensao.xlsx`
- Índices de heterogeneidade ($I^2$, $\tau^2$) — dados em `resultados_por_dimensao.rds`
- Coeficientes de meta-regressão — dados em `coeficientes_meta_regressao.xlsx`
- Referências a forest plots e funnel plots gerados

**Passo 2. Completar GAPs no texto**  
O manuscrito tem marcadores `[GAP CRÍTICO:]` que precisam ser preenchidos.

**Passo 3. Atualizar PROSPERO**  
Substituir `CRD42024xxxxxx` pelo número real ou remover referência.

### ⏳ FASE 4 — Finalização para Submissão

**Passo 4. Verificar references.bib**  
- Compilar LaTeX e verificar [?] warnings

**Passo 5. Tradução PT → EN**  
O periódico-alvo (*Biodiversity and Conservation*) exige inglês.

**Passo 6. Checklist PRISMA 2020**  
Preencher como material suplementar.

**Passo 7. Data availability + Repositório**  
- Criar repositório GitHub/Zenodo
- Atualizar URL no manuscrito

**Passo 8. Converter template para Elsevier**  
O manuscrito usa `elsarticle.cls` — verificar conformidade com guidelines do periódico-alvo.

---

## 4. Resumo Visual do Pipeline Completo

```
PIPELINE EXECUTADO                  STATUS
═══════════════════                 ══════

47 estudos finais (ID=36 excl.)     FASE 1: EVIDÊNCIA ✅ COMPLETA
    │                               ┌─────────────────────────────────────┐
    ├── 18 T1 (mean±SD)  ─────────► │ Codificação: 205/205 (100%)         │
    ├── 21 T2a (p→d→lnRR) ───────► │ Conversão: 222 registros            │
    ├── 21 T2b (ANOVA→lnRR) ─────► │ k = 37 por dimensão                 │
    ├── 74 T3 (ordinal→lnOR) ────► │ Todos confirmatórios                │
    └── 88 T4 (quali→lnOR×1.5) ──► │                                     │
                                    └─────────────────────────────────────┘
         │                                     │
         ▼                                     ▼
    bd_lnRR_misto.rds               FASE 2: PIPELINE ✅ COMPLETO
         │                          ┌─────────────────────────────────────┐
         ├── rma.mv 3 níveis ─────► │ 03: Meta-análise (V1–V8)            │
         ├── Meta-regressão ──────► │ 04: 3 moderadores                   │
         ├── Viés + sensibil. ───► │ 05: Funnel, LOO, trimfill, tier      │
         ├── Forest plots ────────► │ 06: 8 PDFs + 1 PNG                  │
         └── ISB outputs ─────────► │ 07: Ranking, fuzzy, hetero           │
                                    └─────────────────────────────────────┘
                                               │
    V5 SIGNIFICATIVO (p<0.05)                  ▼
    lnRR = -0.279 [-0.49, -0.06]    FASE 3-4: MANUSCRITO ⏳ PENDENTE
    I² = 30.7%                      ┌─────────────────────────────────────┐
                                    │ Atualizar §3.2–3.5 com resultados   │
    44 arquivos em 3-OUTPUT/        │ Preencher GAPs, traduzir EN          │
                                    │ Verificar .bib, submeter             │
                                    └─────────────────────────────────────┘
```

---

## 5. Inventário Atualizado de Arquivos

### Scripts (1-LATEX/2-DADOS/1-SCRIPTS/)

| Script | Função | Status |
|---|---|---|
| `00_setup.R` | Instalação de pacotes | ✅ Pronto |
| `01_revisao_sistematica.R` | Triagem semântica, PRISMA | ✅ Executado |
| `02_extracao_dados.R` | MICE, lnRR, diagnóstico k | ⛔ Desativado (94% missing) |
| `02b_integrar_evidencia_mista.R` | Integração multi-tier | ✅ Executado |
| `03_meta_analise_dimensao.R` | Modelo hierárquico 3 níveis | ✅ Executado |
| `03b_modelo_bayesiano_brms.R` | Modelo bayesiano alternativo | ⏳ Opcional |
| `04_meta_regressao.R` | Meta-regressão | ✅ Executado |
| `05_vies_sensibilidade.R` | Viés de publicação | ✅ Executado |
| `06_forest_plots.R` | Forest plots | ✅ Executado |
| `07_outputs_ISB.R` | Outputs consolidados | ✅ Executado |
| `08–09` | Busca e integração | ✅ Executado |
| `10_gerar_prisma.R` | Diagrama PRISMA | ✅ Executado |
| `11–26` | Extração automatizada PDFs | ✅ Executados |
| `30_preparar_codificacao_quali.py` | Prepara planilha codificação | ✅ Executado |
| `31_converter_quali_para_lnRR.py` | Conversão ordinal → lnRR | ✅ Executado |

### Dados (1-LATEX/2-DADOS/2-BANCO_DADOS/)

| Subpasta/Arquivo | Conteúdo | Status |
|---|---|---|
| `1-ARTIGOS_SELECIONADOS/` | 40 PDFs | ✅ 39/48 obtidos |
| `2-DADOS_TABULADOS/bd_extracao_PREENCHIDO.xlsx` | 288 linhas, 27 colunas | ✅ Completo |
| `2-DADOS_TABULADOS/bd_codificacao_qualitativa.xlsx` | 205 registros codificados | ✅ Completo |
| `2-DADOS_TABULADOS/bd_extracao_convertido.xlsx` | 222 registros com lnRR + vi | ✅ Gerado |
| `2-DADOS_TABULADOS/diagnostico_tiers.xlsx` | Classificação por tier | ✅ Gerado |
| `2-DADOS_TABULADOS/diagnostico_evidencia_mista.xlsx` | Diagnóstico integração | ✅ Gerado |
| `3-BIB_EXPORTS/consolidado_final.bib` | Bibliografia unificada | ✅ |
| `3-OUTPUT/` | JSONs de extração + 44 outputs | ✅ |

### Outputs do Pipeline (1-LATEX/2-DADOS/3-OUTPUT/)

| Arquivo | Descrição | Status |
|---|---|---|
| `bd_lnRR_misto.rds` | Base integrada multi-tier | ✅ |
| `resultados_por_dimensao.rds/.xlsx` | Resultados meta-análise V1–V8 | ✅ |
| `meta_regressao.rds` | Modelo meta-regressão | ✅ |
| `coeficientes_meta_regressao.xlsx` | Coeficientes estimados | ✅ |
| `subgrupos.xlsx` / `moderadores_exploratoria.xlsx` | Análise subgrupos | ✅ |
| `forest_V1.pdf` ... `forest_V8.pdf` | Forest plots por dimensão | ✅ |
| `forest_agregado_V1_V8.pdf/.png` | Forest plot agregado | ✅ |
| `forest_ggplot_V1_V8.pdf/.png` | Forest plot ggplot | ✅ |
| `funnel_V1.pdf` ... `funnel_V8.pdf` | Funnel plots | ✅ |
| `vies_publicacao.xlsx` / `trimfill.xlsx` | Diagnóstico viés | ✅ |
| `leave_one_out.xlsx` | Análise sensibilidade LOO | ✅ |
| `sensibilidade_rho.xlsx` / `sensibilidade_tier.xlsx` | Sensibilidade ρ e tier | ✅ |
| `sensibilidade_DL_REML.xlsx` | Comparação DL vs REML | ✅ |
| `tabela_ISB_consolidada.xlsx` | Tabela ISB final | ✅ |
| `ranking_lnRR.xlsx` | Ranking por lnRR | ✅ |
| `mapa_heterogeneidade.xlsx` | Mapa de heterogeneidade | ✅ |
| `universos_discurso_fuzzy.xlsx` | Fuzzy membership | ✅ |
| Diagrama PRISMA | PDF, PNG, SVG, HTML (PT+EN) | ✅ |

### Figuras (1-LATEX/3-FIGURAS/)

| Arquivo | Status |
|---|---|
| `methods_flowchart.pdf` | ✅ |
| `prisma_flowdiagram_artigo2_en.pdf` | ✅ |

---

## 6. Métricas de Progresso

| Componente | Progresso | Notas |
|---|:---:|---|
| Busca/Triagem | 100% | 47 estudos finais (48 − 1 excl.) |
| Obtenção PDFs | 81% | 39/48 obtidos; 9 como T4 (abstract) |
| Extração estrutural | 100% | 288 linhas preenchidas |
| Codificação qualitativa | **100%** | 205/205 registros codificados |
| Conversão multi-tier | **100%** | 222 registros (lnRR + vi) |
| Pipeline estatístico | **100%** | 03→04→05→06→07 executados |
| Figuras | **100%** | Forest plots, funnel plots, PRISMA |
| Manuscrito | ~85% | **Falta inserir resultados reais** |
| Modelo bayesiano | 0% | Opcional (requer Stan + tidybayes) |

---

## 7. Decisões Tomadas e Pendentes

### Decisões Tomadas

1. **Estudos sem PDF (n=9):** ✅ Mantidos como Tier 4 com inflação de variância (σ×1.5)
2. **Codificação qualitativa:** ✅ 205 registros codificados (100%), protocolo multi-tier aplicado
3. **MICE (script 02):** ⛔ Desativado — 94% missing torna imputação impraticável. Pipeline usa abordagem multi-tier diretamente
4. **ID=36:** ⛔ Excluído na codificação (dados insuficientes)
5. **Moderadores:** ✅ Tipo_Intervencao + Regiao + Tipo_Comunidade (Tempo_Intervencao e NOS removidos: 100% missing)

### Decisões Pendentes

1. **Modelo bayesiano:** Executar `03b_modelo_bayesiano_brms.R` como sensibilidade? Requer instalação de Stan + tidybayes
2. **PROSPERO:** Número de registro ainda é placeholder (`CRD42024xxxxxx`)
3. **Periódico-alvo:** Confirmar se é *Biodiversity and Conservation* (Springer) ou outro. Template atual é `elsarticle.cls` (Elsevier)

---

## 8. PDFs Não Obtidos (tratados como T4)

IDs sem acesso ao PDF: 1, 23, 24, 26, 28, 33, 34, 40, 42 (n=9).  
Todos tratados como Tier 4 na meta-análise com inflação de variância.  
Se PDFs forem obtidos futuramente, podem ser reclassificados para tier superior.

---

## 9. Cronograma Atualizado

| Etapa | Atividade | Status |
|---|---|---|
| ✅ Concluído | Codificação qualitativa (205/205) | 100% |
| ✅ Concluído | Pipeline estatístico completo (31→02b→03→04→05→06→07) | 100% |
| ✅ Concluído | Geração de 44 outputs (figuras, tabelas, diagnósticos) | 100% |
| ⏳ Próximo | Inserir resultados reais no manuscrito (§3.2–3.5) | Pendente |
| ⏳ Próximo | Preencher GAPs e placeholders no LaTeX | Pendente |
| ⏳ Futuro | Verificar references.bib + compilar LaTeX | Pendente |
| ⏳ Futuro | Tradução PT → EN | Pendente |
| ⏳ Futuro | Checklist PRISMA 2020 como suplementar | Pendente |
| ⏳ Futuro | Repositório GitHub/Zenodo + data availability | Pendente |
| ⏳ Opcional | Modelo bayesiano (03b) como sensibilidade | Pendente |

# ================================================================
# 07_outputs_ISB.R — Consolidação dos 4 outputs para o ISB
# Artigo 2: Meta-análise de vulnerabilidade biocultural (V1–V8)
#
# Gera a tabela-resumo com as 4 entregas quantitativas que
# alimentam o Índice de Salvaguarda Biocultural (ISB):
#   1. Ranking de lnRR por dimensão
#   2. Mapa de heterogeneidade (I², τ²)
#   3. Coeficientes de moderadores (meta-regressão)
#   4. Universos de discurso (IC 95%) p/ funções de pertinência fuzzy
# ================================================================

source("00_setup.R")

res_dim <- readRDS(file.path(DIR_OUTPUT, "resultados_por_dimensao.rds"))
mr      <- readRDS(file.path(DIR_OUTPUT, "meta_regressao.rds"))

# ---------------------------------------------------------------
# Nomes das dimensões
# ---------------------------------------------------------------

nomes_dim <- c(
  "V1" = "Erosao Intergeracional",
  "V2" = "Complexidade Biocultural",
  "V3" = "Status de Documentacao",
  "V4" = "Vulnerabilidade Juridica",
  "V5" = "Organizacao Social",
  "V6" = "Vitalidade Linguistica",
  "V7" = "Integracao ao Mercado",
  "V8" = "Exposicao Climatica"
)

# ===============================================================
# 1. OUTPUT 1 — Ranking de lnRR (pesos para regras fuzzy)
# ===============================================================
# Dimensões com maiores |lnRR| → maior peso nas regras SE-ENTÃO

ranking <- res_dim %>%
  filter(!is.na(lnRR)) %>%
  arrange(desc(abs(lnRR))) %>%
  mutate(
    Nome      = nomes_dim[Dimensao],
    Rank      = row_number(),
    pct       = round(pct_change, 1),
    # Peso normalizado (proporcional a |lnRR|)
    peso_bruto = abs(lnRR),
    peso_norm  = round(peso_bruto / sum(peso_bruto), 3)
  ) %>%
  select(Rank, Dimensao, Nome, k, lnRR, se, pct, Status, peso_norm)

cat("\n--- OUTPUT 1: Ranking de magnitudes de efeito ---\n")
print(ranking)

# Pesos conservadores para exploratórias (mais perto de 1/6 = 0.167)
ranking <- ranking %>%
  mutate(
    peso_ISB = ifelse(
      Status %in% c("Exploratória", "Síntese narrativa"),
      round((peso_norm + 1/6) / 2, 3),   # média entre peso empírico e equiponderação
      peso_norm
    ),
    peso_ISB = round(peso_ISB / sum(peso_ISB), 3)  # renormalizar
  )

cat("\n--- Pesos finais para ISB (conservadores para exploratórias) ---\n")
print(ranking %>% select(Dimensao, Nome, peso_norm, peso_ISB, Status))

# ===============================================================
# 2. OUTPUT 2 — Mapa de heterogeneidade (largura das pertinências)
# ===============================================================
# I² alta → funções de pertinência mais amplas (maior sobreposição)
# I² baixa → funções mais estreitas e diferenciadas

heterogeneidade <- res_dim %>%
  filter(!is.na(lnRR)) %>%
  mutate(
    Nome = nomes_dim[Dimensao],
    I2_classe = case_when(
      I2 < 25  ~ "Baixa",
      I2 < 75  ~ "Moderada",
      TRUE     ~ "Alta"
    ),
    largura_fuzzy = case_when(
      I2_classe == "Baixa"    ~ "Estreita",
      I2_classe == "Moderada" ~ "Moderada",
      I2_classe == "Alta"     ~ "Ampla"
    )
  ) %>%
  select(Dimensao, Nome, I2, tau2, I2_classe, largura_fuzzy)

cat("\n--- OUTPUT 2: Mapa de heterogeneidade → largura fuzzy ---\n")
print(heterogeneidade)

# ===============================================================
# 3. OUTPUT 3 — Coeficientes de moderadores (ajustes contextuais)
# ===============================================================

if (length(mr) > 0) {
  coefs_mr <- map_dfr(mr, function(res) {
    rob <- as.data.frame(res$robusto) %>%
      rownames_to_column("Moderador") %>%
      filter(Moderador != "intrcpt") %>%
      mutate(
        Dimensao = res$Dimensao,
        R2       = round(res$R2, 3)
      )
  }) %>%
    select(Dimensao, Moderador, beta, SE, p_Satt, R2) %>%
    filter(p_Satt < 0.10)  # moderadores com p < 0.10

  cat("\n--- OUTPUT 3: Moderadores significativos (p < 0.10) ---\n")
  print(coefs_mr)
} else {
  coefs_mr <- tibble()
  cat("\n--- OUTPUT 3: Nenhuma meta-regressão com k >= 10 ---\n")
}

# ===============================================================
# 4. OUTPUT 4 — Universos de discurso (IC 95% → limites fuzzy)
# ===============================================================
# IC inferior → parâmetro inferior do termo linguístico mais baixo
# IC superior → parâmetro superior do termo linguístico mais alto

universos <- res_dim %>%
  filter(!is.na(lnRR)) %>%
  mutate(
    Nome = nomes_dim[Dimensao],
    # Retrotransformar para escala percentual
    ud_inferior_pct = round((exp(ci_lo) - 1) * 100, 1),
    ud_superior_pct = round((exp(ci_hi) - 1) * 100, 1),
    # Para PI (prediction interval) — faixa total esperada
    ud_pi_inf_pct   = round((exp(pi_lo) - 1) * 100, 1),
    ud_pi_sup_pct   = round((exp(pi_hi) - 1) * 100, 1)
  ) %>%
  select(Dimensao, Nome, ci_lo, ci_hi, ud_inferior_pct, ud_superior_pct,
         pi_lo, pi_hi, ud_pi_inf_pct, ud_pi_sup_pct)

cat("\n--- OUTPUT 4: Universos de discurso para fuzzy ---\n")
print(universos)

# ===============================================================
# 5. Tabela-resumo consolidada (Tabela final do manuscrito)
# ===============================================================

tabela_ISB <- ranking %>%
  select(Dimensao, Nome, k, lnRR, pct, Status, peso_ISB) %>%
  left_join(heterogeneidade %>% select(Dimensao, I2, tau2, largura_fuzzy),
            by = "Dimensao") %>%
  left_join(universos %>% select(Dimensao, ud_inferior_pct, ud_superior_pct),
            by = "Dimensao")

cat("\n--- TABELA-RESUMO ISB ---\n")
print(tabela_ISB)

writexl::write_xlsx(tabela_ISB,       file.path(DIR_OUTPUT, "tabela_ISB_consolidada.xlsx"))
writexl::write_xlsx(ranking,          file.path(DIR_OUTPUT, "ranking_lnRR.xlsx"))
writexl::write_xlsx(heterogeneidade,  file.path(DIR_OUTPUT, "mapa_heterogeneidade.xlsx"))
writexl::write_xlsx(universos,        file.path(DIR_OUTPUT, "universos_discurso_fuzzy.xlsx"))

if (nrow(coefs_mr) > 0) {
  writexl::write_xlsx(coefs_mr, file.path(DIR_OUTPUT, "moderadores_significativos.xlsx"))
}

cat("\n✔ Outputs ISB consolidados e exportados.\n")

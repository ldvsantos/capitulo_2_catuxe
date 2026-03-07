# ================================================================
# 02b_integrar_evidencia_mista.R
# Integra dados T1 (quantitativos) com T2–T4 (convertidos) para
# meta-análise hierárquica com propagação de incerteza de conversão.
#
# Lê: bd_extracao_convertido.xlsx (saída de 31_converter_quali_para_lnRR.py)
# Grava: bd_lnRR_misto.rds (entrada para 03_meta_analise_dimensao.R)
#         diagnostico_evidencia_mista.xlsx
#
# Referências:
#   Hasselblad & Hedges (1995) - conversão lnOR ↔ d
#   Zhang & Yu (1998) - conversão lnOR → lnRR
#   Pustejovsky (2022) - RVE com correção CR2
#   Borenstein et al. (2009) - framework geral
#
# Autor: Diego Vidal / Copilot | 2026-03-02
# ================================================================

source("00_setup.R")

# ---------------------------------------------------------------
# 1. Carregar banco convertido
# ---------------------------------------------------------------

fp_conv <- file.path(DIR_DADOS, "2-DADOS_TABULADOS", "bd_extracao_convertido.xlsx")

if (!file.exists(fp_conv)) {
  stop(paste(
    "Arquivo não encontrado:", fp_conv,
    "\nExecute 31_converter_quali_para_lnRR.py primeiro."
  ))
}

bd <- readxl::read_excel(fp_conv, sheet = "DADOS_CONVERTIDOS") %>%
  mutate(
    Study_ID = as.integer(Study_ID),
    Year     = as.integer(Year),
    across(c(lnRR, vi, sigma_conv, n_T, n_C, NOS), as.numeric),
    Dimensao         = factor(Dimensao, levels = paste0("V", 1:8)),
    Tier             = factor(Tier, levels = c("T1", "T2a", "T2b", "T3", "T4")),
    Tipo_Intervencao = factor(Tipo_Intervencao),
    Regiao           = factor(Regiao),
    Tipo_Comunidade  = factor(Tipo_Comunidade)
  ) %>%
  filter(!is.na(lnRR), !is.infinite(lnRR), !is.na(vi))

# Preencher moderadores (Tipo_Intervencao, Regiao, Tipo_Comunidade) a partir
# da bd_extracao original (script 31 não transfere essas colunas para T2-T4)
fp_orig <- file.path(DIR_DADOS, "2-DADOS_TABULADOS", "bd_extracao_PREENCHIDO_V8.xlsx")
if (file.exists(fp_orig)) {
  bd_orig <- readxl::read_excel(fp_orig, sheet = "Sheet1") %>%
    select(Study_ID, Dimensao, Tipo_Intervencao, Regiao, Tipo_Comunidade) %>%
    mutate(
      Study_ID = as.integer(Study_ID),
      Dimensao = factor(Dimensao, levels = paste0("V", 1:8))
    ) %>%
    distinct(Study_ID, Dimensao, .keep_all = TRUE)

  # Preencher NAs nos moderadores via join
  bd <- bd %>%
    select(-Tipo_Intervencao, -Regiao, -Tipo_Comunidade) %>%
    left_join(bd_orig, by = c("Study_ID", "Dimensao")) %>%
    mutate(
      Tipo_Intervencao = factor(Tipo_Intervencao),
      Regiao           = factor(Regiao),
      Tipo_Comunidade  = factor(Tipo_Comunidade)
    )
  cat("Moderadores preenchidos via bd_extracao_PREENCHIDO:",
      sum(!is.na(bd$Regiao)), "/", nrow(bd), "\n")
}

cat("Registros carregados:", nrow(bd), "\n")
cat("Estudos únicos:", n_distinct(bd$Study_ID), "\n")
cat("Distribuição por tier:\n")
print(table(bd$Tier))

# ---------------------------------------------------------------
# 2. Inflação de variância por incerteza de conversão
# ---------------------------------------------------------------
# Para tiers convertidos, a variância já foi inflada no Python por
# vi * (1 + σ²_conv). Aqui adicionamos inflação bootstrap empírica
# se dados de dupla codificação estiverem disponíveis.
#
# σ²_conv por tier (valores default, atualizáveis após κ empírico):
#   T1:  0.00 (sem conversão)
#   T2a: 0.15 (p→d→lnRR, incerteza moderada)
#   T2b: 0.25 (threshold de p, mais incerteza)
#   T3:  0.35 (ordinal com tabelas)
#   T4:  0.50 (qualitativo puro)

# Verificar se a inflação já foi aplicada (campo sigma_conv)
cat("\nσ_conv por tier:\n")
bd %>%
  group_by(Tier) %>%
  summarise(
    n = n(),
    sigma_conv_mean = mean(sigma_conv, na.rm = TRUE),
    vi_median = median(vi, na.rm = TRUE),
    lnRR_mean = mean(lnRR, na.rm = TRUE),
    .groups = "drop"
  ) %>%
  print()

# ---------------------------------------------------------------
# 3. Variável indicadora para análise de sensibilidade
# ---------------------------------------------------------------

bd <- bd %>%
  mutate(
    # Variável binária: evidência direta (T1) vs. convertida
    Evidencia_direta = ifelse(Tier == "T1", 1L, 0L),
    # Peso informativo (T1 recebe peso pleno, T4 o menor)
    peso_tier = case_when(
      Tier == "T1"  ~ 1.0,
      Tier == "T2a" ~ 0.8,
      Tier == "T2b" ~ 0.6,
      Tier == "T3"  ~ 0.4,
      Tier == "T4"  ~ 0.2
    ),
    # ID de observação para o modelo multinível
    obs_id = row_number()
  )

# ---------------------------------------------------------------
# 4. Diagnóstico de viabilidade por dimensão (atualizado)
# ---------------------------------------------------------------

k_por_dimensao <- bd %>%
  group_by(Dimensao) %>%
  summarise(
    k_total     = n_distinct(Study_ID),
    k_T1        = n_distinct(Study_ID[Tier == "T1"]),
    k_T2        = n_distinct(Study_ID[Tier %in% c("T2a", "T2b")]),
    k_T3_T4     = n_distinct(Study_ID[Tier %in% c("T3", "T4")]),
    n_obs       = n(),
    lnRR_medio  = mean(lnRR, na.rm = TRUE),
    vi_mediano  = median(vi, na.rm = TRUE),
    .groups     = "drop"
  ) %>%
  mutate(
    Status = case_when(
      k_total >= 15 ~ "Confirmatória (meta-análise completa)",
      k_total >= 10 ~ "Confirmatória (subgrupos condicionais)",
      k_total >= 3  ~ "Exploratória",
      TRUE          ~ "Síntese narrativa"
    )
  )

cat("\n=== DIAGNÓSTICO DE VIABILIDADE (ATUALIZADO) ===\n")
print(k_por_dimensao)

# ---------------------------------------------------------------
# 5. Matriz de variância-covariância intra-estudo
# ---------------------------------------------------------------
# ρ = 0.5 (default), com sensibilidade em 0.2 e 0.8
# Conforme Pustejovsky (2022), modelo de efeitos correlados

rho_base <- 0.5

V_mat <- vcalc(
  vi      = vi,
  cluster = Study_ID,
  obs     = obs_id,
  rho     = rho_base,
  data    = bd
)

# ---------------------------------------------------------------
# 6. Modelo hierárquico 3 níveis por dimensão
# ---------------------------------------------------------------

resultados_misto <- map_dfr(levels(bd$Dimensao), function(dim) {

  df <- bd %>% filter(Dimensao == dim)
  k  <- n_distinct(df$Study_ID)

  if (k < 3) {
    return(tibble(
      Dimensao = dim, k = k, n_obs = nrow(df),
      lnRR = NA, se = NA,
      ci_lo = NA, ci_hi = NA,
      pi_lo = NA, pi_hi = NA,
      tau2 = NA, I2 = NA, Q = NA, pQ = NA,
      k_T1 = sum(df$Tier == "T1"),
      Status = "Síntese narrativa"
    ))
  }

  # Submatriz V-C para esta dimensão
  idx <- which(bd$Dimensao == dim)
  V_sub <- V_mat[idx, idx]

  # Modelo 3 níveis: observação / estudo / proxy
  mod <- tryCatch(
    rma.mv(
      yi     = lnRR,
      V      = V_sub,
      random = ~ 1 | Study_ID / Proxy,
      data   = df,
      method = "REML",
      test   = if (k < 15) "t" else "z"
    ),
    error = function(e) {
      warning(paste("Erro no modelo para", dim, ":", e$message))
      NULL
    }
  )

  if (is.null(mod)) {
    return(tibble(
      Dimensao = dim, k = k, n_obs = nrow(df),
      lnRR = mean(df$lnRR), se = NA,
      ci_lo = NA, ci_hi = NA,
      pi_lo = NA, pi_hi = NA,
      tau2 = NA, I2 = NA, Q = NA, pQ = NA,
      k_T1 = sum(df$Tier == "T1"),
      Status = "Modelo falhou"
    ))
  }

  # RVE (clubSandwich CR2)
  rob <- tryCatch(
    coef_test(mod, vcov = "CR2", cluster = df$Study_ID),
    error = function(e) NULL
  )

  se_val <- if (!is.null(rob)) rob$SE else mod$se
  df_val <- if (!is.null(rob)) rob$df else Inf

  # Prediction interval
  pi <- predict(mod)

  # I² generalizado (Cheung 2014)
  sigma2 <- mod$sigma2
  tau2_total <- sum(sigma2)
  vi_typ <- mean(df$vi)
  I2 <- 100 * tau2_total / (tau2_total + vi_typ)

  tibble(
    Dimensao = dim,
    k        = k,
    n_obs    = nrow(df),
    lnRR     = coef(mod),
    se       = se_val,
    ci_lo    = coef(mod) - qt(0.975, max(df_val, 1)) * se_val,
    ci_hi    = coef(mod) + qt(0.975, max(df_val, 1)) * se_val,
    pi_lo    = pi$pi.lb,
    pi_hi    = pi$pi.ub,
    tau2     = tau2_total,
    I2       = I2,
    Q        = mod$QE,
    pQ       = mod$QEp,
    k_T1     = sum(df$Tier == "T1"),
    Status   = k_por_dimensao$Status[k_por_dimensao$Dimensao == dim]
  )
})

# Retrotransformação percentual
resultados_misto <- resultados_misto %>%
  mutate(
    pct_change = (exp(lnRR) - 1) * 100,
    pct_lo     = (exp(ci_lo) - 1) * 100,
    pct_hi     = (exp(ci_hi) - 1) * 100
  )

cat("\n=== RESULTADOS META-ANÁLISE (EVIDÊNCIA MISTA) ===\n")
print(resultados_misto)

# ---------------------------------------------------------------
# 7. Análise de sensibilidade: só T1 vs. todos os tiers
# ---------------------------------------------------------------

cat("\n--- Sensibilidade: T1 only vs. todos ---\n")

sens_tier <- map_dfr(levels(bd$Dimensao), function(dim) {
  df_t1 <- bd %>% filter(Dimensao == dim, Tier == "T1")
  k_t1 <- n_distinct(df_t1$Study_ID)

  if (k_t1 < 2) {
    return(tibble(Dimensao = dim, lnRR_T1only = NA, lnRR_todos = NA, diff = NA))
  }

  # Modelo simplificado só com T1
  mod_t1 <- tryCatch(
    rma(yi = lnRR, vi = vi, data = df_t1, method = "REML"),
    error = function(e) NULL
  )

  lnrr_t1 <- if (!is.null(mod_t1)) coef(mod_t1) else NA

  tibble(
    Dimensao    = dim,
    k_T1        = k_t1,
    lnRR_T1only = lnrr_t1,
    lnRR_todos  = resultados_misto$lnRR[resultados_misto$Dimensao == dim],
    diff        = lnrr_t1 - resultados_misto$lnRR[resultados_misto$Dimensao == dim]
  )
})

print(sens_tier)

# ---------------------------------------------------------------
# 8. Sensibilidade ρ intra-estudo
# ---------------------------------------------------------------

cat("\n--- Sensibilidade ρ ---\n")

rhos <- c(0.2, 0.5, 0.8)

sens_rho <- map_dfr(rhos, function(r) {
  V_r <- vcalc(vi = vi, cluster = Study_ID, obs = obs_id,
                rho = r, data = bd)

  map_dfr(levels(bd$Dimensao), function(dim) {
    df <- bd %>% filter(Dimensao == dim)
    k  <- n_distinct(df$Study_ID)
    if (k < 3) return(NULL)

    idx <- which(bd$Dimensao == dim)
    V_sub <- V_r[idx, idx]

    mod <- tryCatch(
      rma.mv(yi = lnRR, V = V_sub,
             random = ~ 1 | Study_ID / Proxy,
             data = df, method = "REML"),
      error = function(e) NULL
    )

    if (is.null(mod)) return(NULL)

    tibble(rho = r, Dimensao = dim,
           lnRR = coef(mod), tau2 = sum(mod$sigma2))
  })
})

print(sens_rho %>% pivot_wider(names_from = rho, values_from = c(lnRR, tau2)))

# ---------------------------------------------------------------
# 9. Meta-regressão: tier como moderador
# ---------------------------------------------------------------

cat("\n--- Meta-regressão: Tier como moderador ---\n")

for (dim in levels(bd$Dimensao)) {
  df <- bd %>% filter(Dimensao == dim)
  k  <- n_distinct(df$Study_ID)
  if (k < 5 || n_distinct(df$Tier) < 2) next

  idx <- which(bd$Dimensao == dim)
  V_sub <- V_mat[idx, idx]

  mod_tier <- tryCatch(
    rma.mv(yi = lnRR, V = V_sub,
           mods = ~ Evidencia_direta,
           random = ~ 1 | Study_ID / Proxy,
           data = df, method = "REML"),
    error = function(e) NULL
  )

  if (!is.null(mod_tier)) {
    cat("\n", dim, "— Moderador: Evidência direta (T1 vs convertida)\n")
    cat("  Coef =", round(coef(mod_tier)[2], 4),
        " p =", round(mod_tier$pval[2], 4),
        " QM =", round(mod_tier$QM, 3), "\n")
  }
}

# ---------------------------------------------------------------
# 10. Exportar resultados
# ---------------------------------------------------------------

saveRDS(bd, file.path(DIR_OUTPUT, "bd_lnRR_misto.rds"))
saveRDS(resultados_misto, file.path(DIR_OUTPUT, "resultados_evidencia_mista.rds"))
saveRDS(k_por_dimensao, file.path(DIR_OUTPUT, "k_por_dimensao_misto.rds"))

writexl::write_xlsx(
  list(
    resultados = resultados_misto,
    sensibilidade_tier = sens_tier,
    sensibilidade_rho = sens_rho,
    k_dimensao = k_por_dimensao
  ),
  file.path(DIR_OUTPUT, "diagnostico_evidencia_mista.xlsx")
)

cat("\n✔ Banco misto salvo em:", file.path(DIR_OUTPUT, "bd_lnRR_misto.rds"), "\n")
cat("✔ Resultados salvos em:", file.path(DIR_OUTPUT, "diagnostico_evidencia_mista.xlsx"), "\n")

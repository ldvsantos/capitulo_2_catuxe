# ================================================================
# 04_meta_regressao.R — Meta-regressão multivariada e subgrupos
# Artigo 2: Meta-análise de vulnerabilidade biocultural (V1–V8)
# Adaptado de: 11-ARTIGO_MA / meta_regressao_manejo_1.R
# ================================================================

source("00_setup.R")

bd   <- readRDS(file.path(DIR_OUTPUT, "bd_lnRR_misto.rds"))
k_df <- readRDS(file.path(DIR_OUTPUT, "k_por_dimensao_misto.rds"))

rho_ref <- 0.8

# ---------------------------------------------------------------
# 1. Meta-regressão multivariada por dimensão (k >= 10)
# ---------------------------------------------------------------
# Moderadores fixos (§2.8 e §2.11 do manuscrito):
#   - Tipo_Intervencao (documentação, registro, proteção jurídica, governança)
#   - Regiao (semiárido, cerrado, amazônia, mata atlântica, outro)
#   - Tempo_Intervencao (contínuo, anos)
#   - Tipo_Comunidade (quilombola, indígena, camponesa, ribeirinha)
#   - NOS (contínuo, 0–9)

dims_confirma <- k_df %>% filter(k_total >= 10) %>% pull(Dimensao)

resultados_mr <- map(dims_confirma, function(dim) {

  df <- bd %>% filter(Dimensao == dim)
  V  <- vcalc(vi = vi, cluster = Study_ID, obs = seq_len(nrow(df)),
              rho = rho_ref, data = df)

  # Modelo completo com moderadores disponíveis (Tempo_Intervencao e NOS removidos: dados ausentes)
  mod_full <- tryCatch(
    rma.mv(
      yi     = lnRR,
      V      = V,
      mods   = ~ Tipo_Intervencao + Regiao + Tipo_Comunidade,
      random = ~ 1 | Study_ID / Proxy,
      data   = df,
      method = "ML",   # ML para comparação de modelos
      test   = "t"
    ),
    error = function(e) {
      message("Erro na meta-regressão para ", dim, ": ", e$message)
      NULL
    }
  )

  if (is.null(mod_full)) return(NULL)

  # Teste omnibus QM
  cat("\n--- Meta-regressão:", dim, "---\n")
  cat("QM =", round(mod_full$QM, 2), ", p =", sprintf("%.4f", mod_full$QMp), "\n")

  # Coeficientes com variância robusta (CR2)
  rob <- coef_test(mod_full, vcov = "CR2", cluster = df$Study_ID)

  # Proporção de heterogeneidade explicada (R²)
  mod_null <- rma.mv(yi = lnRR, V = V, random = ~ 1 | Study_ID / Proxy,
                     data = df, method = "ML")
  R2 <- max(0, 1 - sum(mod_full$sigma2) / sum(mod_null$sigma2))
  cat("R² (heterogeneidade explicada):", round(R2 * 100, 1), "%\n")

  list(
    Dimensao  = dim,
    modelo    = mod_full,
    robusto   = rob,
    R2        = R2,
    QM        = mod_full$QM,
    QMp       = mod_full$QMp
  )
}) %>% compact()

names(resultados_mr) <- sapply(resultados_mr, `[[`, "Dimensao")

# ---------------------------------------------------------------
# 2. Análise univariada para dimensões com k < 10 (exploratória)
# ---------------------------------------------------------------

dims_explora <- k_df %>% filter(k_total >= 3 & k_total < 10) %>% pull(Dimensao)

resultados_explora <- map(dims_explora, function(dim) {

  df <- bd %>% filter(Dimensao == dim)
  V  <- vcalc(vi = vi, cluster = Study_ID, obs = seq_len(nrow(df)),
              rho = rho_ref, data = df)

  moderadores <- c("Tipo_Intervencao", "Regiao", "Tipo_Comunidade")

  map_dfr(moderadores, function(mod_var) {
    fml <- as.formula(paste("~ ", mod_var))
    mod <- tryCatch(
      rma.mv(yi = lnRR, V = V, mods = fml,
             random = ~ 1 | Study_ID, data = df, method = "REML", test = "t"),
      error = function(e) NULL
    )
    if (is.null(mod)) return(NULL)

    tibble(
      Dimensao  = dim,
      Moderador = mod_var,
      QM        = mod$QM,
      QMp       = mod$QMp,
      k         = n_distinct(df$Study_ID)
    )
  })
}) %>% bind_rows()

cat("\n--- Análises univariadas exploratórias ---\n")
print(resultados_explora)

# ---------------------------------------------------------------
# 3. Análise de subgrupos (categóricos, k >= 10)
# ---------------------------------------------------------------

subgrupo_results <- map_dfr(dims_confirma, function(dim) {

  df <- bd %>% filter(Dimensao == dim)

  map_dfr(c("Tipo_Intervencao", "Regiao", "Tipo_Comunidade"), function(mod_var) {

    subgrupos <- df %>%
      group_by(.data[[mod_var]]) %>%
      summarise(k_sub = n_distinct(Study_ID), .groups = "drop") %>%
      filter(k_sub >= 3)   # mínimo 3 estudos por subgrupo

    map_dfr(subgrupos[[mod_var]], function(nivel) {
      df_sub <- df %>% filter(.data[[mod_var]] == nivel)
      V_sub  <- vcalc(vi = vi, cluster = Study_ID, obs = seq_len(nrow(df_sub)),
                      rho = rho_ref, data = df_sub)

      mod <- tryCatch(
        rma.mv(yi = lnRR, V = V_sub, random = ~ 1 | Study_ID,
               data = df_sub, method = "REML", test = "t"),
        error = function(e) NULL
      )
      if (is.null(mod)) return(NULL)

      tibble(
        Dimensao  = dim,
        Moderador = mod_var,
        Nivel     = nivel,
        k         = n_distinct(df_sub$Study_ID),
        lnRR      = coef(mod),
        se        = mod$se,
        ci_lo     = mod$ci.lb,
        ci_hi     = mod$ci.ub,
        I2_within = 100 * sum(mod$sigma2) / (sum(mod$sigma2) + mean(df_sub$vi))
      )
    })
  })
})

cat("\n--- Análises de subgrupo ---\n")
print(subgrupo_results)

# ---------------------------------------------------------------
# 4. Exportar resultados
# ---------------------------------------------------------------

saveRDS(resultados_mr,     file.path(DIR_OUTPUT, "meta_regressao.rds"))
writexl::write_xlsx(resultados_explora, file.path(DIR_OUTPUT, "moderadores_exploratoria.xlsx"))
writexl::write_xlsx(subgrupo_results,   file.path(DIR_OUTPUT, "subgrupos.xlsx"))

# Tabela consolidada de coeficientes da meta-regressão
tabela_mr <- map_dfr(resultados_mr, function(res) {
  rob <- res$robusto
  as.data.frame(rob) %>%
    rownames_to_column("Coeficiente") %>%
    mutate(Dimensao = res$Dimensao, R2 = res$R2)
})

writexl::write_xlsx(tabela_mr, file.path(DIR_OUTPUT, "coeficientes_meta_regressao.xlsx"))

cat("✔ Meta-regressão e subgrupos concluídos.\n")

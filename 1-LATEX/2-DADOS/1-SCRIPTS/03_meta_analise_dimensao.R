# ================================================================
# 03_meta_analise_dimensao.R — Meta-análise hierárquica por V1–V6
# Artigo 2: Meta-análise de vulnerabilidade biocultural
# Adaptado de: 11-ARTIGO_MA / efeito_aleatorio_fisicas.R,
#              efeito_aleatorio_biologicas.R, efeito_aleatorio_quimico.R
# ================================================================

source("00_setup.R")

bd   <- readRDS(file.path(DIR_OUTPUT, "bd_lnRR_misto.rds"))
k_df <- readRDS(file.path(DIR_OUTPUT, "k_por_dimensao_misto.rds"))

# ---------------------------------------------------------------
# 1. Modelo hierárquico 3 níveis por dimensão (REML)
# ---------------------------------------------------------------
# Equação §2.11 (Eq. 3):
#   lnRR_ij = μ + β·X_ij + u_j + ε_ij
#   u_j ~ N(0, τ²), ε_ij ~ N(0, v_i)

# Matriz V-C intra-estudo: ρ = 0.8 (sensibilidade em 0.5–1.0)
rho_ref <- 0.8

resultados_dim <- map_dfr(levels(bd$Dimensao), function(dim) {

  df <- bd %>% filter(Dimensao == dim)
  k  <- n_distinct(df$Study_ID)

  if (k < 3) {
    return(tibble(
      Dimensao = dim, k = k, lnRR = NA, se = NA,
      ci_lo = NA, ci_hi = NA, pi_lo = NA, pi_hi = NA,
      tau2 = NA, I2 = NA, Q = NA, pQ = NA,
      Status = "Síntese narrativa"
    ))
  }

  # Construir V-C matrix com ρ constante
  V <- metafor::vcalc(vi = vi, cluster = Study_ID,
                      obs = seq_len(nrow(df)),
                      rho = rho_ref, data = df)

  # Modelo 3 níveis
  mod <- rma.mv(
    yi     = lnRR,
    V      = V,
    random = ~ 1 | Study_ID / Proxy,
    data   = df,
    method = "REML",
    test   = if (k < 15) "t" else "z"   # HKSJ para k < 15
  )

  # RVE (clubSandwich CR2)
  rob <- coef_test(mod, vcov = "CR2", cluster = df$Study_ID)

  # Prediction interval (IntHout et al. 2016)
  pi <- predict(mod)

  # I² generalizado (Cheung 2014)
  sigma2 <- mod$sigma2
  tau2_total <- sum(sigma2)
  vi_typ <- mean(df$vi)
  I2 <- 100 * tau2_total / (tau2_total + vi_typ)

  tibble(
    Dimensao = dim,
    k        = k,
    lnRR     = coef(mod),
    se       = rob$SE,
    ci_lo    = rob$beta - qt(0.975, rob$df) * rob$SE,
    ci_hi    = rob$beta + qt(0.975, rob$df) * rob$SE,
    pi_lo    = pi$pi.lb,
    pi_hi    = pi$pi.ub,
    tau2     = tau2_total,
    I2       = I2,
    Q        = mod$QE,
    pQ       = mod$QEp,
    Status   = k_df$Status[k_df$Dimensao == dim]
  )
})

# Retrotransformação percentual: (exp(lnRR) − 1) × 100
resultados_dim <- resultados_dim %>%
  mutate(
    pct_change = (exp(lnRR) - 1) * 100,
    pct_lo     = (exp(ci_lo) - 1) * 100,
    pct_hi     = (exp(ci_hi) - 1) * 100
  )

print(resultados_dim)

# ---------------------------------------------------------------
# 2. Sensibilidade τ² estimator: DL vs REML
# ---------------------------------------------------------------

sens_dl <- map_dfr(levels(bd$Dimensao), function(dim) {
  df <- bd %>% filter(Dimensao == dim)
  k  <- n_distinct(df$Study_ID)
  if (k < 3) return(NULL)

  # Usar modelo univariado agregado para DL (rma.mv não suporta DL)
  agg <- df %>%
    group_by(Study_ID) %>%
    summarise(lnRR = mean(lnRR), vi = mean(vi), .groups = "drop")

  mod_dl <- rma(yi = lnRR, vi = vi, data = agg, method = "DL")

  tibble(Dimensao = dim, tau2_DL = mod_dl$tau2, lnRR_DL = coef(mod_dl))
})

# Comparar com REML
sens_compare <- resultados_dim %>%
  select(Dimensao, tau2_REML = tau2, lnRR_REML = lnRR) %>%
  left_join(sens_dl, by = "Dimensao") %>%
  mutate(
    diff_tau2 = tau2_DL - tau2_REML,
    diff_lnRR = lnRR_DL - lnRR_REML
  )

cat("\n--- Sensibilidade DL vs REML ---\n")
print(sens_compare)

# ---------------------------------------------------------------
# 3. Sensibilidade ρ intra-estudo: 0.5, 0.6, 0.7, 0.8, 0.9, 1.0
# ---------------------------------------------------------------

rhos <- c(0.5, 0.6, 0.7, 0.8, 0.9, 1.0)

sens_rho <- map_dfr(rhos, function(r) {
  map_dfr(levels(bd$Dimensao), function(dim) {
    df <- bd %>% filter(Dimensao == dim)
    k  <- n_distinct(df$Study_ID)
    if (k < 3) return(NULL)

    V <- vcalc(vi = vi, cluster = Study_ID, obs = seq_len(nrow(df)),
               rho = r, data = df)
    mod <- rma.mv(yi = lnRR, V = V, random = ~ 1 | Study_ID / Proxy,
                  data = df, method = "REML")

    tibble(rho = r, Dimensao = dim, lnRR = coef(mod), tau2 = sum(mod$sigma2))
  })
})

cat("\n--- Sensibilidade ρ ---\n")
print(sens_rho %>% pivot_wider(names_from = rho, values_from = c(lnRR, tau2)))

# ---------------------------------------------------------------
# 4. Exportar resultados
# ---------------------------------------------------------------

saveRDS(resultados_dim, file.path(DIR_OUTPUT, "resultados_por_dimensao.rds"))
writexl::write_xlsx(resultados_dim, file.path(DIR_OUTPUT, "resultados_por_dimensao.xlsx"))
writexl::write_xlsx(sens_compare,   file.path(DIR_OUTPUT, "sensibilidade_DL_REML.xlsx"))
writexl::write_xlsx(sens_rho,       file.path(DIR_OUTPUT, "sensibilidade_rho.xlsx"))

cat("✔ Meta-análise por dimensão concluída.\n")

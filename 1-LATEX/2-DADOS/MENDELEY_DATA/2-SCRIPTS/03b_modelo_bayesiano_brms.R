# ================================================================
# 03b_modelo_bayesiano_brms.R
# Modelo bayesiano hierárquico para integração de evidência mista:
#   - lnRR quantitativos → gaussiano com variância conhecida
#   - Julgamentos ordinais → ordinal cumulativo com mesmo θ latente
#
# Implementa robustness check para o modelo frequencista (03_meta_analise).
# Publicações com dados quantitativos informam a posterior de θ_dimensão
# com precisão proporcional a 1/vi, enquanto julgamentos qualitativos
# contribuem como prior empírico via likelihood ordinal.
#
# Referências:
#   Bürkner (2017) https://doi.org/10.18637/jss.v080.i01
#   Röver (2020) - bayesian meta-analysis
#   Hasselblad & Hedges (1995) - scale mixing
#
# Requer: brms, cmdstanr (ou rstan), tidybayes
# Autor: Diego Vidal / Copilot | 2026-03-02
# ================================================================

source("00_setup.R")

# Pacotes adicionais
if (!requireNamespace("brms", quietly = TRUE)) install.packages("brms")
if (!requireNamespace("tidybayes", quietly = TRUE)) install.packages("tidybayes")
library(brms)
library(tidybayes)

# ---------------------------------------------------------------
# 1. Carregar e preparar dados
# ---------------------------------------------------------------

bd <- readRDS(file.path(DIR_OUTPUT, "bd_lnRR_misto.rds"))

cat("Registros totais:", nrow(bd), "\n")
cat("Por tier:\n")
print(table(bd$Tier, bd$Dimensao))

# ---------------------------------------------------------------
# 2. Preparar dois subconjuntos
# ---------------------------------------------------------------

# Subconjunto A: quantitativos (T1, T2a com lnRR contínuo)
# Estes entram como gaussian com se conhecido
bd_quant <- bd %>%
  filter(Tier %in% c("T1", "T2a", "T2b")) %>%
  mutate(
    se = sqrt(vi),
    obs_id = row_number()
  )

cat("\nSubconjunto quantitativo:", nrow(bd_quant), "obs\n")

# Subconjunto B: ordinais (T3, T4)
# Estes entram como variável ordinal (1 = vulnerabilidade reduzida,
# 2 = neutro, 3 = vulnerabilidade agravada)
bd_ord <- bd %>%
  filter(Tier %in% c("T3", "T4")) %>%
  mutate(
    # Recodificar lnRR convertido em categoria ordinal
    # lnRR < -0.2 → -1 (redução), -0.2 a 0.2 → 0 (neutro), > 0.2 → +1 (agravamento)
    y_ordinal = case_when(
      lnRR < -0.2  ~ 1L,   # vulnerabilidade reduzida
      lnRR <= 0.2  ~ 2L,   # neutro
      TRUE         ~ 3L    # vulnerabilidade agravada
    ),
    y_ordinal = ordered(y_ordinal),
    obs_id = row_number()
  )

cat("Subconjunto ordinal:", nrow(bd_ord), "obs\n")
cat("Distribuição ordinal:\n")
print(table(bd_ord$y_ordinal, bd_ord$Dimensao))

# ---------------------------------------------------------------
# 3. Modelo A: Meta-análise bayesiana para dados quantitativos
# ---------------------------------------------------------------
# lnRR_i | θ_dim, τ ~ N(θ_dim + u_study, se_i²)
# u_study ~ N(0, τ²)
# θ_dim ~ N(0, 1)  prior fracamente informativo
# τ ~ half-Cauchy(0, 0.5)

cat("\n=== Ajustando modelo bayesiano (dados quantitativos) ===\n")

# Prior para τ: half-Cauchy recomendado por Röver (2020)
priors_quant <- c(
  prior(normal(0, 1), class = "Intercept"),
  prior(cauchy(0, 0.5), class = "sd")
)

if (nrow(bd_quant) >= 5) {

  mod_bayes_quant <- brm(
    lnRR | se(se) ~ 0 + Dimensao + (1 | Study_ID),
    data    = bd_quant,
    family  = gaussian(),
    prior   = priors_quant,
    iter    = 4000,
    warmup  = 1000,
    chains  = 4,
    cores   = 4,
    seed    = 2024,
    control = list(adapt_delta = 0.95),
    file    = file.path(DIR_OUTPUT, "mod_bayes_quant")
  )

  cat("\n--- Sumário modelo quantitativo bayesiano ---\n")
  print(summary(mod_bayes_quant))

  # Extrair θ por dimensão
  theta_quant <- mod_bayes_quant %>%
    spread_draws(b_DimensaoV1, b_DimensaoV2, b_DimensaoV3,
                 b_DimensaoV4, b_DimensaoV5, b_DimensaoV6) %>%
    pivot_longer(starts_with("b_Dimensao"),
                 names_to = "Dimensao",
                 values_to = "theta") %>%
    mutate(Dimensao = gsub("b_Dimensao", "", Dimensao)) %>%
    group_by(Dimensao) %>%
    summarise(
      theta_mean = mean(theta),
      theta_sd   = sd(theta),
      ci_lo      = quantile(theta, 0.025),
      ci_hi      = quantile(theta, 0.975),
      P_pos      = mean(theta > 0),
      .groups    = "drop"
    )

  cat("\n--- Estimativas θ por dimensão (quantitativo bayesiano) ---\n")
  print(theta_quant)

} else {
  cat("AVISO: Poucos dados quantitativos para modelo bayesiano.\n")
  mod_bayes_quant <- NULL
  theta_quant <- NULL
}

# ---------------------------------------------------------------
# 4. Modelo B: Ordinal bayesiano para dados qualitativos
# ---------------------------------------------------------------
# y_ordinal ~ cumulative(logit)
# η_i = θ_dim + u_study
# Mesma família de θ_dim para coerência com modelo A

cat("\n=== Ajustando modelo bayesiano (dados ordinais) ===\n")

priors_ord <- c(
  prior(normal(0, 1), class = "b"),
  prior(cauchy(0, 0.5), class = "sd")
)

if (nrow(bd_ord) >= 10) {

  mod_bayes_ord <- brm(
    y_ordinal ~ 0 + Dimensao + (1 | Study_ID),
    data    = bd_ord,
    family  = cumulative("logit"),
    prior   = priors_ord,
    iter    = 4000,
    warmup  = 1000,
    chains  = 4,
    cores   = 4,
    seed    = 2024,
    control = list(adapt_delta = 0.95),
    file    = file.path(DIR_OUTPUT, "mod_bayes_ordinal")
  )

  cat("\n--- Sumário modelo ordinal bayesiano ---\n")
  print(summary(mod_bayes_ord))

  # Extrair θ latente por dimensão (escala logit)
  theta_ord <- fixef(mod_bayes_ord) %>%
    as.data.frame() %>%
    tibble::rownames_to_column("param") %>%
    filter(grepl("Dimensao", param)) %>%
    mutate(
      Dimensao = gsub("Dimensao", "", param),
      # Converter de escala logit para escala lnRR aproximada
      # lnRR ≈ lnOR * (1-p0) com p0 = 0.5 → lnRR ≈ Estimate * 0.5
      theta_lnRR_approx = Estimate * sqrt(3) / pi  # d ≈ lnOR * √3/π
    )

  cat("\n--- Estimativas θ ordinais (escala logit → d) ---\n")
  print(theta_ord)

} else {
  cat("AVISO: Poucos dados ordinais para modelo bayesiano.\n")
  mod_bayes_ord <- NULL
  theta_ord <- NULL
}

# ---------------------------------------------------------------
# 5. Modelo C: Integrado (evidência mista como prior)
# ---------------------------------------------------------------
# Se ambos os modelos convergiram, combinar as posteriors:
# θ_combinado = (θ_quant/σ²_quant + θ_ord_convertido/σ²_ord) /
#               (1/σ²_quant + 1/σ²_ord)

cat("\n=== Combinação de posteriors ===\n")

if (!is.null(theta_quant) && !is.null(theta_ord)) {

  combinado <- theta_quant %>%
    rename(theta_Q = theta_mean, sd_Q = theta_sd) %>%
    left_join(
      theta_ord %>%
        select(Dimensao, theta_O = theta_lnRR_approx) %>%
        mutate(sd_O = 0.5),  # prior vago para conversão
      by = "Dimensao"
    ) %>%
    mutate(
      # Combinação bayesiana simples (normal conjugada)
      prec_Q = 1 / sd_Q^2,
      prec_O = 1 / sd_O^2,
      theta_comb = (theta_Q * prec_Q + theta_O * prec_O) / (prec_Q + prec_O),
      sd_comb    = sqrt(1 / (prec_Q + prec_O)),
      ci_lo_comb = theta_comb - 1.96 * sd_comb,
      ci_hi_comb = theta_comb + 1.96 * sd_comb,
      pct_change = (exp(theta_comb) - 1) * 100,
      # Diferença entre estimativas
      diff_Q_O   = theta_Q - theta_O
    )

  cat("\n--- Estimativas combinadas (quantitativo + ordinal) ---\n")
  print(combinado %>%
          select(Dimensao, theta_Q, theta_O, theta_comb, sd_comb,
                 ci_lo_comb, ci_hi_comb, pct_change, diff_Q_O))

  # Salvar
  saveRDS(combinado, file.path(DIR_OUTPUT, "theta_bayesiano_combinado.rds"))
  writexl::write_xlsx(combinado,
                      file.path(DIR_OUTPUT, "theta_bayesiano_combinado.xlsx"))

} else {
  cat("Combinação não possível — um ou ambos modelos não convergiram.\n")
}

# ---------------------------------------------------------------
# 6. Diagnóstico de convergência
# ---------------------------------------------------------------

if (!is.null(mod_bayes_quant)) {
  cat("\n--- Diagnóstico modelo quantitativo ---\n")
  cat("Rhat max:", max(rhat(mod_bayes_quant), na.rm = TRUE), "\n")
  cat("ESS min (bulk):", min(neff_ratio(mod_bayes_quant) * 12000, na.rm = TRUE), "\n")

  # Salvar trace plots
  pdf(file.path(DIR_OUTPUT, "trace_bayes_quant.pdf"), width = 10, height = 8)
  plot(mod_bayes_quant)
  dev.off()
}

if (!is.null(mod_bayes_ord)) {
  cat("\n--- Diagnóstico modelo ordinal ---\n")
  cat("Rhat max:", max(rhat(mod_bayes_ord), na.rm = TRUE), "\n")

  pdf(file.path(DIR_OUTPUT, "trace_bayes_ordinal.pdf"), width = 10, height = 8)
  plot(mod_bayes_ord)
  dev.off()
}

# ---------------------------------------------------------------
# 7. Comparação frequencista vs. bayesiano
# ---------------------------------------------------------------

cat("\n=== Comparação frequencista vs. bayesiano ===\n")

res_freq <- tryCatch(
  readRDS(file.path(DIR_OUTPUT, "resultados_evidencia_mista.rds")),
  error = function(e) NULL
)

if (!is.null(res_freq) && !is.null(theta_quant)) {
  comp <- res_freq %>%
    select(Dimensao, lnRR_freq = lnRR, se_freq = se) %>%
    left_join(
      theta_quant %>% select(Dimensao, lnRR_bayes = theta_mean, se_bayes = theta_sd),
      by = "Dimensao"
    ) %>%
    mutate(
      diff = lnRR_freq - lnRR_bayes,
      concordancia = abs(diff) < 0.1
    )

  cat("\n")
  print(comp)
  cat("\nConcordância (|diff| < 0.1):",
      sum(comp$concordancia, na.rm = TRUE), "/",
      sum(!is.na(comp$concordancia)), "\n")

  writexl::write_xlsx(comp,
                      file.path(DIR_OUTPUT, "comparacao_freq_bayes.xlsx"))
}

cat("\n✔ Análise bayesiana concluída.\n")

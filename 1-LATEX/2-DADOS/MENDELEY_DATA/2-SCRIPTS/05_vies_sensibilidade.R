# ================================================================
# 05_vies_sensibilidade.R — Viés de publicação e análise de
#                            sensibilidade (leave-one-out, NOS,
#                            trim-and-fill)
# Artigo 2: Meta-análise de vulnerabilidade biocultural (V1–V6)
# Adaptado de: 11-ARTIGO_MA / efeito_aleatorio_estudos.R
# ================================================================

source("00_setup.R")

bd       <- readRDS(file.path(DIR_OUTPUT, "bd_lnRR_misto.rds"))
res_dim  <- readRDS(file.path(DIR_OUTPUT, "resultados_por_dimensao.rds"))

rho_ref <- 0.8

# ---------------------------------------------------------------
# 1. Funnel plots + testes de Egger e Begg por dimensão
# ---------------------------------------------------------------

vies_results <- map_dfr(levels(bd$Dimensao), function(dim) {

  df <- bd %>% filter(Dimensao == dim)
  k  <- n_distinct(df$Study_ID)
  if (k < 3) return(NULL)

  V <- vcalc(vi = vi, cluster = Study_ID, obs = seq_len(nrow(df)),
             rho = rho_ref, data = df)

  mod <- rma.mv(yi = lnRR, V = V, random = ~ 1 | Study_ID / Proxy,
                data = df, method = "REML")

  # Funnel plot
  pdf(file.path(DIR_OUTPUT, paste0("funnel_", dim, ".pdf")), width = 7, height = 5)
  funnel(mod, main = paste("Funnel plot —", dim),
         xlab = "lnRR", ylab = "Erro padrão",
         back = "white", shade = "gray90")
  dev.off()

  # Teste de Egger (regressão do SE sobre o efeito)
  egger <- tryCatch({
    regtest(mod, model = "lm")
  }, error = function(e) NULL)

  # Teste de Begg (correlação de ranks)
  begg <- tryCatch({
    ranktest(mod)
  }, error = function(e) NULL)

  tibble(
    Dimensao      = dim,
    k             = k,
    Egger_z       = if (!is.null(egger)) egger$zval else NA,
    Egger_p       = if (!is.null(egger)) egger$pval else NA,
    Begg_tau      = if (!is.null(begg))  begg$tau   else NA,
    Begg_p        = if (!is.null(begg))  begg$pval  else NA,
    Advertencia   = ifelse(k < 10, "Baixo poder (k < 10)", "OK")
  )
})

cat("\n--- Viés de publicação ---\n")
print(vies_results)

# ---------------------------------------------------------------
# 2. Trim-and-fill (Duval & Tweedie)
# ---------------------------------------------------------------

trimfill_results <- map_dfr(levels(bd$Dimensao), function(dim) {

  df <- bd %>% filter(Dimensao == dim)
  k  <- n_distinct(df$Study_ID)
  if (k < 5) return(NULL)   # trim-and-fill precisa de k razoável

  # Modelo univariado agregado para trim-and-fill
  # (rma.mv não suporta trimfill diretamente)
  agg <- df %>%
    group_by(Study_ID) %>%
    summarise(lnRR = mean(lnRR), vi = mean(vi), .groups = "drop")

  mod_uni <- rma(yi = lnRR, vi = vi, data = agg, method = "REML")

  tf <- tryCatch(trimfill(mod_uni), error = function(e) {
    message("Trimfill falhou para ", dim, ": ", e$message)
    NULL
  })

  if (is.null(tf)) return(NULL)

  tibble(
    Dimensao       = dim,
    k_original     = k,
    k_imputados_tf = tf$k0,
    lnRR_original  = coef(mod_uni),
    lnRR_ajustado  = coef(tf),
    diff_pct       = (exp(coef(tf)) - exp(coef(mod_uni))) / exp(coef(mod_uni)) * 100
  )
})

cat("\n--- Trim-and-fill ---\n")
print(trimfill_results)

# ---------------------------------------------------------------
# 3. Leave-one-out e leave-one-study-out
# ---------------------------------------------------------------

loo_results <- map_dfr(levels(bd$Dimensao), function(dim) {

  df <- bd %>% filter(Dimensao == dim)
  k  <- n_distinct(df$Study_ID)
  if (k < 4) return(NULL)

  estudos <- unique(df$Study_ID)

  map_dfr(estudos, function(s) {
    df_loo <- df %>% filter(Study_ID != s)
    V_loo  <- vcalc(vi = vi, cluster = Study_ID, obs = seq_len(nrow(df_loo)),
                    rho = rho_ref, data = df_loo)

    mod_loo <- tryCatch(
      rma.mv(yi = lnRR, V = V_loo, random = ~ 1 | Study_ID / Proxy,
             data = df_loo, method = "REML"),
      error = function(e) NULL
    )
    if (is.null(mod_loo)) return(NULL)

    tibble(
      Dimensao     = dim,
      Excluido     = s,
      Excluido_ref = unique(df$Study[df$Study_ID == s])[1],
      lnRR_loo     = coef(mod_loo),
      tau2_loo     = sum(mod_loo$sigma2)
    )
  })
})

cat("\n--- Leave-one-study-out ---\n")
print(loo_results)

# ---------------------------------------------------------------
# 4. Sensibilidade por qualidade NOS (restringir a alta qualidade)
#    NOTA: NOS não disponível nos dados — seção desativada
# ---------------------------------------------------------------

cat("\n--- Sensibilidade NOS: DESATIVADA (NOS não preenchido) ---\n")
sens_nos <- tibble(
  Dimensao  = character(),
  k_full    = integer(),
  k_alta    = integer(),
  lnRR_full = double(),
  lnRR_alta = double()
)

# ---------------------------------------------------------------
# 5. Sensibilidade: T1 (evidência direta) vs todos os tiers
# ---------------------------------------------------------------

cat("\n--- Sensibilidade T1 only vs. todos ---\n")

sens_tier <- map_dfr(levels(bd$Dimensao), function(dim) {
  df_full <- bd %>% filter(Dimensao == dim)
  df_t1   <- bd %>% filter(Dimensao == dim, Tier == "T1")

  k_full <- n_distinct(df_full$Study_ID)
  k_t1   <- n_distinct(df_t1$Study_ID)

  if (k_t1 < 2) {
    return(tibble(Dimensao = dim, k_full = k_full, k_T1 = k_t1,
                  lnRR_full = NA, lnRR_T1 = NA))
  }

  mod_full <- rma(yi = lnRR, vi = vi, data = df_full %>%
                    group_by(Study_ID) %>%
                    summarise(lnRR = mean(lnRR), vi = mean(vi), .groups = "drop"),
                  method = "REML")
  mod_t1 <- rma(yi = lnRR, vi = vi, data = df_t1, method = "REML")

  tibble(
    Dimensao  = dim,
    k_full    = k_full,
    k_T1      = k_t1,
    lnRR_full = coef(mod_full),
    lnRR_T1   = coef(mod_t1),
    diff_pct  = (exp(coef(mod_t1)) - exp(coef(mod_full))) / exp(coef(mod_full)) * 100
  )
})

print(sens_tier)

# ---------------------------------------------------------------
# 6. Exportar todos os resultados de viés e sensibilidade
# ---------------------------------------------------------------

writexl::write_xlsx(vies_results,     file.path(DIR_OUTPUT, "vies_publicacao.xlsx"))
writexl::write_xlsx(trimfill_results, file.path(DIR_OUTPUT, "trimfill.xlsx"))
writexl::write_xlsx(loo_results,      file.path(DIR_OUTPUT, "leave_one_out.xlsx"))
writexl::write_xlsx(sens_tier,        file.path(DIR_OUTPUT, "sensibilidade_tier.xlsx"))

cat("✔ Viés de publicação e sensibilidade concluídos.\n")

# ================================================================
# 02_extracao_dados.R — Extração, cálculo de lnRR e imputação MICE
# Artigo 2: Meta-análise de vulnerabilidade biocultural (V1–V6)
# Adaptado de: 11-ARTIGO_MA / efeito_aleatorio_multi.R
# ================================================================

source("00_setup.R")

# ---------------------------------------------------------------
# 1. Carregar banco de dados de extração
# ---------------------------------------------------------------
# O banco deve conter as colunas:
#   Study, Dimensao (V1–V6), Proxy, n_T, m_T, sd_T, n_C, m_C, sd_C,
#   Tipo_Intervencao, Regiao, Tipo_Comunidade, Tempo_Intervencao, NOS

bd <- readxl::read_excel(
  file.path(DIR_DADOS, "bd_extracao.xlsx"),
  sheet = "DADOS"
) %>%
  mutate(
    across(c(n_T, m_T, sd_T, n_C, m_C, sd_C, Tempo_Intervencao, NOS), as.numeric),
    Dimensao         = factor(Dimensao, levels = paste0("V", 1:6)),
    Tipo_Intervencao = factor(Tipo_Intervencao),
    Regiao           = factor(Regiao),
    Tipo_Comunidade  = factor(Tipo_Comunidade),
    Study_ID         = as.integer(factor(Study))
  )

cat("Estudos carregados:", n_distinct(bd$Study), "\n")
cat("Observações:", nrow(bd), "\n")
cat("Dimensões representadas:", paste(levels(bd$Dimensao), collapse = ", "), "\n")

# ---------------------------------------------------------------
# 2. Imputação múltipla para variâncias faltantes (MICE/CART)
# ---------------------------------------------------------------
# Conforme §2.10 do manuscrito: 20 conjuntos, método CART, regras Rubin

set.seed(2024)
bd_imput <- mice::mice(
  bd %>% select(n_T, m_T, sd_T, n_C, m_C, sd_C, NOS),
  m = 20,
  method = "cart",
  maxit = 10,
  printFlag = FALSE
)

# Verificar convergência
plot(bd_imput)

# ---------------------------------------------------------------
# 3. Calcular lnRR e variância amostral (vi) por imputação
# ---------------------------------------------------------------
# Equações §2.11:
#   lnRR = ln(X̄_T / X̄_C)                              (Eq. 1)
#   vi   = SD_T² / (n_T · X̄_T²) + SD_C² / (n_C · X̄_C²)  (Eq. 2)

bd_completos <- mice::complete(bd_imput, action = "long", include = FALSE) %>%
  bind_cols(bd %>% select(Study, Study_ID, Dimensao, Proxy,
                          Tipo_Intervencao, Regiao, Tipo_Comunidade,
                          Tempo_Intervencao) %>%
              slice(rep(1:n(), 20))) %>%
  filter(m_T > 0, m_C > 0) %>%
  mutate(
    lnRR = log(m_T / m_C),
    vi   = (sd_T^2 / (n_T * m_T^2)) + (sd_C^2 / (n_C * m_C^2)),
    vi   = pmax(vi, 1e-6)  # piso para estabilidade numérica
  ) %>%
  filter(!is.na(lnRR), !is.infinite(lnRR), !is.na(vi), vi < quantile(vi, 0.999, na.rm = TRUE))

cat("Observações válidas após MICE:", nrow(bd_completos), "\n")

# ---------------------------------------------------------------
# 4. Contagem de estudos e observações por dimensão
# ---------------------------------------------------------------

k_por_dimensao <- bd %>%
  group_by(Dimensao) %>%
  summarise(
    k_estudos = n_distinct(Study),
    n_obs     = n(),
    .groups   = "drop"
  )

print(k_por_dimensao)

# Classificar status analítico conforme Tabela 3 do manuscrito
k_por_dimensao <- k_por_dimensao %>%
  mutate(
    Status = case_when(
      k_estudos >= 15 ~ "Confirmatória",
      k_estudos >= 10 ~ "Confirmatória (subgrupos condicionais)",
      k_estudos >= 3  ~ "Exploratória",
      TRUE            ~ "Síntese narrativa"
    )
  )

print(k_por_dimensao)

# ---------------------------------------------------------------
# 5. Exportar banco processado
# ---------------------------------------------------------------

saveRDS(bd_completos, file.path(DIR_OUTPUT, "bd_lnRR_imputado.rds"))
saveRDS(k_por_dimensao, file.path(DIR_OUTPUT, "k_por_dimensao.rds"))

writexl::write_xlsx(
  k_por_dimensao,
  file.path(DIR_OUTPUT, "diagnostico_k_dimensoes.xlsx")
)

cat("✔ Banco processado salvo em:", file.path(DIR_OUTPUT, "bd_lnRR_imputado.rds"), "\n")

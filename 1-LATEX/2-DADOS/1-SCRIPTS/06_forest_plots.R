# ================================================================
# 06_forest_plots.R — Forest plots por dimensão (V1–V6) e agregado
# Artigo 2: Meta-análise de vulnerabilidade biocultural
# Adaptado de: 11-ARTIGO_MA / grafico_agregado.R,
#              efeito_aleatorio_fisicas.R
# ================================================================

source("00_setup.R")

bd      <- readRDS(file.path(DIR_OUTPUT, "bd_lnRR_misto.rds"))
res_dim <- readRDS(file.path(DIR_OUTPUT, "resultados_por_dimensao.rds"))

# ---------------------------------------------------------------
# Mapa de cores por dimensão (6 cores distintas)
# ---------------------------------------------------------------

cores_dim <- c(
  "V1" = "#D55E00",   # Erosão Intergeracional — vermelho
  "V2" = "#009E73",   # Complexidade Biocultural — verde
  "V3" = "#56B4E9",   # Singularidade Territorial — azul claro
  "V4" = "#E69F00",   # Status de Documentação — amarelo
  "V5" = "#CC79A7",   # Vulnerabilidade Jurídica — rosa
  "V6" = "#0072B2"    # Organização Social — azul escuro
)

nomes_dim <- c(
  "V1" = "Erosao Intergeracional",
  "V2" = "Complexidade Biocultural",
  "V3" = "Singularidade Territorial",
  "V4" = "Status de Documentacao",
  "V5" = "Vulnerabilidade Juridica",
  "V6" = "Organizacao Social"
)

# ===============================================================
# 1. Forest plot INDIVIDUAL por dimensão (com estudos)
# ===============================================================

for (dim in levels(bd$Dimensao)) {

  df <- bd %>% filter(Dimensao == dim)
  k  <- n_distinct(df$Study_ID)
  if (k < 3) next

  # Agregar por estudo para forest plot individual
  agg <- df %>%
    group_by(Study_ID, Study) %>%
    summarise(lnRR = mean(lnRR), vi = mean(vi), .groups = "drop")

  meta_dim <- metagen(
    TE       = agg$lnRR,
    seTE     = sqrt(agg$vi),
    studlab  = agg$Study,
    sm       = "lnRR",
    method.tau = "REML",
    common   = FALSE,
    random   = TRUE
  )

  pdf(file.path(DIR_OUTPUT, paste0("forest_", dim, ".pdf")), width = 10, height = max(6, k * 0.5))

  forest(
    meta_dim,
    comb.fixed  = FALSE,
    comb.random = TRUE,
    overall     = TRUE,
    print.tau2  = TRUE,
    print.I2    = TRUE,
    col.square  = cores_dim[dim],
    col.diamond = "black",
    digits      = 3,
    digits.TE   = 3,
    atransf     = identity,
    xlab        = "lnRR (log response ratio)",
    rightcols   = c("effect", "ci", "w.random"),
    rightlabs   = c("lnRR", "IC 95%", "Peso (%)"),
    leftcols    = c("studlab"),
    leftlabs    = c(paste0(nomes_dim[dim], " (", dim, ")")),
    smlab       = paste0(dim, " — ", nomes_dim[dim])
  )

  dev.off()
  cat("✔ Forest plot:", dim, "\n")
}

# ===============================================================
# 2. Forest plot AGREGADO (todas as dimensões)
# ===============================================================

# Usar resultados já calculados em 03_meta_analise_dimensao.R
res_plot <- res_dim %>%
  filter(!is.na(lnRR)) %>%
  mutate(
    label = paste0(Dimensao, " — ", nomes_dim[Dimensao],
                   " (k = ", k, ")"),
    label = fct_reorder(label, lnRR)
  )

meta_agg <- metagen(
  TE       = res_plot$lnRR,
  seTE     = res_plot$se,
  studlab  = res_plot$label,
  sm       = "lnRR",
  method.tau = "DL",
  common   = FALSE,
  random   = TRUE
)

pdf(file.path(DIR_OUTPUT, "forest_agregado_V1_V6.pdf"), width = 11, height = 7)

forest(
  meta_agg,
  comb.fixed       = FALSE,
  comb.random      = TRUE,
  overall          = TRUE,
  print.tau2       = TRUE,
  print.I2         = TRUE,
  col.square       = cores_dim[as.character(res_plot$Dimensao)],
  col.diamond      = "black",
  digits           = 3,
  digits.TE        = 3,
  atransf          = identity,
  at               = seq(-1, 1, by = 0.2),
  xlab             = "lnRR (log response ratio)",
  rightcols        = c("effect", "ci", "w.random"),
  rightlabs        = c("lnRR", "IC 95%", "Peso (%)"),
  leftcols         = c("studlab"),
  leftlabs         = c("Dimensão de vulnerabilidade (k)"),
  smlab            = "Efeito agregado por dimensão"
)

dev.off()
cat("✔ Forest plot agregado V1–V6.\n")

# ===============================================================
# 3. Forest plot com ggplot2 (publicação)
# ===============================================================

p <- ggplot(res_plot, aes(x = lnRR, y = label)) +
  geom_point(aes(color = Dimensao), size = 4, shape = 18) +
  geom_errorbarh(aes(xmin = ci_lo, xmax = ci_hi, color = Dimensao),
                 height = 0.25, linewidth = 0.7) +
  # Prediction interval (mais claro)
  geom_errorbarh(aes(xmin = pi_lo, xmax = pi_hi, color = Dimensao),
                 height = 0.12, linewidth = 0.4, linetype = "dashed") +
  geom_vline(xintercept = 0, linetype = "dashed", color = "gray40") +
  scale_color_manual(values = cores_dim, guide = "none") +
  labs(
    x = expression(italic(lnRR) ~ "(log response ratio)"),
    y = NULL,
    title = "Efeito de intervenções de salvaguarda por dimensão de vulnerabilidade",
    subtitle = "IC 95% (sólido) e intervalo de predição (tracejado)"
  ) +
  theme_minimal(base_size = 12) +
  theme(
    panel.grid.major.y = element_blank(),
    plot.title = element_text(face = "bold", size = 13),
    plot.subtitle = element_text(size = 10, color = "gray40")
  )

ggsave(file.path(DIR_OUTPUT, "forest_agregado_V1_V6.pdf"), p, width = 10, height = 6)
ggsave(file.path(DIR_OUTPUT, "forest_agregado_V1_V6.png"), p, width = 10, height = 6, dpi = 300)

cat("✔ Forest plots concluídos e exportados.\n")

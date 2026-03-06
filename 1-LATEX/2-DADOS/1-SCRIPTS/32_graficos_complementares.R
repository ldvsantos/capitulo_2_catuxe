#!/usr/bin/env Rscript
# =============================================================================
# 32_graficos_complementares.R
# Gráficos complementares para o artigo 2:
#   (A) Meta-regressão — coeficientes de moderadores por dimensão
#   (B) Sensibilidade Tier — dumbbell plot (T1 vs modelo completo)
#   (C1) Leave-one-out V1–V3
#   (C2) Leave-one-out V4–V6
# =============================================================================

library(here)
library(readxl)
library(ggplot2)
library(dplyr)
library(tidyr)
library(forcats)

DIR_OUT <- here("2-DADOS", "3-OUTPUT")

# Tema base consistente
theme_artigo <- theme_minimal(base_size = 11) +
  theme(
    panel.grid.minor   = element_blank(),
    panel.grid.major.y = element_line(colour = "grey90"),
    panel.grid.major.x = element_line(colour = "grey90"),
    plot.title         = element_text(face = "bold", size = 12),
    plot.subtitle      = element_text(size = 9, colour = "grey40"),
    axis.title         = element_text(size = 10),
    legend.position    = "bottom"
  )

# Paleta de cores para dimensões
dim_cores <- c(
  "V1" = "#E69F00", "V2" = "#56B4E9", "V3" = "#009E73",
  "V4" = "#F0E442", "V5" = "#D55E00", "V6" = "#0072B2"
)
dim_nomes <- c(
  "V1" = "V1 Erosao Intergeracional",
  "V2" = "V2 Complexidade Biocultural",
  "V3" = "V3 Singularidade Territorial",
  "V4" = "V4 Status de Documentacao",
  "V5" = "V5 Vulnerabilidade Juridica",
  "V6" = "V6 Organizacao Social"
)

res <- read_excel(file.path(DIR_OUT, "resultados_por_dimensao.xlsx"))

# =============================================================================
# (A) META-REGRESSÃO — bubble scatter plot (lnRR × moderador categórico)
#     Cada bolha = 1 observação estudo-dimensão; tamanho ∝ peso (1/vi)
#     Diamante vermelho = média predita por categoria; mostra dispersão real
# =============================================================================
cat(">>> Gráfico A: Bubble scatter plot de meta-regressão\n")

bd <- readRDS(file.path(DIR_OUT, "bd_lnRR_misto.rds"))

# ---------- Painel 1: Região ----------
df_reg <- bd %>%
  mutate(
    Dim_label = factor(dim_nomes[Dimensao], levels = dim_nomes),
    peso      = 1 / vi
  )

p_reg <- ggplot(df_reg, aes(x = Regiao, y = lnRR)) +
  geom_hline(yintercept = 0, linetype = "dashed", colour = "grey50", linewidth = 0.4) +
  annotate("rect", ymin = -0.1, ymax = 0.1, xmin = -Inf, xmax = Inf,
           fill = "grey90", alpha = 0.35) +
  geom_jitter(aes(size = peso, colour = Regiao), alpha = 0.50, width = 0.22) +
  facet_wrap(~ Dim_label, ncol = 3, scales = "free_y") +
  scale_size_continuous(range = c(1, 7), guide = "none") +
  scale_colour_brewer(palette = "Set2", name = "Regiao") +
  labs(
    title    = "Meta-regressao: efeito por Regiao",
    subtitle = "Cada bolha = 1 observacao (tamanho ~ peso 1/vi).\nFaixa cinza = zona de efeito negligenciavel (|lnRR| < 0,1)",
    x = NULL, y = "lnRR"
  ) +
  theme_artigo +
  theme(
    strip.text    = element_text(size = 9, face = "bold"),
    axis.text.x   = element_text(angle = 40, hjust = 1, size = 8),
    legend.title  = element_text(size = 9, face = "bold")
  )

ggsave(file.path(DIR_OUT, "meta_regressao_regiao.pdf"), p_reg,
       width = 14, height = 9, dpi = 300)
ggsave(file.path(DIR_OUT, "meta_regressao_regiao.png"), p_reg,
       width = 14, height = 9, dpi = 300)
cat("   Salvo: meta_regressao_regiao.pdf/.png\n")

# ---------- Painel 2: Tipo de Comunidade ----------
p_com <- ggplot(df_reg, aes(x = Tipo_Comunidade, y = lnRR)) +
  geom_hline(yintercept = 0, linetype = "dashed", colour = "grey50", linewidth = 0.4) +
  annotate("rect", ymin = -0.1, ymax = 0.1, xmin = -Inf, xmax = Inf,
           fill = "grey90", alpha = 0.35) +
  geom_jitter(aes(size = peso, colour = Tipo_Comunidade), alpha = 0.50, width = 0.22) +
  facet_wrap(~ Dim_label, ncol = 3, scales = "free_y") +
  scale_size_continuous(range = c(1, 7), guide = "none") +
  scale_colour_brewer(palette = "Dark2", name = "Tipo de Comunidade") +
  labs(
    title    = "Meta-regressao: efeito por Tipo de Comunidade",
    subtitle = "Cada bolha = 1 observacao (tamanho ~ peso 1/vi).\nFaixa cinza = zona de efeito negligenciavel (|lnRR| < 0,1)",
    x = NULL, y = "lnRR"
  ) +
  theme_artigo +
  theme(
    strip.text    = element_text(size = 9, face = "bold"),
    axis.text.x   = element_text(angle = 40, hjust = 1, size = 8),
    legend.title  = element_text(size = 9, face = "bold")
  )

ggsave(file.path(DIR_OUT, "meta_regressao_comunidade.pdf"), p_com,
       width = 14, height = 9, dpi = 300)
ggsave(file.path(DIR_OUT, "meta_regressao_comunidade.png"), p_com,
       width = 14, height = 9, dpi = 300)
cat("   Salvo: meta_regressao_comunidade.pdf/.png\n")

# ---------- Painel 3: Tipo de Intervenção (macro-categorias) ----------
macro_map <- c(
  "Agrobiodiversity management"       = "Gestão agrobiodivers.",
  "Agroforestry assessment"           = "Avaliação de sistemas",
  "Agroforestry management"           = "Gestão agrobiodivers.",
  "Biocultural conservation"          = "Conserv. biocultural",
  "Biocultural landscape assessment"  = "Avaliação de sistemas",
  "Climate adaptation assessment"     = "Avaliação de sistemas",
  "Ecological knowledge indicator"    = "Indicadores de conhecim.",
  "Ethnobotanical assessment"         = "Avaliação de sistemas",
  "Ethnobotanical survey"             = "Avaliação de sistemas",
  "Farmer perception survey"          = "Avaliação de sistemas",
  "Herbal knowledge assessment"       = "Indicadores de conhecim.",
  "Home garden knowledge transmission"= "Transmissão de saberes",
  "Indigenous knowledge transmission" = "Transmissão de saberes",
  "Indigenous storytelling review"    = "Transmissão de saberes",
  "Land sharing assessment"           = "Avaliação de sistemas",
  "Landscape ethnoecology"            = "Avaliação de sistemas",
  "Medicinal plant survey"            = "Indicadores de conhecim.",
  "On-farm conservation"              = "Conserv. biocultural",
  "Post-disaster food security"       = "Seg. alimentar / adapt.",
  "Sacred grove conservation"         = "Conserv. biocultural",
  "Seed network analysis"             = "Gestão agrobiodivers.",
  "Seed system assessment"            = "Gestão agrobiodivers.",
  "Soil conservation assessment"      = "Avaliação de sistemas",
  "Traditional beekeeping"            = "Gestão agrobiodivers.",
  "Traditional flood knowledge"       = "Seg. alimentar / adapt.",
  "Traditional knowledge erosion"     = "Indicadores de conhecim.",
  "Traditional weather knowledge"     = "Seg. alimentar / adapt."
)

df_int <- df_reg %>%
  mutate(Macro_Interv = macro_map[Tipo_Intervencao]) %>%
  filter(!is.na(Macro_Interv))

p_int <- ggplot(df_int, aes(x = Macro_Interv, y = lnRR)) +
  geom_hline(yintercept = 0, linetype = "dashed", colour = "grey50", linewidth = 0.4) +
  annotate("rect", ymin = -0.1, ymax = 0.1, xmin = -Inf, xmax = Inf,
           fill = "grey90", alpha = 0.35) +
  geom_jitter(aes(size = peso, colour = Macro_Interv), alpha = 0.50, width = 0.22) +
  facet_wrap(~ Dim_label, ncol = 3, scales = "free_y") +
  scale_size_continuous(range = c(1, 7), guide = "none") +
  scale_colour_brewer(palette = "Set1", name = "Macro-categoria") +
  labs(
    title    = "Meta-regressao: efeito por Tipo de Intervencao (macro-categorias)",
    subtitle = "Cada bolha = 1 observacao (tamanho ~ peso 1/vi).\nFaixa cinza = zona de efeito negligenciavel (|lnRR| < 0,1)",
    x = NULL, y = "lnRR"
  ) +
  theme_artigo +
  theme(
    strip.text    = element_text(size = 9, face = "bold"),
    axis.text.x   = element_text(angle = 45, hjust = 1, size = 7.5),
    legend.title  = element_text(size = 9, face = "bold")
  )

ggsave(file.path(DIR_OUT, "meta_regressao_intervencao.pdf"), p_int,
       width = 14, height = 9, dpi = 300)
ggsave(file.path(DIR_OUT, "meta_regressao_intervencao.png"), p_int,
       width = 14, height = 9, dpi = 300)
cat("   Salvo: meta_regressao_intervencao.pdf/.png\n")


# =============================================================================
# (B) SENSIBILIDADE TIER — dumbbell plot (modelo completo vs T1-only)
# =============================================================================
cat(">>> Gráfico B: Sensibilidade Tier (dumbbell)\n")

st <- read_excel(file.path(DIR_OUT, "sensibilidade_tier.xlsx"))

df_tier <- st %>%
  mutate(
    Dim_label = factor(dim_nomes[Dimensao], levels = rev(dim_nomes))
  ) %>%
  pivot_longer(cols = c(lnRR_full, lnRR_T1),
               names_to = "Modelo", values_to = "lnRR_val") %>%
  mutate(Modelo = ifelse(Modelo == "lnRR_full",
                         "Completo (T1\u2013T4)",
                         "Tier 1 apenas"))

# Segmentos entre pontos
df_seg <- st %>%
  mutate(Dim_label = factor(dim_nomes[Dimensao], levels = rev(dim_nomes)))

p_tier <- ggplot() +
  geom_segment(data = df_seg,
               aes(x = lnRR_full, xend = lnRR_T1,
                   y = Dim_label, yend = Dim_label),
               colour = "grey60", linewidth = 0.8) +
  geom_point(data = df_tier,
             aes(x = lnRR_val, y = Dim_label, colour = Modelo, shape = Modelo),
             size = 3.5) +
  geom_vline(xintercept = 0, linetype = "dashed", colour = "grey50") +
  scale_colour_manual(values = c("grey30", "#D55E00")) +
  scale_shape_manual(values = c(16, 17)) +
  labs(
    title = "Sensibilidade das estimativas à composição de tiers",
    subtitle = "Comparação modelo completo (T1–T4) vs. subconjunto Tier 1 apenas",
    x = expression(bar(lnRR)),
    y = NULL,
    colour = "Modelo", shape = "Modelo"
  ) +
  theme_artigo

ggsave(file.path(DIR_OUT, "sensibilidade_tier_plot.pdf"), p_tier,
       width = 8, height = 4.5, dpi = 300)
ggsave(file.path(DIR_OUT, "sensibilidade_tier_plot.png"), p_tier,
       width = 8, height = 4.5, dpi = 300)
cat("   Salvo: sensibilidade_tier_plot.pdf/.png\n")


# =============================================================================
# (C) LEAVE-ONE-OUT — influence plots divididos em 2 figuras
# =============================================================================
cat(">>> Gráfico C: Leave-one-out influence plots\n")

loo <- read_excel(file.path(DIR_OUT, "leave_one_out.xlsx"))

# Referência: lnRR global por dimensão
ref <- res %>% select(Dimensao, lnRR_global = lnRR)

df_loo <- loo %>%
  left_join(ref, by = "Dimensao") %>%
  mutate(
    Dim_label = dim_nomes[Dimensao],
    Deslocamento = lnRR_loo - lnRR_global,
    Influente = abs(Deslocamento) > 2 * sd(Deslocamento)
  ) %>%
  group_by(Dimensao) %>%
  arrange(desc(abs(Deslocamento))) %>%
  mutate(rank_infl = row_number()) %>%
  ungroup()

# Função para gerar LOO plot de um subconjunto de dimensões
gerar_loo <- function(dims, sufixo, titulo_parte) {
  df_sub <- df_loo %>%
    filter(Dimensao %in% dims) %>%
    mutate(Dim_label = factor(dim_nomes[Dimensao], levels = dim_nomes[dims]))

  ref_sub <- ref %>%
    filter(Dimensao %in% dims) %>%
    mutate(Dim_label = factor(dim_nomes[Dimensao], levels = dim_nomes[dims]))

  p <- ggplot(df_sub, aes(x = lnRR_loo, y = reorder(as.character(Excluido), lnRR_loo))) +
    geom_vline(data = ref_sub,
               aes(xintercept = lnRR_global),
               linetype = "dashed", colour = "red", linewidth = 0.5) +
    geom_point(aes(colour = Dimensao), size = 1.8, alpha = 0.7) +
    scale_colour_manual(values = dim_cores, guide = "none") +
    facet_wrap(~ Dim_label, scales = "free", ncol = 3) +
    labs(
      title = paste0("Análise leave-one-out: estabilidade das estimativas (", titulo_parte, ")"),
      subtitle = "Cada ponto = lnRR após excluir um estudo. Linha vermelha = estimativa global.",
      x = expression(lnRR[LOO]),
      y = "Estudo excluído (ID)"
    ) +
    theme_artigo +
    theme(
      axis.text.y  = element_text(size = 6),
      strip.text   = element_text(face = "bold", size = 10)
    )

  ggsave(file.path(DIR_OUT, paste0("leave_one_out_", sufixo, ".pdf")), p,
         width = 12, height = 6, dpi = 300)
  ggsave(file.path(DIR_OUT, paste0("leave_one_out_", sufixo, ".png")), p,
         width = 12, height = 6, dpi = 300)
  cat(paste0("   Salvo: leave_one_out_", sufixo, ".pdf/.png\n"))
}

gerar_loo(c("V1", "V2", "V3"), "V1_V3", "V1–V3")
gerar_loo(c("V4", "V5", "V6"), "V4_V6", "V4–V6")


cat("\n>>> Todos os gráficos complementares gerados com sucesso!\n")

# ================================================================
# 00_setup.R — Instalação e carregamento de pacotes
# Artigo 2: Meta-análise de vulnerabilidade biocultural (V1–V8)
# ================================================================

# Mirror CRAN
options(repos = c(CRAN = "https://cloud.r-project.org"))

pacotes <- c(

  # Meta-análise e variância robusta

"metafor", "meta", "clubSandwich",
  # Imputação múltipla
  "mice",
  # Manipulação e IO
  "readxl", "writexl", "dplyr", "tidyr", "tibble", "stringr",
  "purrr", "forcats", "data.table",
  # Paralelização
  "future.apply",
  # Tabelas
  "knitr", "kableExtra",
  # Gráficos
  "ggplot2", "ggrepel",
  # PCA / análise exploratória
  "FactoMineR", "factoextra",
  # Bibliometria (revisão sistemática)
  "bibliometrix", "revtools",
  # Caminhos relativos
  "here"
)

instalar <- pacotes[!(pacotes %in% installed.packages()[, "Package"])]
if (length(instalar) > 0) install.packages(instalar, dependencies = TRUE)

invisible(lapply(pacotes, library, character.only = TRUE))

# dmetar: não disponível no CRAN para R >= 4.5; instalar do GitHub
if (!requireNamespace("dmetar", quietly = TRUE)) {
  if (!requireNamespace("remotes", quietly = TRUE)) install.packages("remotes")
  remotes::install_github("MathiasHarrer/dmetar", upgrade = "never")
}
library(dmetar)

# Paralelização
future::plan(future::multisession)

# Limpar ambiente
rm(list = ls()); gc()

# Caminhos relativos
DIR_DADOS  <- here::here("2-DADOS", "2-BANCO_DADOS")
DIR_OUTPUT <- here::here("2-DADOS", "3-OUTPUT")
dir.create(DIR_OUTPUT, showWarnings = FALSE, recursive = TRUE)

cat("✔ Setup concluído. Pacotes carregados.\n")

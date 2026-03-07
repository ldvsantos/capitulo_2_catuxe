#!/usr/bin/env Rscript
# ================================================================
# 10_gerar_prisma.R — Fluxograma PRISMA 2020 (PT + EN)
# Artigo 2: Meta-análise de vulnerabilidade biocultural (V1–V8)
#
# Adaptado de: artigo_1_catuxe / gerar_prisma_portugues.R
# Gera diagrama PRISMA 2020 usando o pacote PRISMA2020 do R
# com dados específicos desta meta-análise.
# Produz duas versões: PT (para tese) e EN (para submissão).
#
# Contagens (conforme §3.1 do manuscrito):
#   Scopus: 193 | WoS: 172 | Total bruto: 365
#   Filtro documental: -33 → 332
#   Filtro temporal: -20 → 310 (total removidos antes dedup: 55)
#   Deduplicação DOI+título: -117 → 193 únicos
#   Triagem semântica PICOS: -151 → 42 (automático)
#   Re-triagem manual (resumos ausentes): +6 → 48
#   Texto completo: 48 avaliados
#   Incluídos na síntese: 48
# ================================================================

# Suprimir avisos
options(warn = -1)

# Configurar CRAN mirror
options(repos = c(CRAN = "https://cran.rstudio.com"))

# Verificar e instalar pacotes necessários
pacotes_necessarios <- c("devtools", "htmlwidgets", "DiagrammeR")

for (pacote in pacotes_necessarios) {
  if (!require(pacote, character.only = TRUE, quietly = TRUE)) {
    cat(sprintf("Instalando pacote: %s\n", pacote))
    install.packages(pacote, quiet = TRUE)
    library(pacote, character.only = TRUE)
  }
}

# Instalar PRISMA2020 do GitHub se necessário
if (!require("PRISMA2020", character.only = TRUE, quietly = TRUE)) {
  cat("Instalando PRISMA2020 do GitHub...\n")
  if (!requireNamespace("magrittr", quietly = TRUE)) {
    install.packages("magrittr", quiet = TRUE)
  }
  devtools::install_github("prisma-flowdiagram/PRISMA2020",
                           quiet = TRUE, force = TRUE)
}

library(PRISMA2020, quietly = TRUE)
library(htmlwidgets, quietly = TRUE)
library(DiagrammeR, quietly = TRUE)

# ---------------------------------------------------------------
# Diretórios
# ---------------------------------------------------------------
script_dir <- dirname(normalizePath(
  if (interactive()) rstudioapi::getSourceEditorContext()$path
  else commandArgs(trailingOnly = FALSE)[4],
  winslash = "/"
))
setwd(script_dir)

DIR_OUTPUT  <- file.path("..", "3-OUTPUT")
DIR_FIGURAS <- file.path("..", "..", "3-FIGURAS")
dir.create(DIR_OUTPUT,  showWarnings = FALSE, recursive = TRUE)
dir.create(DIR_FIGURAS, showWarnings = FALSE, recursive = TRUE)

cat("======================================================================\n")
cat("GERADOR DE FLUXOGRAMA PRISMA 2020 - ARTIGO 2 (PT + EN)\n")
cat("Meta-análise de vulnerabilidade biocultural em SSAT\n")
cat("======================================================================\n\n")

# ---------------------------------------------------------------
# 1. Carregar CSV do PRISMA
# ---------------------------------------------------------------
csv_file <- "PRISMA_artigo2.csv"

if (!file.exists(csv_file)) {
  cat(sprintf("Arquivo %s não encontrado!\n", csv_file))
  quit(status = 1)
}

cat(sprintf("Carregando dados PRISMA de: %s\n", csv_file))
data <- read.csv(csv_file, sep = ",", stringsAsFactors = FALSE, check.names = FALSE)
cat("Dados carregados com sucesso\n\n")

# ---------------------------------------------------------------
# 2. Traduzir textos para português
# ---------------------------------------------------------------
cat("Traduzindo textos para português...\n")

traduzir_texto <- function(texto) {
  traducoes <- list(
    # Títulos das seções principais
    "Grey title box; Previous studies" = "Caixa cinza; Estudos anteriores",
    "Previous studies" = "Estudos anteriores",
    "Studies included in previous version of review" =
      "Estudos incluídos na versão anterior da revisão",
    "Reports of studies included in previous version of review" =
      "Relatórios de estudos incluídos na versão anterior da revisão",

    # Identificação
    "Yellow title box; Identification of new studies via databases and registers" =
      "Caixa amarela; Identificação de novos estudos via bases de dados e registros",
    "Identification of new studies via databases and registers" =
      "Identificação de novos estudos via bases de dados e registros",
    "Records identified from: Databases" =
      "Registros identificados em: Bases de dados",
    "Databases" = "Bases de dados",
    "Records identified from: Databases and Registers" =
      "Registros identificados em: Bases de dados e Registros",
    "Records identified from: specific databases" =
      "Registros identificados em: bases específicas",
    "Specific Databases" = "Bases específicas",
    "Records identified from: Registers" =
      "Registros identificados em: Registros",
    "Registers" = "Registros",
    "Records identified from: specific registers" =
      "Registros identificados em: registros específicos",
    "Specific Registers" = "Registros específicos",

    # Outros métodos
    "Grey title box; Identification of new studies via other methods" =
      "Caixa cinza; Identificação de novos estudos via outros métodos",
    "Identification of new studies via other methods" =
      "Identificação de novos estudos via outros métodos",
    "Records identified from: Websites" =
      "Registros identificados em: Sites web",
    "Websites" = "Sites web",
    "Records identified from: Websites, Organisations and Citation Searching" =
      "Registros identificados em: Sites, Organizações e Busca por citações",
    "Records identified from: Organisations" =
      "Registros identificados em: Organizações",
    "Organisations" = "Organizações",
    "Records identified from: Citation searching" =
      "Registros identificados em: Busca por citações",
    "Citation searching" = "Busca por citações",

    # Triagem
    "Duplicate records" = "Registros duplicados",
    "Records marked as ineligible by automation tools" =
      "Registros inelegíveis por automação (filtros documental e temporal)",
    "Records removed for other reasons" =
      "Registros removidos por outros motivos",
    "Records screened (databases and registers)" =
      "Registros triados (bases de dados e registros)",
    "Records screened" = "Registros triados",
    "Records excluded (databases and registers)" =
      "Registros excluídos (bases de dados e registros)",
    "Records excluded" = "Registros excluídos",

    # Elegibilidade
    "Reports sought for retrieval (databases and registers)" =
      "Relatórios buscados para recuperação (bases de dados e registros)",
    "Reports sought for retrieval" = "Relatórios buscados para recuperação",
    "Reports not retrieved (databases and registers)" =
      "Relatórios não recuperados (bases de dados e registros)",
    "Reports not retrieved" = "Relatórios não recuperados",
    "Reports assessed for eligibility (databases and registers)" =
      "Relatórios avaliados para elegibilidade (bases de dados e registros)",
    "Reports assessed for eligibility" =
      "Relatórios avaliados para elegibilidade",
    "Reports excluded (databases and registers)" =
      "Relatórios excluídos (bases de dados e registros)",
    "Reports excluded" = "Relatórios excluídos",

    # Outros métodos de elegibilidade
    "Reports sought for retrieval (other)" =
      "Relatórios buscados para recuperação (outros)",
    "Reports not retrieved (other)" =
      "Relatórios não recuperados (outros)",
    "Reports assessed for eligibility (other)" =
      "Relatórios avaliados para elegibilidade (outros)",
    "Reports excluded (other)" =
      "Relatórios excluídos (outros)",

    # Inclusão
    "New studies included in review" =
      "Novos estudos incluídos na revisão",
    "Reports of new included studies" =
      "Relatórios de novos estudos incluídos",
    "Total studies included in review" =
      "Total de estudos incluídos na revisão",
    "Reports of total included studies" =
      "Relatórios do total de estudos incluídos",
    "Total studies included in meta-analysis" =
      "Total de estudos incluídos na meta-análise",
    "Reports of total included studies in meta-analysis" =
      "Relatórios do total de estudos na meta-análise",

    # Títulos das fases
    "Blue identification box" = "Caixa azul de identificação",
    "Blue screening box" = "Caixa azul de triagem",
    "Blue included box" = "Caixa azul de inclusão",

    # Boxes principais
    "Identification" = "Identificação",
    "Screening" = "Triagem",
    "Included" = "Incluídos"
  )

  if (texto %in% names(traducoes)) {
    return(traducoes[[texto]])
  } else {
    return(texto)
  }
}

# Aplicar traduções
if ("description" %in% names(data))
  data$description <- sapply(data$description, traduzir_texto)
if ("boxtext" %in% names(data))
  data$boxtext <- sapply(data$boxtext, traduzir_texto)
if ("tooltips" %in% names(data))
  data$tooltips <- sapply(data$tooltips, traduzir_texto)

cat("Textos traduzidos para português\n\n")

# ---------------------------------------------------------------
# 3. Processar dados e gerar fluxograma PORTUGUÊS
# ---------------------------------------------------------------
cat("Processando dados PRISMA...\n")
prisma_data <- PRISMA_data(data)

cat("Gerando fluxograma PRISMA 2020 (PT)...\n")

plot_pt <- PRISMA_flowdiagram(
  prisma_data,
  fontsize     = 12,
  font         = "Helvetica",
  title_colour = "Goldenrod1",
  greybox_colour = "Gainsboro",
  main_colour  = "Black",
  arrow_colour = "Black",
  arrow_head   = "normal",
  arrow_tail   = "none",
  interactive  = FALSE,
  previous     = FALSE,
  other        = FALSE,
  detail_databases = TRUE,
  detail_registers = FALSE,
  side_boxes       = TRUE
)

# ---------------------------------------------------------------
# 4. Salvar versão PT em múltiplos formatos
# ---------------------------------------------------------------
salvar_prisma <- function(plot_obj, prefix, dir_out) {
  formatos <- list(
    list(ext = "html", tipo = "HTML"),
    list(ext = "pdf",  tipo = "PDF"),
    list(ext = "png",  tipo = "PNG"),
    list(ext = "svg",  tipo = "SVG")
  )
  for (fmt in formatos) {
    fpath <- file.path(dir_out, paste0(prefix, ".", fmt$ext))
    tryCatch({
      PRISMA_save(plot_obj, filename = fpath, filetype = fmt$tipo, overwrite = TRUE)
      cat(sprintf("  %s: %s\n", fmt$tipo, fpath))
    }, error = function(e) {
      cat(sprintf("  Erro %s: %s\n", fmt$tipo, e$message))
    })
  }
}

cat("\nSalvando versão PT...\n")
salvar_prisma(plot_pt, "prisma_flowdiagram_artigo2", DIR_OUTPUT)

# ---------------------------------------------------------------
# 5. Gerar versão INGLÊS (para submissão)
# ---------------------------------------------------------------
cat("\n--- Gerando versão inglês (EN) para submissão ---\n")

# Recarregar CSV original sem tradução
data_en <- read.csv(csv_file, sep = ",", stringsAsFactors = FALSE, check.names = FALSE)

prisma_data_en <- PRISMA_data(data_en)

cat("Gerando fluxograma PRISMA 2020 (EN)...\n")

plot_en <- PRISMA_flowdiagram(
  prisma_data_en,
  fontsize     = 12,
  font         = "Helvetica",
  title_colour = "Goldenrod1",
  greybox_colour = "Gainsboro",
  main_colour  = "Black",
  arrow_colour = "Black",
  arrow_head   = "normal",
  arrow_tail   = "none",
  interactive  = FALSE,
  previous     = FALSE,
  other        = FALSE,
  detail_databases = TRUE,
  detail_registers = FALSE,
  side_boxes       = TRUE
)

cat("\nSalvando versão EN...\n")
salvar_prisma(plot_en, "prisma_flowdiagram_artigo2_en", DIR_OUTPUT)

# ---------------------------------------------------------------
# 6. Copiar AMBAS versões para 3-FIGURAS
# ---------------------------------------------------------------
fig_files <- list.files(DIR_OUTPUT, pattern = "prisma_flowdiagram_artigo2", full.names = TRUE)
file.copy(fig_files, DIR_FIGURAS, overwrite = TRUE)
cat(sprintf("\nCopiado para: %s\n", normalizePath(DIR_FIGURAS, winslash = "/")))

cat("\n======================================================================\n")
cat("FLUXOGRAMA PRISMA 2020 — ARTIGO 2 GERADO (PT + EN)\n")
cat("======================================================================\n")
cat(sprintf("Arquivos em: %s\n", normalizePath(DIR_OUTPUT, winslash = "/")))
cat(sprintf("Figuras em:  %s\n", normalizePath(DIR_FIGURAS, winslash = "/")))
cat("Para visualizar, abra os arquivos HTML em seu navegador\n\n")

# ---------------------------------------------------------------
# 5. Resumo das contagens (auditoria)
# ---------------------------------------------------------------
cat("--- CONTAGENS PRISMA (auditoria) ---\n")
cat("  Scopus (API):         193\n")
cat("  Web of Science:       172\n")
cat("  Total bruto:          365\n")
cat("  Filtro documental:   -33  -> 332\n")
cat("  Filtro temporal:     -20  -> 310\n")
cat("  (Total auto-excl.:    55)\n")
cat("  Deduplicação DOI:   -117  -> 193\n")
cat("  Triagem semântica:  -151  -> 42\n")
cat("  Re-triagem manual:   +6  -> 48\n")
cat("  Dedup. fuzzy:         -0  -> 48\n")
cat("  Para triagem manual:  48\n")
cat("  Texto completo:      48\n")
cat("  Incluídos síntese:   48\n")
cat("  Incluídos MA:        48\n")

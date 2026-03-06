# ================================================================
# 01_revisao_sistematica.R -- Importacao, triagem e PRISMA
# Artigo 2: Meta-analise de vulnerabilidade biocultural (V1-V6)
# ================================================================

source(here::here("2-DADOS", "1-SCRIPTS", "00_setup.R"))

# ---------------------------------------------------------------
# 1. Importar planilha consolidada (gerada por 09_integrar_wos_manual.py)
# ---------------------------------------------------------------

xlsx_consolidado <- here::here("2-DADOS", "2-BANCO_DADOS",
                               "busca_consolidada_final.xlsx")

db_all <- readxl::read_excel(xlsx_consolidado)

cat("Total de registros importados:", nrow(db_all), "\n")
cat("Colunas disponiveis:", paste(names(db_all), collapse = ", "), "\n")
cat("Tipos de documento:\n")
print(table(db_all$doc_type))

# ---------------------------------------------------------------
# 2. Deduplicacao adicional por fuzzy matching (stringdist em titulos)
# ---------------------------------------------------------------

db_all$title_norm <- tolower(trimws(db_all$title))
dup_groups <- revtools::find_duplicates(
  data.frame(TI = db_all$title_norm, stringsAsFactors = FALSE),
  match_variable = "TI",
  match_function = "stringdist",
  method = "osa",
  threshold = 5
)
# find_duplicates retorna vetor de grupos; duplicatas compartilham o mesmo grupo
n_dups_fuzzy <- length(dup_groups) - length(unique(dup_groups))
cat("Duplicatas fuzzy encontradas:", n_dups_fuzzy, "\n")

# ---------------------------------------------------------------
# 3. Blocos semanticos de busca (auditoria PICOS)
# ---------------------------------------------------------------

# Bloco 1 -- Populacao (SAT / TEK)
bloco_populacao <- paste(c(
  "traditional agricultural system", "traditional ecological knowledge",
  "indigenous farming", "quilombola", "smallholder",
  "agrobiodiversity", "agroecology",
  "traditional knowledge", "family farming",
  "biocultural", "ethnobotany", "ethnoecology"
), collapse = "|")

# Bloco 2 -- Intervencao / Salvaguarda
bloco_intervencao <- paste(c(
  "safeguard", "documentation", "heritage",
  "legal protection", "intangible heritage", "biocultural conservation",
  "community governance", "conservation",
  "policy", "protection", "resilience"
), collapse = "|")

# Bloco 3 -- Desfechos (vulnerabilidade)
bloco_desfecho <- paste(c(
  "vulnerability", "erosion", "knowledge loss",
  "intergenerational transmission", "biodiversity",
  "cultural complexity", "documentation status",
  "threat", "decline", "change", "transformation",
  "food security", "food sovereignty"
), collapse = "|")

# ---------------------------------------------------------------
# 4. Filtragem por relevancia (titulo + abstract + keywords)
# ---------------------------------------------------------------

db_all <- db_all %>%
  mutate(
    texto_busca = paste(
      ifelse(is.na(title), "", title),
      ifelse(is.na(abstract), "", abstract),
      ifelse(is.na(keywords), "", keywords),
      sep = " "
    ),
    tem_populacao   = grepl(bloco_populacao,   texto_busca, ignore.case = TRUE),
    tem_intervencao = grepl(bloco_intervencao, texto_busca, ignore.case = TRUE),
    tem_desfecho    = grepl(bloco_desfecho,    texto_busca, ignore.case = TRUE),
    relevante       = tem_populacao & (tem_intervencao | tem_desfecho)
  )

db_relevante <- db_all %>% filter(relevante)
cat("Registros potencialmente relevantes:", nrow(db_relevante), "\n")

# Registros nao-relevantes (para inspecao)
db_excluidos <- db_all %>% filter(!relevante)
cat("Registros excluidos na triagem automatica:", nrow(db_excluidos), "\n")

# ---------------------------------------------------------------
# 5. Exportar para triagem manual (titulo + resumo)
# ---------------------------------------------------------------

db_triagem <- db_relevante %>%
  select(source_db, eid, doi, title, authors, journal, year,
         abstract, keywords, doc_type, citations) %>%
  mutate(
    decisao_rev1    = NA_character_,
    decisao_rev2    = NA_character_,
    motivo_exclusao = NA_character_
  )

writexl::write_xlsx(db_triagem,
                    file.path(DIR_DADOS, "triagem_titulos_resumos.xlsx"))

cat("Planilha de triagem exportada:", nrow(db_triagem), "registros\n")

# Exportar tambem os excluidos para auditoria
writexl::write_xlsx(db_excluidos,
                    file.path(DIR_DADOS, "excluidos_triagem_automatica.xlsx"))

# ---------------------------------------------------------------
# 6. Concordancia interavaliadores (kappa de Cohen)
# ---------------------------------------------------------------

# Apos preenchimento manual das colunas decisao_rev1 e decisao_rev2:
# triagem <- readxl::read_excel(file.path(DIR_DADOS, "triagem_titulos_resumos.xlsx"))
# kappa_result <- irr::kappa2(triagem[, c("decisao_rev1", "decisao_rev2")])
# cat("Kappa de Cohen:", round(kappa_result$value, 3), "\n")

# ---------------------------------------------------------------
# 7. Contagens PRISMA
# ---------------------------------------------------------------

prisma_counts <- list(
  identificados_scopus   = 193,
  identificados_wos      = 172,
  total_bruto            = 365,
  apos_filtro_doctype    = 332,
  apos_filtro_temporal   = 310,
  apos_deduplicacao      = nrow(db_all),
  triados_titulo_resumo  = nrow(db_relevante),
  excluidos_automatico   = nrow(db_excluidos),
  texto_completo         = NA,
  incluidos_sintese      = NA
)

cat("\n--- Contagens PRISMA ---\n")
for (nm in names(prisma_counts)) {
  cat(sprintf("  %-25s %s\n", nm, as.character(prisma_counts[[nm]])))
}

# Salvar contagens para uso posterior
saveRDS(prisma_counts, file.path(DIR_OUTPUT, "prisma_counts.rds"))
cat("\nContagens PRISMA salvas em:", file.path(DIR_OUTPUT, "prisma_counts.rds"), "\n")

# Dataset: Biocultural Vulnerability Meta-Analysis

## Description

This dataset supports the article **"Vulnerability of traditional agricultural knowledge systems: a meta-analytical approach"** and contains all data and analysis scripts necessary to reproduce the meta-analytical results.

## Contents

### 1-DATABASE/
- **bd_extracao_convertido.xlsx** — Extraction database with coded variables aligned to the V1–V8 architecture, including tier classification and effect sizes.
- **bd_codificacao_qualitativa.xlsx** — Qualitative coding of studies classified as Tier 3–4, including ordinal conversion parameters.
- **PRISMA_artigo2.csv** — PRISMA 2020 flow diagram data (identification, screening, eligibility, inclusion counts).
- **consolidado_final.bib** — BibTeX file with all references included in the systematic review.

### 2-SCRIPTS/
R scripts numbered sequentially to reproduce the full analytical pipeline:
- **00_setup.R** — Package installation and environment configuration.
- **01_revisao_sistematica.R** — Systematic review search strategy and screening.
- **02_extracao_dados.R** — Data extraction and lnRR calculation.
- **02b_integrar_evidencia_mista.R** — Integration of mixed evidence (quantitative + qualitative tiers).
- **03_meta_analise_dimensao.R** — Random-effects meta-analysis by dimension (V1–V8).
- **03b_modelo_bayesiano_brms.R** — Bayesian meta-analysis (sensitivity check).
- **04_meta_regressao.R** — Meta-regression with geographic, community, and intervention moderators.
- **05_vies_sensibilidade.R** — Publication bias (Egger, Begg, trim-and-fill) and sensitivity analyses (tier, rho, DL vs. REML).
- **06_forest_plots.R** — Forest plots and leave-one-out diagnostics.
- **07_outputs_ISB.R** — Composite safeguard index outputs.
- **10_gerar_prisma.R** — PRISMA flow diagram generation.
- **30_preparar_codificacao_quali.R** — Preparation of qualitative coding sheets.
- **31_converter_quali_para_lnRR.R** — Conversion of qualitative evidence to lnRR with variance inflation.
- **32_graficos_complementares.R** — Supplementary figures.

### 3-RESULTS/
- **resultados_por_dimensao.xlsx** — Summary meta-analytic results per dimension (lnRR, CI, I², p-value).
- **coeficientes_meta_regressao.xlsx** — Meta-regression coefficients and model fit statistics.
- **leave_one_out.xlsx** — Leave-one-out sensitivity analysis results.
- **sensibilidade_tier.xlsx** — Sensitivity to tier-specific variance inflation.
- **sensibilidade_rho.xlsx** — Sensitivity to assumed correlation (rho).
- **sensibilidade_DL_REML.xlsx** — Comparison of DerSimonian–Laird vs. REML estimators.
- **vies_publicacao.xlsx** — Publication bias diagnostics (Egger, Begg, trim-and-fill).
- **subgrupos.xlsx** — Subgroup analyses by region and community type.
- **moderadores_significativos.xlsx** — Statistically significant moderators from meta-regression.
- **ranking_lnRR.xlsx** — Dimensional vulnerability ranking.
- **trimfill.xlsx** — Trim-and-fill adjusted estimates.

## Software

Analyses were conducted in R (version 4.3+) using the packages `metafor`, `dmetar`, `brms`, `ggplot2`, among others. See `00_setup.R` for the full list.

## License

CC BY 4.0

## Citation

If you use this dataset, please cite the associated article.

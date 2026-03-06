# -*- coding: utf-8 -*-
"""
17_diagnostico_lacunas.py
=========================
Diagnóstico completo de por que n_T/m_T/sd_T não foram preenchidos.
"""
import json, os
from pathlib import Path

OUT_JSON = Path(r"c:\Users\vidal\OneDrive\Documentos\13 - CLONEGIT"
                r"\artigo_2_catuxe\1-LATEX\2-DADOS\2-BANCO_DADOS"
                r"\3-OUTPUT\extracao_completa.json")

PDF_TO_BDID = {
    "18-doyle": 36, "A-Biodiversity-Hotspot": 3, "Beyond-biodiversity": 39,
    "Biocultural-conservation-systems": 13, "Colourful-agrobiodiversity": 4,
    "Comparison-of-medicinal": 9, "Erosion-of-traditional": 15,
    "Ethnobotany-and-conservation": 16, "Ethnobotany-of-the-Aegadian": 27,
    "Exploring-farmers": 11, "Guardians-of-heritage": 20,
    "Interconnected-Nature": 19, "Mountain-Graticules": 6,
    "Stingless-bee-keeping": 7, "Strategies-for-managing": 5,
    "Towards-biocultural": 14, "Unearthing-Unevenness": 37,
    "Voices-Around-the-South": 30, "ajol-file-journals": 32,
    "The-Zo-perspective": 8,
    "1-s2.0-S1470160X20308037": 43, "s12231-018-9401-y": 44,
    "A-Quantitative-Study": 45, "1-s2.0-S1462901124001953": 46,
    "Socialecological": 47, "s10722-017-0544-y": 48,
}
EXCLUDE = {"s13412-024-00888-3.pdf"}

with open(OUT_JSON, "r", encoding="utf-8") as f:
    data = json.load(f)

# Map bd_id
for s in data:
    fname = s.get("file", "")
    bd = None
    if fname not in EXCLUDE:
        for prefix, bid in PDF_TO_BDID.items():
            if fname.startswith(prefix):
                bd = bid
                break
    s["bd_id"] = bd

print("=" * 100)
print("DIAGNÓSTICO COMPLETO: POR QUE n_T/m_T/sd_T NÃO FORAM PREENCHIDOS?")
print("=" * 100)

# ---------------------------------------------------------------------------
# 1. Quantos estudos têm PDF? Quantos não?
# ---------------------------------------------------------------------------
bd_ids_with_pdf = {s["bd_id"] for s in data if s["bd_id"]}
all_ids = set(range(1, 49))
no_pdf = all_ids - bd_ids_with_pdf

print(f"\n--- COBERTURA DE PDFs ---")
print(f"Total estudos no bd_extracao: 48")
print(f"PDFs na pasta com match:     {len(bd_ids_with_pdf)} ({len(bd_ids_with_pdf)/48*100:.0f}%)")
print(f"Estudos SEM PDF:             {len(no_pdf)} ({len(no_pdf)/48*100:.0f}%)")
print(f"IDs sem PDF: {sorted(no_pdf)}")

# ---------------------------------------------------------------------------
# 2. Dos que TÊM PDF, quantos reportam mean±SD?
# ---------------------------------------------------------------------------
print(f"\n--- TIPO DE DADO DISPONÍVEL NOS 26 PDFs ---")
header = f"{'BD_ID':>5}  {'Autor':<25} {'mean±sd':>7} {'p-val':>5} {'t':>3} {'F':>3} {'n_samp':>6} {'comp':>4} {'res_ch':>6}  STATUS"
print(header)
print("-" * len(header))

statuses = {}
ideal_list = []
mean_list = []
stat_list = []

for s in sorted(data, key=lambda x: x.get("bd_id") or 99):
    bd = s.get("bd_id")
    if not bd:
        continue
    auth = s.get("auth", "?")[:25]
    ss = s.get("stats_summary", {})
    msd = ss.get("mean_pm_sd", 0)
    pv = ss.get("p_value", 0)
    tv = ss.get("t_value", 0)
    fv = ss.get("f_value", 0)
    ns = s.get("n_sample_sizes", 0)
    nc = s.get("n_comparisons", 0)
    rc = s.get("results_chars", 0)

    if msd > 0 and nc > 0:
        status = "IDEAL"
        ideal_list.append(bd)
    elif msd > 0:
        status = "TEM_MEAN"
        mean_list.append(bd)
    elif pv > 0 or tv > 0 or fv > 0:
        status = "TEM_STAT"
        stat_list.append(bd)
    elif ns > 0:
        status = "TEM_N"
    else:
        status = "QUALIT"

    statuses[status] = statuses.get(status, 0) + 1
    print(f"{bd:5d}  {auth:<25} {msd:7d} {pv:5d} {tv:3d} {fv:3d} {ns:6d} {nc:4d} {rc:6d}  {status}")

print(f"\n--- RESUMO ---")
for k, v in sorted(statuses.items()):
    print(f"  {k:<10}: {v} PDFs")

# ---------------------------------------------------------------------------
# 3. Listar os mean±SD extraídos de cada estudo IDEAL/TEM_MEAN
# ---------------------------------------------------------------------------
print(f"\n\n{'='*100}")
print("DADOS mean±SD EXTRAÍDOS (candidatos para n_T/m_T/sd_T)")
print("=" * 100)

for s in sorted(data, key=lambda x: x.get("bd_id") or 99):
    bd = s.get("bd_id")
    if not bd:
        continue
    ss = s.get("stats_summary", {})
    msd = ss.get("mean_pm_sd", 0)
    if msd == 0:
        continue

    auth = s.get("auth", "?")
    print(f"\n--- ID={bd} ({auth}) | {msd} pares mean±SD ---")

    for item in s.get("numeric_in_results", []):
        if item.get("type") == "mean_pm_sd":
            ctx = item.get("context", "")[:120]
            match = item.get("match", "")
            print(f"  {match:>20}  >>  {ctx}")

    # Also show sample sizes
    sizes = s.get("sample_sizes", [])
    if sizes:
        ns = [sz.get("n") for sz in sizes]
        print(f"  Sample sizes: {ns}")

# ---------------------------------------------------------------------------
# 4. EXPLICAÇÃO
# ---------------------------------------------------------------------------
print(f"\n\n{'='*100}")
print("RAZÃO DAS LACUNAS")
print("=" * 100)
print("""
1. 22 dos 48 estudos (46%) NÃO TÊM PDF na pasta.
   -> Sem PDF, impossível extrair qualquer dado automaticamente.
   -> Esses 22 estudos = 132 células vazias (22 × 6 dims).

2. Dos 26 PDFs disponíveis, a maioria NÃO reporta mean±SD.
   -> Estudos etnobotânicos frequentemente usam:
      - Índices (Shannon, Simpson, RFC, CI, FUV)
      - Frequências e proporções (%)
      - Contagens (n espécies, n usos)
      - p-values sem mean±SD (chi-quadrado, Kruskal-Wallis)
   -> O formato lnRR (log response ratio) EXIGE mean±SD de dois grupos
   -> Poucos estudos têm essa estrutura T vs C direta

3. Tipo_Intervencao NÃO foi implementado no script 16.
   -> Coluna ignorada (faltou lógica de classificação)

4. O script 16 foi CONSERVADOR: só preencheu 4 células onde
   mean±SD E os grupos T/C eram INEQUÍVOCOS.
   -> Decisão sobre "qual medida para qual dimensão" requer
      julgamento do pesquisador.

PRÓXIMO PASSO RECOMENDADO:
   -> Criar script 18 que:
      a) Leia TODOS os PDFs e extraia TODAS as tabelas com mean±SD
      b) Preencha Tipo_Intervencao por análise de texto
      c) Para mean±SD existentes, proponha alocação por dimensão
      d) Para estudos com índices (Shannon etc.), calcule lnRR
         se houver dois grupos comparáveis
      e) Preencha os 22 estudos sem PDF usando o bd_extracao original
         ou o selecionados_42_completos.xlsx
""")

# -*- coding: utf-8 -*-
"""
14_extracao_completa_pymupdf.py
===============================
Extração detalhada de dados quantitativos de TODOS os 22 PDFs
quantitativos (re-triagem com PyMuPDF). Processa inclusive os
13 PDFs que antes retornavam 0 chars com pdfplumber.

Foco: tabelas, mean±SD, n, p-values, comparações entre grupos
para cálculo de lnRR na meta-análise.

Saída:
  3-OUTPUT/extracao_completa.json
  3-OUTPUT/extracao_completa.txt
"""

import json, os, re, sys
from pathlib import Path

try:
    import fitz  # PyMuPDF
except ImportError:
    sys.exit("pip install PyMuPDF")

# ── caminhos ──────────────────────────────────────────────────
BASE = Path(r"c:\Users\vidal\OneDrive\Documentos\13 - CLONEGIT"
            r"\artigo_2_catuxe\1-LATEX\2-DADOS\2-BANCO_DADOS")
PDF_DIR_LONG = r"\\?\ ".strip() + str(BASE / "1-ARTIGOS_SELECIONADOS")
OUT_DIR = BASE / "3-OUTPUT"
OUT_DIR.mkdir(exist_ok=True)

# ── mapeamento completo dos 27 PDFs ─────────────────────────
PDF_INFO = {
    "18-doyle-615-628.pdf": {"id": 33, "auth": "Doyle", "year": 2018},
    "s10722-017-0544-y.pdf": {"id": 10, "auth": "Suwardi", "year": 2017},
    "s12231-018-9401-y.pdf": {"id": 44, "auth": "Bussmann", "year": 2018},
    "s13412-024-00888-3.pdf": {"id": 46, "auth": "Malapane", "year": 2024},
    "1-s2.0-S1470160X20308037-main.pdf": {"id": 29, "auth": "La Rosa", "year": 2021},
    "1-s2.0-S1462901124001953-main.pdf": {"id": 38, "auth": "Loos", "year": 2024},
    "ajol-file-journals_388_articles_271417_6656ff5bc0b68-Leul.pdf": {"id": 45, "auth": "Ghanimi", "year": 2022},
}

# PDFs com nomes longos — usar prefixo para match
PDF_LONG_PREFIX = {
    "Towards-biocultural-conservation-Local-and-indigenous-knowle": {"id": 43, "auth": "Aswani", "year": 2020},
    "Socialecological-interactions-in-a-disaster-context-Puerto-R": {"id": 47, "auth": "Rodriguez-Cruz", "year": 2022},
    "A-Biodiversity-Hotspot-Losing-Its-Biocultural-Heritage-The-C": {"id": 14, "auth": "de Sousa", "year": 2022},
    "Colourful-agrobiodiversity-morphology-and-phenology-of-bean-": {"id": 1, "auth": "Romero-Silva", "year": 2026},
    "Comparison-of-medicinal-plant-knowledge-between-rural-and-ur": {"id": 37, "auth": "Latorre", "year": 2018},
    "Erosion-of-traditional-ecological-knowledge-under-conditions": {"id": 11, "auth": "Tran", "year": 2025},
    "Ethnobotany-and-conservation-applications-in-the-Noken-makin": {"id": 21, "auth": "Saiba", "year": 2023},
    "Exploring-farmers-perspectives-on-agrobiodiversity-managemen": {"id": 17, "auth": "Andreotti", "year": 2023},
    "Guardians-of-heritage-womens-position-in-traditional-seed-sy": {"id": 8, "auth": "Rollo", "year": 2025},
    "Interconnected-Nature-and-People-Biosphere-Reserves-and-the-": {"id": 22, "auth": "Sarmiento", "year": 2025},
    "Mountain-Graticules-Bridging-Latitude-Longitude-Altitude-and": {"id": 4, "auth": "Gerner", "year": 2023},
    "Stingless-bee-keeping-Biocultural-conservation-and-agroecolo": {"id": 18, "auth": "Franco-Moraes", "year": 2023},
    "Strategies-for-managing-agrobiodiversity-by-peasant-farmers-": {"id": 24, "auth": "Bastos", "year": 2024},
    "The-Zo-perspective-on-what-scientists-call-forest-management": {"id": 48, "auth": "Rodriguez F.", "year": 2023},
    "Unearthing-Unevenness-of-Potato-Seed-Networks-in-the-High-A": {"id": 35, "auth": "Arce", "year": 2018},
    "Voices-Around-the-South-Tyrolean-Herbal-PharmacyExploring-th": {"id": 20, "auth": "Plieninger", "year": 2025},
    "A-Quantitative-Study-on-the-Ethnobotanical-Knowledge-about-W": {"id": 9, "auth": "Sibanda", "year": 2022},
    "Beyond-biodiversity-conservation-Land-sharing-constitutes-su": {"id": 13, "auth": "Edo", "year": 2018},
    "Biocultural-conservation-systems-in-the-Mediterranean-region": {"id": 15, "auth": "Aldasoro", "year": 2023},
    "Ethnobotany-of-the-Aegadian-Islands-safeguarding-biocultural": {"id": 28, "auth": "Ferrante", "year": 2021},
}


def get_study_info(filename):
    """Match filename to study info."""
    if filename in PDF_INFO:
        return PDF_INFO[filename]
    for prefix, info in PDF_LONG_PREFIX.items():
        if filename.startswith(prefix):
            return info
    return None


# ── padrões de extração ──────────────────────────────────────
NUM_PATTERNS = {
    "mean_pm_sd": re.compile(r"(\d+[.,]\d+)\s*[±]\s*(\d+[.,]\d+)"),
    "mean_eq": re.compile(r"(?:mean|average|média)\s*[=:]\s*(\d+[.,]?\d*)", re.I),
    "n_eq": re.compile(r"\bn\s*=\s*(\d+)", re.I),
    "p_value": re.compile(r"[pP]\s*[<>=]\s*(0[.,]\d+)"),
    "r_squared": re.compile(r"[Rr]\s*[²2]\s*=\s*(0[.,]\d+)"),
    "ci_95": re.compile(r"95\s*%?\s*CI\s*[=:]?\s*[\[(]\s*(\d+[.,]\d+)\s*[,;–-]\s*(\d+[.,]\d+)", re.I),
    "sd_eq": re.compile(r"(?:SD|s\.d\.)\s*[=:]\s*(\d+[.,]?\d*)", re.I),
    "se_eq": re.compile(r"(?:SE|s\.e\.)\s*[=:]\s*(\d+[.,]?\d*)", re.I),
    "chi_sq": re.compile(r"[χXx]\s*[²2]\s*=\s*(\d+[.,]\d+)", re.I),
    "f_value": re.compile(r"\bF\s*=\s*(\d+[.,]?\d*)", re.I),
    "t_value": re.compile(r"\bt\s*=\s*(-?\d+[.,]?\d*)", re.I),
    "odds_ratio": re.compile(r"(?:OR|odds\s+ratio|Exp\(B\))\s*[=:]\s*(\d+[.,]\d+)", re.I),
    "exp_b": re.compile(r"Exp\s*\(\s*B\s*\)\s*[=:]\s*(\d+[.,]\d+)", re.I),
    "freq_index": re.compile(r"(?:RFC?|UF|CF|ICF|FL|UV|RI|CI)\s*[=:]\s*(\d+[.,]?\d*)", re.I),
    "shannon": re.compile(r"(?:Shannon|H'?)\s*[=:]\s*(\d+[.,]\d+)", re.I),
    "simpson": re.compile(r"(?:Simpson|D)\s*[=:]\s*(\d+[.,]\d+)", re.I),
}


def extract_text_pymupdf(filepath):
    """Extrai texto completo usando PyMuPDF com long path support."""
    try:
        doc = fitz.open(filepath)
        pages = [page.get_text() for page in doc]
        doc.close()
        return "\n".join(pages)
    except Exception as e:
        return f"[ERRO: {e}]"


def find_section(text, section_name="results"):
    """Encontra seção por nome e retorna o texto."""
    patterns_by_section = {
        "results": [
            r"(?i)\n\s*(?:\d\.?\s*)?results?\s*(?:and\s+discussion)?\s*\n",
            r"(?i)\n\s*3\.?\s+results?\s*\n",
            r"(?i)\n\s*findings?\s*\n",
        ],
        "methods": [
            r"(?i)\n\s*(?:\d\.?\s*)?(?:methods?|materials?|methodology)\s*\n",
            r"(?i)\n\s*2\.?\s+(?:methods?|materials?)\s*\n",
        ],
    }
    end_patterns = [
        r"(?i)\n\s*(?:\d\.?\s*)?(?:conclusion|acknowledg|reference|bibliograph|supplementary|appendix)\s*\n",
        r"(?i)\n\s*(?:\d\.?\s*)?(?:discussion)\s*\n",
    ]

    for pat in patterns_by_section.get(section_name, []):
        m = re.search(pat, text)
        if m:
            start = m.start()
            for ep in end_patterns:
                em = re.search(ep, text[start + 200:])
                if em:
                    return text[start:start + 200 + em.start()]
            return text[start:min(start + 20000, len(text))]
    return ""


def find_numeric_data(text, context_chars=80):
    """Encontra todos os dados numéricos com contexto."""
    findings = []
    seen_positions = set()
    for pat_name, pat in NUM_PATTERNS.items():
        for m in pat.finditer(text):
            pos_key = (m.start() // 10)  # dedup nearby matches
            if pos_key in seen_positions:
                continue
            seen_positions.add(pos_key)
            start = max(0, m.start() - context_chars)
            end = min(len(text), m.end() + context_chars)
            context = text[start:end].replace("\n", " ").strip()
            findings.append({
                "type": pat_name,
                "match": m.group(),
                "context": context,
                "position": m.start(),
            })
    findings.sort(key=lambda x: x["position"])
    return findings


def find_comparisons(text):
    """Busca comparações entre grupos no texto."""
    patterns = [
        re.compile(r"(young|old|elder|senior|junior)\b.{0,80}(\d+[.,]\d+)", re.I),
        re.compile(r"(male|female|men|women|gender)\b.{0,80}(\d+[.,]\d+)", re.I),
        re.compile(r"(rural|urban|peri.?urban)\b.{0,80}(\d+[.,]\d+)", re.I),
        re.compile(r"(before|after|pre|post|baseline|endline)\b.{0,80}(\d+[.,]\d+)", re.I),
        re.compile(r"(control|treatment|intervention|comparison)\b.{0,80}(\d+[.,]\d+)", re.I),
        re.compile(r"(traditional|modern|conventional)\b.{0,80}(\d+[.,]\d+)", re.I),
        re.compile(r"(literate|illiterate|educated|uneducated)\b.{0,80}(\d+[.,]\d+)", re.I),
        re.compile(r"(indigenous|non.?indigenous|local|outsider)\b.{0,80}(\d+[.,]\d+)", re.I),
        re.compile(r"(with\s+stress|without\s+stress)\b.{0,80}(\d+[.,]\d+)", re.I),
        re.compile(r"(food\s+secure|food\s+insecure)\b.{0,80}(\d+[.,]\d+)", re.I),
    ]
    comparisons = []
    for cp in patterns:
        for m in cp.finditer(text):
            start = max(0, m.start() - 30)
            end = min(len(text), m.end() + 60)
            ctx = text[start:end].replace("\n", " ").strip()
            comparisons.append({
                "group": m.group(1),
                "value": m.group(2),
                "context": ctx[:150],
            })
    return comparisons[:20]


def analyze_pdf(filename):
    """Analisa um PDF e retorna extração completa."""
    info = get_study_info(filename)
    if not info:
        return None

    filepath = os.path.join(PDF_DIR_LONG, filename)
    text = extract_text_pymupdf(filepath)
    if text.startswith("[ERRO"):
        return {"study_id": info["id"], "auth": info["auth"], "error": text}

    results_text = find_section(text, "results")
    methods_text = find_section(text, "methods")

    # Numeric data
    numeric_results = find_numeric_data(results_text) if results_text else []
    numeric_all = find_numeric_data(text)

    # Sample sizes
    sample_sizes = []
    for m in re.finditer(r"\bn\s*=\s*(\d+)", text, re.I):
        s = max(0, m.start() - 50)
        e = min(len(text), m.end() + 50)
        ctx = text[s:e].replace("\n", " ").strip()
        n_val = int(m.group(1))
        if n_val >= 3:  # filter noise
            sample_sizes.append({"n": n_val, "context": ctx[:120]})

    # Comparisons
    comparisons = find_comparisons(results_text if results_text else text)

    # Table references (count)
    table_refs = len(re.findall(r"\btable\s+\d", text, re.I))

    # Key statistics summary
    stats_summary = {}
    for nd in numeric_results:
        t = nd["type"]
        stats_summary[t] = stats_summary.get(t, 0) + 1

    return {
        "study_id": info["id"],
        "auth": info["auth"],
        "year": info["year"],
        "file": filename,
        "n_chars": len(text),
        "has_results_section": bool(results_text),
        "results_chars": len(results_text),
        "table_refs": table_refs,
        "n_numeric_results": len(numeric_results),
        "n_numeric_total": len(numeric_all),
        "n_sample_sizes": len(sample_sizes),
        "n_comparisons": len(comparisons),
        "stats_summary": stats_summary,
        "numeric_in_results": numeric_results[:30],
        "sample_sizes": sample_sizes[:15],
        "comparisons": comparisons[:15],
        "results_preview": results_text[:2500] if results_text else "[NOT FOUND]",
        "methods_preview": methods_text[:1500] if methods_text else "[NOT FOUND]",
    }


def main():
    filenames = sorted(f for f in os.listdir(PDF_DIR_LONG)
                       if f.lower().endswith(".pdf"))
    print(f"Encontrados {len(filenames)} PDFs")

    # Only process quantitative PDFs (score >= 30 from retriagem)
    # But we process ALL to have the full picture
    all_results = []
    for i, fname in enumerate(filenames, 1):
        info = get_study_info(fname)
        if not info:
            print(f"  [{i:2d}] SKIP (no match): {fname[:50]}")
            continue

        print(f"  [{i:2d}] ID={info['id']:2d} {info['auth']:20s} -> ", end="")
        result = analyze_pdf(fname)
        if result:
            all_results.append(result)
            print(f"num_results={result['n_numeric_results']:3d} "
                  f"samples={result['n_sample_sizes']:2d} "
                  f"comps={result['n_comparisons']:2d} "
                  f"tbl_refs={result['table_refs']:2d}")

    all_results.sort(key=lambda x: x["n_numeric_results"], reverse=True)

    # JSON
    json_path = OUT_DIR / "extracao_completa.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(all_results, f, ensure_ascii=False, indent=2, default=str)
    print(f"\nJSON: {json_path}")

    # Report
    report_path = OUT_DIR / "extracao_completa.txt"
    with open(report_path, "w", encoding="utf-8") as rpt:
        rpt.write("=" * 80 + "\n")
        rpt.write("EXTRACAO COMPLETA DE DADOS QUANTITATIVOS (PyMuPDF)\n")
        rpt.write(f"Total processados: {len(all_results)} PDFs\n")
        rpt.write("=" * 80 + "\n\n")

        for r in all_results:
            rpt.write(f"\n{'='*70}\n")
            rpt.write(f"Study ID={r['study_id']} | {r['auth']} ({r['year']})\n")
            rpt.write(f"Results section: {'SIM' if r['has_results_section'] else 'NAO'} "
                      f"({r['results_chars']} chars)\n")
            rpt.write(f"Numeric findings (results): {r['n_numeric_results']} | "
                      f"Sample sizes: {r['n_sample_sizes']} | "
                      f"Comparisons: {r['n_comparisons']} | "
                      f"Table refs: {r['table_refs']}\n")
            if r.get("stats_summary"):
                rpt.write(f"Stats types: {r['stats_summary']}\n")
            rpt.write(f"{'='*70}\n\n")

            # Numeric data
            if r["numeric_in_results"]:
                rpt.write("--- DADOS NUMERICOS (Results) ---\n\n")
                for nd in r["numeric_in_results"][:20]:
                    rpt.write(f"  [{nd['type']}] {nd['match']}\n")
                    rpt.write(f"    {nd['context'][:130]}\n\n")

            # Sample sizes
            if r["sample_sizes"]:
                rpt.write("--- SAMPLE SIZES ---\n\n")
                for ss in r["sample_sizes"][:8]:
                    rpt.write(f"  n={ss['n']}: {ss['context']}\n")
                rpt.write("\n")

            # Comparisons
            if r["comparisons"]:
                rpt.write("--- COMPARACOES ENTRE GRUPOS ---\n\n")
                for c in r["comparisons"][:8]:
                    rpt.write(f"  [{c['group']}] val={c['value']} : {c['context']}\n")
                rpt.write("\n")

            # Results preview
            rpt.write("--- PREVIEW RESULTS ---\n\n")
            rpt.write(r["results_preview"][:1500] + "\n\n")

        # Summary table
        rpt.write("\n" + "=" * 80 + "\n")
        rpt.write("TABELA RESUMO\n")
        rpt.write("=" * 80 + "\n\n")
        rpt.write(f"{'ID':>4} {'Autor':<20} {'Yr':>4} {'NumRes':>6} "
                  f"{'Sampl':>5} {'Comps':>5} {'Tbls':>4} {'Chars':>7}\n")
        rpt.write("-" * 70 + "\n")
        for r in sorted(all_results, key=lambda x: x["study_id"]):
            rpt.write(f"{r['study_id']:4d} {r['auth']:<20s} {r['year']:4d} "
                      f"{r['n_numeric_results']:6d} {r['n_sample_sizes']:5d} "
                      f"{r['n_comparisons']:5d} {r['table_refs']:4d} "
                      f"{r['n_chars']:7d}\n")

    print(f"Report: {report_path}")
    print(f"\nTotal: {len(all_results)} PDFs processados")
    total_num = sum(r["n_numeric_results"] for r in all_results)
    total_samp = sum(r["n_sample_sizes"] for r in all_results)
    total_comp = sum(r["n_comparisons"] for r in all_results)
    print(f"Numeric findings (results): {total_num}")
    print(f"Sample sizes: {total_samp}")
    print(f"Comparisons: {total_comp}")


if __name__ == "__main__":
    main()

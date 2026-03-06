# -*- coding: utf-8 -*-
"""
13_retriagem_pymupdf.py
=======================
Re-triagem de TODOS os 27 PDFs usando PyMuPDF (fitz) em vez de pdfplumber.
PyMuPDF extrai texto inclusive de PDFs com texto renderizado em layers,
que pdfplumber não conseguia ler (13 PDFs retornaram 0 chars antes).

Usa prefixo \\?\ para contornar o limite MAX_PATH do Windows (260 chars).

Saída:
  3-OUTPUT/retriagem_pymupdf.json  (dados completos)
  3-OUTPUT/retriagem_pymupdf.txt   (relatório legível)
"""

import json, os, re, sys
from pathlib import Path

try:
    import fitz  # PyMuPDF
except ImportError:
    sys.exit("PyMuPDF não instalado. Execute: pip install PyMuPDF")

# ── caminhos (com prefixo \\?\ para long paths) ──────────────
BASE    = Path(r"c:\Users\vidal\OneDrive\Documentos\13 - CLONEGIT"
               r"\artigo_2_catuxe\1-LATEX\2-DADOS\2-BANCO_DADOS")
PDF_DIR = str(BASE / "1-ARTIGOS_SELECIONADOS")
# Prefixo para long path support no Windows
PDF_DIR_LONG = r"\\?\ ".strip() + PDF_DIR  # \\?\C:\...
OUT_DIR = BASE / "3-OUTPUT"
OUT_DIR.mkdir(exist_ok=True)

# ── PDF → Study_ID mapping ───────────────────────────────────
# Mapeamento completo dos 27 PDFs para Study_IDs
PDF_STUDY_MAP = {
    "18-doyle-615-628.pdf": 33,
    "s10722-017-0544-y.pdf": 10,  # Suwardi
    "s12231-018-9401-y.pdf": 44,  # Bussmann
    "s13412-024-00888-3.pdf": 46, # Malapane (systematic review!)
    "1-s2.0-S1470160X20308037-main.pdf": 29,  # La Rosa
    "1-s2.0-S1462901124001953-main.pdf": 38,  # Loos
    "ajol-file-journals_388_articles_271417_6656ff5bc0b68-Leul.pdf": 45,  # Ghanimi
    "Towards-biocultural-conservation-Local-and-indigenous-knowle": 43,   # Aswani
    "Socialecological-interactions-in-a-disaster-context-Puerto-R": 47,   # Rodríguez-Cruz
    "A-Biodiversity-Hotspot-Losing-Its-Biocultural-Heritage-The-C": 14,  # de Sousa
    "Colourful-agrobiodiversity-morphology-and-phenology-of-bean-": 1,   # Romero-Silva
    "Comparison-of-medicinal-plant-knowledge-between-rural-and-ur": 37,  # Latorre
    "Erosion-of-traditional-ecological-knowledge-under-conditions": 11,  # Tran
    "Ethnobotany-and-conservation-applications-in-the-Noken-makin": 21,  # Saiba
    "Exploring-farmers-perspectives-on-agrobiodiversity-managemen": 17,  # Andreotti? 
    "Guardians-of-heritage-womens-position-in-traditional-seed-sy": 8,   # Rollo
    "Interconnected-Nature-and-People-Biosphere-Reserves-and-the-": 22,  # Sarmiento
    "Mountain-Graticules-Bridging-Latitude-Longitude-Altitude-and": 4,   # Gerner
    "Stingless-bee-keeping-Biocultural-conservation-and-agroecolo": 18,  # Franco-Moraes
    "Strategies-for-managing-agrobiodiversity-by-peasant-farmers-": 24,  # Bastos
    "The-Zo-perspective-on-what-scientists-call-forest-management": 48,  # Rodríguez 2018? 
    "Unearthing-Unevenness-of-Potato-Seed-Networks-in-the-High-A": 35,  # Arce
    "Voices-Around-the-South-Tyrolean-Herbal-PharmacyExploring-th": 20,  # Plieninger
    "A-Quantitative-Study-on-the-Ethnobotanical-Knowledge-about-W": 9,  # Sibanda? 
    "Beyond-biodiversity-conservation-Land-sharing-constitutes-su": 13,  # Edo
    "Biocultural-conservation-systems-in-the-Mediterranean-region": 15,  # Aldasoro
    "Ethnobotany-of-the-Aegadian-Islands-safeguarding-biocultural": 28,  # Ferrante?
}


def match_study_id(filename):
    """Match a PDF filename to its Study_ID using the map."""
    # Try exact match first
    if filename in PDF_STUDY_MAP:
        return PDF_STUDY_MAP[filename]
    # Try prefix match (for long filenames)
    for prefix, sid in PDF_STUDY_MAP.items():
        if filename.startswith(prefix):
            return sid
    return None


# ── palavras-chave para detectar conteúdo quantitativo ────────
QUANT_KEYWORDS = re.compile(
    r"\b(mean|average|median|std\.?\s*dev|standard\s+deviation|"
    r"s\.?d\.?\s*[=±]|s\.?e\.?\s*[=±]|n\s*=\s*\d|sample\s+size|"
    r"p\s*[<>=]\s*0[.,]\d|anova|t-test|chi-square|regression|"
    r"mann.?whitney|kruskal|wilcoxon|logistic|odds\s+ratio|"
    r"confidence\s+interval|95\s*%?\s*ci|effect\s+size|"
    r"species\s+richness|shannon|simpson|diversity\s+index|"
    r"frequency|proportion|percentage|prevalence|incidence|"
    r"likert|score|index|coefficient|r\s*[²2]\s*=|r²|"
    r"β\s*=|exp\s*\(b\)|hazard|relative\s+risk|"
    r"before.{0,30}after|control.{0,30}intervention|"
    r"treatment\s+group|comparison\s+group|"
    r"baseline|endline|pre.?intervention|post.?intervention|"
    r"use\s+value|cultural\s+importance|"
    r"informant\s+consensus|fidelity\s+level|"
    r"ethnobotanical|citation\s+frequency|"
    r"relative\s+frequency|use\s+report|"
    r"taxonomic\s+distinctness|"
    r"food\s+insecurity|household\s+survey|"
    r"questionnaire|respondent|interview)",
    re.IGNORECASE
)

TABLE_KEYWORDS = re.compile(
    r"\b(table\s+\d|tab\.\s*\d|tabela\s+\d|appendix\s+table)",
    re.IGNORECASE
)

NUMERIC_PATTERN = re.compile(
    r"(\d+[.,]\d+)\s*[±]\s*(\d+[.,]\d+)"
    r"|mean\s*[=:]\s*(\d+[.,]?\d*)"
    r"|n\s*=\s*(\d+)"
    r"|(\d+[.,]\d+)\s*\(\s*(\d+[.,]\d+)\s*\)",
    re.IGNORECASE
)


def extract_text_pymupdf(pdf_path):
    """Extrai texto de um PDF usando PyMuPDF com suporte a long paths."""
    try:
        doc = fitz.open(pdf_path)
        pages_text = []
        for page in doc:
            pages_text.append(page.get_text())
        doc.close()
        return "\n".join(pages_text)
    except Exception as e:
        return f"[ERRO: {e}]"


def find_results_section(text):
    """Isola a seção Results/Discussion do texto."""
    patterns = [
        r"(?i)\n\s*(?:\d\.?\s*)?results?\s*(?:and\s+discussion)?\s*\n",
        r"(?i)\n\s*(?:\d\.?\s*)?resultados?\s*(?:e\s+discuss[ãa]o)?\s*\n",
        r"(?i)\n\s*3\.?\s+results?\s*\n",
        r"(?i)\n\s*findings?\s*\n",
    ]
    for pat in patterns:
        m = re.search(pat, text)
        if m:
            start = m.start()
            end_m = re.search(
                r"(?i)\n\s*(?:\d\.?\s*)?(?:conclusion|acknowledg|reference|bibliograph|supplementary)\s*\n",
                text[start + 100:]
            )
            end_pos = start + 100 + end_m.start() if end_m else min(start + 15000, len(text))
            return text[start:end_pos]
    return ""


def analyze_pdf(filename, text):
    """Analisa texto extraído e retorna métricas de quantitatividade."""
    if text.startswith("[ERRO"):
        return {
            "file": filename, "error": text,
            "is_quantitative": False, "score": 0,
        }

    quant_matches = QUANT_KEYWORDS.findall(text)
    table_matches = TABLE_KEYWORDS.findall(text)
    numeric_matches = NUMERIC_PATTERN.findall(text)

    results_section = find_results_section(text)
    results_quant = QUANT_KEYWORDS.findall(results_section) if results_section else []
    results_numeric = NUMERIC_PATTERN.findall(results_section) if results_section else []

    score = (
        len(quant_matches) * 1
        + len(table_matches) * 3
        + len(numeric_matches) * 2
        + len(results_quant) * 2
        + len(results_numeric) * 3
    )

    # Numeric excerpts from results section
    numeric_in_results = []
    if results_section:
        for m in NUMERIC_PATTERN.finditer(results_section):
            cs = max(0, m.start() - 60)
            ce = min(len(results_section), m.end() + 60)
            numeric_in_results.append(results_section[cs:ce].strip())

    study_id = match_study_id(filename)

    return {
        "file": filename,
        "study_id": study_id,
        "n_chars": len(text),
        "quant_keyword_count": len(quant_matches),
        "table_ref_count": len(table_matches),
        "numeric_pattern_count": len(numeric_matches),
        "results_quant_keywords": len(results_quant),
        "results_numeric_count": len(results_numeric),
        "score": score,
        "is_quantitative": score >= 30,
        "results_preview": (results_section[:800] if results_section
                            else "[seção não localizada]"),
        "numeric_excerpts": numeric_in_results[:25],
    }


def main():
    # List PDFs using long path
    filenames = sorted(f for f in os.listdir(PDF_DIR_LONG)
                       if f.lower().endswith(".pdf"))
    print(f"Encontrados {len(filenames)} PDFs")
    print(f"Extraindo texto com PyMuPDF...\n")

    results = []
    for i, fname in enumerate(filenames, 1):
        fpath = os.path.join(PDF_DIR_LONG, fname)
        text = extract_text_pymupdf(fpath)
        analysis = analyze_pdf(fname, text)
        results.append(analysis)

        tag = "QUANTI" if analysis["is_quantitative"] else "quali "
        sid = f"ID={analysis['study_id']:2d}" if analysis["study_id"] else "ID=??"
        print(f"  [{i:2d}/{len(filenames)}] {sid} score={analysis['score']:4d} "
              f"[{tag}] {fname[:55]}")

    results.sort(key=lambda x: x["score"], reverse=True)

    # JSON
    json_path = OUT_DIR / "retriagem_pymupdf.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2, default=str)
    print(f"\nJSON: {json_path}")

    # Relatório legível
    quanti = [r for r in results if r["is_quantitative"]]
    quali  = [r for r in results if not r["is_quantitative"]]

    report_path = OUT_DIR / "retriagem_pymupdf.txt"
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("=" * 80 + "\n")
        f.write("RE-TRIAGEM DE PDFs COM PyMuPDF (corrige 13 PDFs com 0 chars)\n")
        f.write(f"Total: {len(results)} | Quantitativos: {len(quanti)} | "
                f"Qualitativos: {len(quali)}\n")
        f.write("=" * 80 + "\n\n")

        f.write("QUANTITATIVOS (score >= 30)\n\n")
        for r in quanti:
            sid = f"Study_ID={r['study_id']}" if r["study_id"] else "ID=??"
            f.write(f"  {sid}  score={r['score']}  "
                    f"kw={r['quant_keyword_count']}  "
                    f"tbl={r['table_ref_count']}  "
                    f"num={r['numeric_pattern_count']}\n")
            f.write(f"  {r['file'][:75]}\n")
            if r.get("numeric_excerpts"):
                f.write(f"  Exemplos numericos na secao Results:\n")
                for ex in r["numeric_excerpts"][:8]:
                    clean = ex.replace("\n", " ")[:120]
                    f.write(f"    | {clean}\n")
            f.write("\n")

        f.write("\nQUALITATIVOS (score < 30)\n\n")
        for r in quali:
            sid = f"ID={r['study_id']}" if r["study_id"] else "ID=??"
            f.write(f"  {sid:>6}  score={r['score']:3d}  {r['file'][:65]}\n")

    print(f"Relatório: {report_path}")
    print(f"\nResumo: {len(quanti)} QUANTI / {len(quali)} quali")


if __name__ == "__main__":
    main()

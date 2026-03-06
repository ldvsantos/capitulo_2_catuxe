# -*- coding: utf-8 -*-
"""
11_extrair_pdfs.py
==================
Extrai texto de todos os PDFs em 1-ARTIGOS_SELECIONADOS,
identifica seções de resultados/tabelas e gera relatório
de dados quantitativos candidatos para meta-análise (lnRR).

Saída: 3-OUTPUT/pdf_extractions.json  (texto + flags quanti)
       3-OUTPUT/triagem_quantitativos.txt (resumo legível)
"""

import json, os, re, sys
from pathlib import Path

try:
    import pdfplumber
except ImportError:
    sys.exit("pdfplumber não instalado. Execute: pip install pdfplumber")

# ── caminhos ──────────────────────────────────────────────────
BASE   = Path(r"c:\Users\vidal\OneDrive\Documentos\13 - CLONEGIT\artigo_2_catuxe\1-LATEX\2-DADOS\2-BANCO_DADOS")
PDF_DIR = BASE / "1-ARTIGOS_SELECIONADOS"
OUT_DIR = BASE / "3-OUTPUT"
OUT_DIR.mkdir(exist_ok=True)

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

# Padrões numéricos: "12.3 ± 4.5", "mean = 23.1 (SD 5.2)", etc.
NUMERIC_PATTERN = re.compile(
    r"(\d+[.,]\d+)\s*[±]\s*(\d+[.,]\d+)"  # valor ± desvio
    r"|mean\s*[=:]\s*(\d+[.,]?\d*)"         # mean = X
    r"|n\s*=\s*(\d+)"                        # n = X
    r"|(\d+[.,]\d+)\s*\(\s*(\d+[.,]\d+)\s*\)",  # X (Y) 
    re.IGNORECASE
)


def extract_pdf_text(pdf_path):
    """Extrai texto completo de um PDF via pdfplumber."""
    pages_text = []
    tables_raw = []
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for i, page in enumerate(pdf.pages):
                txt = page.extract_text() or ""
                pages_text.append(txt)
                # Tentar extrair tabelas
                try:
                    tbls = page.extract_tables()
                    for t in tbls:
                        tables_raw.append({
                            "page": i + 1,
                            "rows": len(t),
                            "data": t[:15]  # primeiras 15 linhas
                        })
                except Exception:
                    pass
    except Exception as e:
        return {"error": str(e), "text": "", "tables": []}
    
    full_text = "\n".join(pages_text)
    return {"text": full_text, "tables": tables_raw}


def find_results_section(text):
    """Tenta isolar a seção Results/Discussion do texto."""
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
            # Tentar achar fim (Conclusion, References, etc.)
            end_m = re.search(
                r"(?i)\n\s*(?:\d\.?\s*)?(?:conclusion|acknowledg|reference|bibliograph|supplementary)\s*\n",
                text[start + 100:]
            )
            end_pos = start + 100 + end_m.start() if end_m else min(start + 15000, len(text))
            return text[start:end_pos]
    return ""


def analyze_pdf(pdf_path):
    """Analisa um PDF e retorna métricas de 'quantitatividade'."""
    fname = pdf_path.name
    extraction = extract_pdf_text(pdf_path)
    
    if "error" in extraction and extraction["error"]:
        return {
            "file": fname,
            "error": extraction["error"],
            "is_quantitative": False,
            "score": 0,
        }
    
    text = extraction["text"]
    n_pages = text.count("\n\n") // 3 + 1  # rough estimate
    
    # Contagem de keywords quantitativos
    quant_matches = QUANT_KEYWORDS.findall(text)
    table_matches = TABLE_KEYWORDS.findall(text)
    numeric_matches = NUMERIC_PATTERN.findall(text)
    
    # Seção de resultados
    results_section = find_results_section(text)
    results_quant = QUANT_KEYWORDS.findall(results_section) if results_section else []
    results_numeric = NUMERIC_PATTERN.findall(results_section) if results_section else []
    
    # Score de quantitatividade
    score = (
        len(quant_matches) * 1
        + len(table_matches) * 3
        + len(numeric_matches) * 2
        + len(results_quant) * 2
        + len(results_numeric) * 3
        + len(extraction["tables"]) * 5
    )
    
    # Extrair primeiras 500 chars da seção de resultados para review
    results_preview = results_section[:800] if results_section else "[seção não localizada]"
    
    # Extrair todos os padrões numéricos da seção de resultados
    numeric_in_results = []
    if results_section:
        for m in NUMERIC_PATTERN.finditer(results_section):
            context_start = max(0, m.start() - 50)
            context_end = min(len(results_section), m.end() + 50)
            numeric_in_results.append(results_section[context_start:context_end].strip())
    
    return {
        "file": fname,
        "n_chars": len(text),
        "n_tables_extracted": len(extraction["tables"]),
        "quant_keyword_count": len(quant_matches),
        "table_ref_count": len(table_matches),
        "numeric_pattern_count": len(numeric_matches),
        "results_quant_keywords": len(results_quant),
        "results_numeric_count": len(results_numeric),
        "score": score,
        "is_quantitative": score >= 30,  # threshold
        "results_preview": results_preview,
        "numeric_excerpts": numeric_in_results[:20],
        "tables_preview": extraction["tables"][:5],
    }


def main():
    pdfs = sorted(PDF_DIR.glob("*.pdf"))
    print(f"Encontrados {len(pdfs)} PDFs em {PDF_DIR}")
    
    results = []
    for i, pdf_path in enumerate(pdfs, 1):
        print(f"  [{i:2d}/{len(pdfs)}] {pdf_path.name[:70]}...")
        analysis = analyze_pdf(pdf_path)
        results.append(analysis)
        tag = "QUANTI" if analysis["is_quantitative"] else "quali"
        print(f"         -> score={analysis['score']:4d}  [{tag}]  "
              f"tables={analysis.get('n_tables_extracted',0)}  "
              f"quant_kw={analysis.get('quant_keyword_count',0)}  "
              f"numeric={analysis.get('numeric_pattern_count',0)}")
    
    # Ordenar por score (desc)
    results.sort(key=lambda x: x["score"], reverse=True)
    
    # Salvar JSON completo
    json_path = OUT_DIR / "pdf_extractions.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2, default=str)
    print(f"\nJSON salvo: {json_path}")
    
    # Relatório legível
    report_path = OUT_DIR / "triagem_quantitativos.txt"
    quanti = [r for r in results if r["is_quantitative"]]
    quali = [r for r in results if not r["is_quantitative"]]
    
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("=" * 80 + "\n")
        f.write("TRIAGEM AUTOMÁTICA DE PDFs — CANDIDATOS QUANTITATIVOS\n")
        f.write(f"Total: {len(results)} PDFs | Quantitativos: {len(quanti)} | Qualitativos: {len(quali)}\n")
        f.write("=" * 80 + "\n\n")
        
        f.write("──── QUANTITATIVOS (score >= 30) ────\n\n")
        for r in quanti:
            f.write(f"📊 {r['file'][:70]}\n")
            f.write(f"   Score: {r['score']} | Tables: {r.get('n_tables_extracted',0)} | "
                    f"Quant KW: {r.get('quant_keyword_count',0)} | "
                    f"Numeric: {r.get('numeric_pattern_count',0)}\n")
            if r.get("numeric_excerpts"):
                f.write(f"   Exemplos numéricos:\n")
                for ex in r["numeric_excerpts"][:5]:
                    f.write(f"     • {ex}\n")
            f.write("\n")
        
        f.write("\n──── QUALITATIVOS (score < 30) ────\n\n")
        for r in quali:
            f.write(f"   {r['file'][:70]}  (score={r['score']})\n")
        
    print(f"Relatório salvo: {report_path}")
    print(f"\nResumo: {len(quanti)} quantitativos / {len(quali)} qualitativos")


if __name__ == "__main__":
    main()

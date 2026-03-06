# -*- coding: utf-8 -*-
"""
12_extrair_dados_quantitativos.py
=================================
Extrai dados quantitativos detalhados dos PDFs quantitativos
identificados, com foco em tabelas, médias, desvios-padrão,
tamanhos amostrais e comparações entre grupos (T vs C) para
cálculo de lnRR na meta-análise.

Saída principal:
  3-OUTPUT/extracao_quantitativos.json  — dados estruturados
  3-OUTPUT/extracao_quantitativos.txt   — relatório legível
"""

import json, re, sys
from pathlib import Path

try:
    import pdfplumber
except ImportError:
    sys.exit("pdfplumber não instalado")

# ── mapeamento completo (PDF → Study_ID) ─────────────────────
PDF_MAP = {
    "ajol-file-journals_388_articles_271417_6656ff5bc0b68-Leul.pdf": {
        "id": 13, "auth": "Edo, K; Kidane, L; Beyene, T", "year": 2024,
        "doi": "10.4314/mejs.v16i1.6",
        "title": "Socio-ecological Benefit of Homegarden Agroforestry"
    },
    "s10722-017-0544-y.pdf": {
        "id": 48, "auth": "Rodríguez F.", "year": 2018,
        "doi": "10.1007/s10722-017-0544-y",
        "title": "Ahipa on-farm conservation temporal comparison"
    },
    "Guardians-of-heritage-womens-position-in-traditional-seed-systems-and-agroecology-in-Zimbabwe_2025_BioMed-Central-Ltd.pdf": {
        "id": 9, "auth": "Sibanda M.", "year": 2025,
        "doi": "10.1186/s40066-025-00573-w",
        "title": "Guardians of heritage: women's position in traditional seed systems"
    },
    "A-Quantitative-Study-on-the-Ethnobotanical-Knowledge-about-Wild-Edible-Plants-among-the-Population-of-Messiwa_2022_NLM-Medline.pdf": {
        "id": 45, "auth": "Ghanimi H.M.A.", "year": 2022,
        "doi": "10.4314/ejhs.v32i6.22",
        "title": "Ethnobotanical Knowledge about Wild Edible Plants Messiwa"
    },
    "1-s2.0-S1470160X20308037-main.pdf": {
        "id": None, "auth": "???", "year": 2020,
        "doi": "10.1016/j.ecolind.2020.106865",
        "title": "UNKNOWN - Ecological Indicators 2020 (verificar se pertence aos 48)"
    },
    "s13412-024-00888-3.pdf": {
        "id": 46, "auth": "Malapane O.L.", "year": 2024,
        "doi": "10.1007/s13412-024-00888-3",
        "title": "Farm Trees as Cultural Keystone Species"
    },
    "1-s2.0-S1462901124001953-main.pdf": {
        "id": 10, "auth": "Suwardi A.B.", "year": 2025,
        "doi": "10.1016/j.ecofro.2025.10.014",
        "title": "Ecological functions, ecosystem services, and biocultural significance"
    },
    "s12231-018-9401-y.pdf": {
        "id": 44, "auth": "Bussmann R.W.", "year": 2018,
        "doi": "10.1007/s12231-018-9401-y",
        "title": "Chácobo ethnobotany - complete adult population survey"
    },
    "Ethnobotany-of-the-Aegadian-Islands-safeguarding-biocultural-refugia-in-the-Mediterranean_2021_BioMed-Central-Ltd.pdf": {
        "id": 29, "auth": "La Rosa A.", "year": 2021,
        "doi": "10.1186/s13002-021-00470-z",
        "title": "Ethnobotany of the Aegadian Islands"
    },
}

# PDFs de imagem (sem texto) — estudos que precisam extração manual
IMAGE_PDFS = {
    "A-Biodiversity-Hotspot-Losing-Its-Biocultural-Heritage-The-Challenge-to-Biocultural-Conservation-of-Brazilwood-Paubrasilia-echinata_2022_Frontiers-Media-SA.pdf": {
        "id": 24, "auth": "Bastos J.G.", "year": 2022
    },
    "Colourful-agrobiodiversity-morphology-and-phenology-of-bean-landraces-to-face-commodification-of-the-commons-in-the-southern-Andes_2026_Springer-Science-and-Business-Media-Deutschland-GmbH.pdf": {
        "id": 1, "auth": "Romero-Silva M.J.", "year": 2026
    },
    "Comparison-of-medicinal-plant-knowledge-between-rural-and-urban-people-living-in-the-Biosphere-Reserve-Bioma-PampaQuebradas-del-Norte-Uruguay-An-opportunity-for-biocultural-conservation_2018_Universidade-Federal-Ru.pdf": {
        "id": 37, "auth": "Latorre E.C.", "year": 2018
    },
    "Erosion-of-traditional-ecological-knowledge-under-conditions-of-hydrosocial-rupture-Insights-from-the-Mekong-floodplains-communities_2025_Springer-Science-and-Business-Media-BV.pdf": {
        "id": 11, "auth": "Tran T.A.", "year": 2025
    },
    "Ethnobotany-and-conservation-applications-in-the-Noken-making-by-the-Sougb-Tribe-of-West-Papua-Indonesia_2023_Society-for-Indonesian-Biodiversity.pdf": {
        "id": 21, "auth": "Saiba Y.", "year": 2023
    },
    "Exploring-farmers-perspectives-on-agrobiodiversity-management-future-options-for-quinoa-smallholder-organizations-in-the-Peruvian-high-Andes_2023_SpringerVerlag-Italia-srl.pdf": {
        "id": 17, "auth": "Andreotti F.", "year": 2023
    },
    "Interconnected-Nature-and-People-Biosphere-Reserves-and-the-Power-of-Memory-and-Oral-Histories-as-Biocultural-Heritage-for-a-Sustainable-Future_2025_Multidisciplinary-Digital-Publishing-Institute-MDPI.pdf": {
        "id": 8, "auth": "Rollo M.F.", "year": 2025
    },
    "Mountain-Graticules-Bridging-Latitude-Longitude-Altitude-and-Historicity-to-Biocultural-Heritage_2023_Multidisciplinary-Digital-Publishing-Institute-MDPI.pdf": {
        "id": 22, "auth": "Sarmiento F.O.", "year": 2023
    },
    "Socialecological-interactions-in-a-disaster-context-Puerto-Rican-farmer-households-food-security-after-Hurricane-Maria_2022_IOP-Publishing-Ltd.pdf": {
        "id": 47, "auth": "Rodríguez-Cruz L.A.", "year": 2022
    },
    "Strategies-for-managing-agrobiodiversity-by-peasant-farmers-in-the-CerradoCaatinga-ecotone-Southwest-Piau-Brazil_2024_Universidade-de-Brasilia.pdf": {
        "id": 14, "auth": "de Sousa T.B.", "year": 2024
    },
    "The-Zo-perspective-on-what-scientists-call-forest-management-and-its-implications-for-floristic-diversity-and-biocultural-conservation_2023_Resilience-Alliance.pdf": {
        "id": 18, "auth": "Franco-Moraes J.", "year": 2023
    },
    "Unearthing-Unevenness-of-Potato-Seed-Networks-in-the-High-Andes-A-Comparison-of-Distinct-Cultivar-Groups-and-Farmer-Types-Following-Seasons-With-and-Without-Acute-Stress_2018_Frontiers-Media-SA-infofrontiersinorg.pdf": {
        "id": 35, "auth": "Arce, A; de Haan, S", "year": 2018
    },
    "Voices-Around-the-South-Tyrolean-Herbal-PharmacyExploring-the-Stakeholder-Landscape-and-Perspectives-on-Medicinal-Plants-as-Culturally-Salient-Species_2025_SAGE-Publications-Ltd.pdf": {
        "id": 4, "auth": "Gerner, IR", "year": 2025
    },
}

# ── caminhos ──────────────────────────────────────────────────
BASE    = Path(r"c:\Users\vidal\OneDrive\Documentos\13 - CLONEGIT\artigo_2_catuxe\1-LATEX\2-DADOS\2-BANCO_DADOS")
PDF_DIR = BASE / "1-ARTIGOS_SELECIONADOS"
OUT_DIR = BASE / "3-OUTPUT"

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
    "percent": re.compile(r"(\d+[.,]\d+)\s*%"),
    "chi_sq": re.compile(r"[χXx]\s*[²2]\s*=\s*(\d+[.,]\d+)", re.I),
    "f_value": re.compile(r"\bF\s*[\(=]\s*(\d+[.,]?\d*)", re.I),
    "t_value": re.compile(r"\bt\s*[\(=]\s*(-?\d+[.,]?\d*)", re.I),
    "freq_index": re.compile(r"(?:RFC?|UF|CF|ICF|FL|UV|RI|CI)\s*[=:]\s*(\d+[.,]?\d*)", re.I),
}

SECTION_PATTERNS = {
    "results": re.compile(r"\n\s*(?:\d\.?\s*)?results?\b", re.I),
    "discussion": re.compile(r"\n\s*(?:\d\.?\s*)?discussion\b", re.I),
    "methods": re.compile(r"\n\s*(?:\d\.?\s*)?(?:methods?|materials?|methodology)\b", re.I),
    "conclusion": re.compile(r"\n\s*(?:\d\.?\s*)?(?:conclusion|acknowledg|reference)\b", re.I),
}


def extract_sections(text):
    """Segmenta o texto em seções por headers."""
    sections = {}
    positions = []
    for name, pat in SECTION_PATTERNS.items():
        m = pat.search(text)
        if m:
            positions.append((m.start(), name))
    positions.sort()
    
    for i, (pos, name) in enumerate(positions):
        end = positions[i + 1][0] if i + 1 < len(positions) else len(text)
        sections[name] = text[pos:end]
    
    return sections


def extract_tables_detailed(pdf_path):
    """Extrai todas as tabelas do PDF com contexto."""
    tables = []
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for i, page in enumerate(pdf.pages):
                try:
                    page_tables = page.extract_tables()
                    for j, tbl in enumerate(page_tables):
                        if tbl and len(tbl) > 1:
                            tables.append({
                                "page": i + 1,
                                "table_idx": j,
                                "n_rows": len(tbl),
                                "n_cols": max(len(r) for r in tbl) if tbl else 0,
                                "header": tbl[0] if tbl else [],
                                "data": tbl[1:20],  # up to 20 data rows
                            })
                except Exception:
                    pass
    except Exception as e:
        return [{"error": str(e)}]
    return tables


def extract_full_text(pdf_path):
    """Extrai texto completo do PDF."""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            pages = []
            for page in pdf.pages:
                pages.append(page.extract_text() or "")
            return "\n".join(pages)
    except Exception as e:
        return f"[ERROR: {e}]"


def find_numeric_data(text, context_chars=80):
    """Encontra todos os dados numéricos com contexto."""
    findings = []
    for pat_name, pat in NUM_PATTERNS.items():
        for m in pat.finditer(text):
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


def analyze_quantitative_pdf(pdf_path, study_info):
    """Análise completa de um PDF quantitativo."""
    fname = pdf_path.name
    sid = study_info["id"]
    auth = study_info["auth"]
    year = study_info["year"]
    
    print(f"\n{'='*70}")
    print(f"PROCESSANDO: ID={sid} {auth} ({year})")
    print(f"  Arquivo: {fname[:60]}")
    print(f"{'='*70}")
    
    # 1. Extrair texto completo
    full_text = extract_full_text(pdf_path)
    if full_text.startswith("[ERROR"):
        return {"error": full_text, "study_id": sid}
    
    # 2. Segmentar em seções
    sections = extract_sections(full_text)
    results_text = sections.get("results", "")
    methods_text = sections.get("methods", "")
    
    # 3. Extrair tabelas
    tables = extract_tables_detailed(pdf_path)
    
    # 4. Encontrar dados numéricos na seção de resultados
    numeric_results = find_numeric_data(results_text) if results_text else []
    numeric_all = find_numeric_data(full_text)
    
    # 5. Buscar menções a sample size
    sample_sizes = []
    for m in re.finditer(r"\bn\s*=\s*(\d+)", full_text, re.I):
        start = max(0, m.start() - 60)
        end = min(len(full_text), m.end() + 60)
        ctx = full_text[start:end].replace("\n", " ").strip()
        sample_sizes.append({"n": int(m.group(1)), "context": ctx})
    
    # 6. Buscar comparações entre grupos
    comparison_patterns = [
        re.compile(r"(young|old|elder|senior|junior)\b.{0,60}(mean|average|%|frequency)", re.I),
        re.compile(r"(male|female|men|women|gender)\b.{0,60}(mean|average|%|frequency|know)", re.I),
        re.compile(r"(rural|urban|peri.?urban)\b.{0,60}(mean|average|%|frequency|know)", re.I),
        re.compile(r"(before|after|pre|post|baseline|endline)\b.{0,60}(mean|average|%)", re.I),
        re.compile(r"(control|treatment|intervention|comparison)\b.{0,60}(mean|average|group)", re.I),
        re.compile(r"(traditional|modern|conventional)\b.{0,60}(mean|average|%|know)", re.I),
        re.compile(r"(literate|illiterate|educated|uneducated)\b.{0,60}(mean|average|%)", re.I),
    ]
    comparisons = []
    for cp in comparison_patterns:
        for m in cp.finditer(full_text):
            start = max(0, m.start() - 40)
            end = min(len(full_text), m.end() + 80)
            ctx = full_text[start:end].replace("\n", " ").strip()
            comparisons.append(ctx)
    
    result = {
        "study_id": sid,
        "auth": auth,
        "year": year,
        "doi": study_info.get("doi", ""),
        "title": study_info.get("title", ""),
        "file": fname,
        "text_length": len(full_text),
        "has_results_section": bool(results_text),
        "results_section_length": len(results_text),
        "n_tables": len(tables),
        "tables": tables,
        "n_numeric_findings_results": len(numeric_results),
        "n_numeric_findings_total": len(numeric_all),
        "numeric_in_results": numeric_results[:40],
        "sample_sizes": sample_sizes[:15],
        "group_comparisons": comparisons[:15],
        "results_preview": results_text[:2000] if results_text else "[NOT FOUND]",
        "methods_preview": methods_text[:1500] if methods_text else "[NOT FOUND]",
    }
    
    # Print summary
    print(f"  Texto: {len(full_text)} chars")
    print(f"  Seção Results: {'SIM' if results_text else 'NÃO'} ({len(results_text)} chars)")
    print(f"  Tabelas: {len(tables)}")
    print(f"  Dados numéricos (results): {len(numeric_results)}")
    print(f"  Sample sizes encontrados: {len(sample_sizes)}")
    print(f"  Comparações entre grupos: {len(comparisons)}")
    
    if tables:
        print(f"  Tabelas extraídas:")
        for t in tables[:5]:
            h = t.get("header", [])
            print(f"    p.{t['page']}: {t['n_rows']}×{t['n_cols']} header={[str(c)[:20] for c in (h or [])[:6]]}")
    
    if sample_sizes:
        print(f"  Sample sizes:")
        for ss in sample_sizes[:5]:
            print(f"    n={ss['n']}: {ss['context'][:80]}")
    
    if comparisons:
        print(f"  Comparações:")
        for c in comparisons[:5]:
            print(f"    {c[:90]}")
    
    return result


def main():
    print("=" * 70)
    print("EXTRAÇÃO DE DADOS QUANTITATIVOS DOS PDFs")
    print("=" * 70)
    
    all_results = []
    quant_pdfs = {k: v for k, v in PDF_MAP.items() if v.get("id") is not None}
    
    for fname, study_info in quant_pdfs.items():
        pdf_path = PDF_DIR / fname
        if not pdf_path.exists():
            print(f"\n⚠ ARQUIVO NÃO ENCONTRADO: {fname}")
            continue
        
        result = analyze_quantitative_pdf(pdf_path, study_info)
        all_results.append(result)
    
    # Salvar JSON
    json_path = OUT_DIR / "extracao_quantitativos.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(all_results, f, ensure_ascii=False, indent=2, default=str)
    print(f"\n\nJSON detalhado: {json_path}")
    
    # Relatório legível
    report_path = OUT_DIR / "extracao_quantitativos.txt"
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("EXTRAÇÃO DETALHADA DE DADOS QUANTITATIVOS\n")
        f.write("=" * 70 + "\n\n")
        
        for r in all_results:
            f.write(f"\n{'='*70}\n")
            f.write(f"Study ID={r['study_id']} | {r['auth']} ({r['year']})\n")
            f.write(f"DOI: {r['doi']}\n")
            f.write(f"Title: {r['title']}\n")
            f.write(f"Tables: {r['n_tables']} | Numeric findings: {r['n_numeric_findings_results']}\n")
            f.write(f"{'='*70}\n\n")
            
            # Tables
            if r["tables"]:
                f.write("--- TABELAS EXTRAÍDAS ---\n\n")
                for t in r["tables"]:
                    if "error" in t:
                        continue
                    f.write(f"  Tabela p.{t['page']} ({t['n_rows']}×{t['n_cols']}):\n")
                    h = t.get("header", [])
                    if h:
                        f.write(f"    Header: {h}\n")
                    for row in t.get("data", [])[:10]:
                        f.write(f"    {row}\n")
                    f.write("\n")
            
            # Numeric data in results
            if r["numeric_in_results"]:
                f.write("--- DADOS NUMÉRICOS (seção Results) ---\n\n")
                for nd in r["numeric_in_results"][:25]:
                    f.write(f"  [{nd['type']}] {nd['match']}\n")
                    f.write(f"    ...{nd['context']}...\n\n")
            
            # Sample sizes
            if r["sample_sizes"]:
                f.write("--- TAMANHOS AMOSTRAIS ---\n\n")
                for ss in r["sample_sizes"][:10]:
                    f.write(f"  n={ss['n']}: {ss['context']}\n")
                f.write("\n")
            
            # Group comparisons
            if r["group_comparisons"]:
                f.write("--- COMPARAÇÕES ENTRE GRUPOS ---\n\n")
                for c in r["group_comparisons"][:10]:
                    f.write(f"  {c}\n")
                f.write("\n")
            
            # Results preview
            f.write("--- PREVIEW DA SEÇÃO RESULTS ---\n\n")
            f.write(r["results_preview"][:1500] + "\n\n")
        
        # Image PDFs
        f.write("\n" + "=" * 70 + "\n")
        f.write("PDFs SEM TEXTO (EXTRAÇÃO MANUAL NECESSÁRIA)\n")
        f.write("=" * 70 + "\n\n")
        for fname, info in IMAGE_PDFS.items():
            f.write(f"  ID={info['id']:2d} {info['auth']:30s} ({info['year']}) | {fname[:55]}\n")
    
    print(f"Relatório legível: {report_path}")
    
    # Summary
    print(f"\n{'='*70}")
    print(f"RESUMO FINAL")
    print(f"{'='*70}")
    print(f"PDFs quantitativos processados: {len(all_results)}")
    total_tables = sum(r["n_tables"] for r in all_results)
    total_numeric = sum(r["n_numeric_findings_results"] for r in all_results)
    print(f"Total de tabelas extraídas: {total_tables}")
    print(f"Total de dados numéricos (results): {total_numeric}")
    print(f"PDFs de imagem (OCR necessário): {len(IMAGE_PDFS)}")


if __name__ == "__main__":
    main()

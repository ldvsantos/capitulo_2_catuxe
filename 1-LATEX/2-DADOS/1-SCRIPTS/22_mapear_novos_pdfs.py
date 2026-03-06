# -*- coding: utf-8 -*-
"""
22_mapear_novos_pdfs.py
=======================
Mapeia TODOS os 40 PDFs na pasta aos Study_IDs do bd_extracao,
identificando os 13 novos e os que ainda faltam.
"""
import openpyxl, shutil, tempfile, sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

TAB = Path(r"c:\Users\vidal\OneDrive\Documentos\13 - CLONEGIT"
           r"\artigo_2_catuxe\1-LATEX\2-DADOS\2-BANCO_DADOS\2-DADOS_TABULADOS")
PDF_DIR = Path(r"c:\Users\vidal\OneDrive\Documentos\13 - CLONEGIT"
               r"\artigo_2_catuxe\1-LATEX\2-DADOS\2-BANCO_DADOS\1-ARTIGOS_SELECIONADOS")

# === Mapeamento ORIGINAL (26 PDFs já mapeados) ===
OLD_MAP = {
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

# === Mapeamento dos 13 NOVOS PDFs ===
# Baseado nos DOIs da busca anterior:
# ID=1  Gonçalves   DOI 10.2993/0278-0771-42.2.241         -> NÃO BAIXADO
# ID=2  Calvet-Mir  DOI 10.1080/08941920.2015.1094711      -> calvet-mir2015.pdf
# ID=10 Mobarak     DOI 10.1659/mrd.2024.00024              -> mrd.2024.00024.pdf
# ID=12 Suwardi     DOI 10.1016/j.ecofro.2025.10.014       -> 1-s2.0-S2665972725003484-main.pdf
# ID=17 Vázquez     DOI 10.1016/j.heliyon.2022.e09805      -> 1-s2.0-S2405844022010933-main.pdf
# ID=18 Nord        DOI 10.1002/ldr.3582                    -> Land Degrad Dev - 2020 - Nord
# ID=21 Tabe-Ojong  DOI 10.1002/ldr.4569                    -> Land Degrad Dev - 2022 - Tabe-Ojong
# ID=22 Aniah       DOI 10.1016/j.heliyon.2019.e01492      -> 1-s2.0-S2405844019311880-main.pdf
# ID=25 Alemayehu   DOI 10.1016/j.envdev.2023.100908       -> Farmers-traditional-knowledge
# ID=29 Fernández   DOI 10.1111/conl.12398                  -> Conservation Letters - 2017
# ID=31 Frascaroli  DOI 10.1007/s13280-015-0738-5           -> frascaroli2015.pdf
# ID=35 Mondal      DOI 10.2298/IJGI240802003M              -> 0350-75992500003M.pdf
# ID=38 García      DOI 10.1002/csc2.20620                  -> 10.1002@csc2.20620.pdf
# ID=41 Mugi-Ngenga DOI 10.1016/j.jrurstud.2015.11.004     -> mugi-ngenga2016.pdf
# Plus: s13412-024-00888-3.pdf was excluded before but could be a study

NEW_MAP = {
    "calvet-mir2015": 2,
    "mrd.2024.00024": 10,
    "1-s2.0-S2665972725003484": 12,
    "1-s2.0-S2405844022010933": 17,
    "Land Degrad Dev - 2020 - Nord": 18,
    "Land Degrad Dev - 2022 - Tabe": 21,
    "1-s2.0-S2405844019311880": 22,
    "Farmers-traditional-knowledge": 25,
    "Conservation Letters - 2017 - Fern": 29,
    "frascaroli2015": 31,
    "0350-75992500003M": 35,
    "10.1002@csc2.20620": 38,
    "mugi-ngenga2016": 41,
}

# Combine
FULL_MAP = {**OLD_MAP, **NEW_MAP}

# Listar todos os PDFs e mapear
pdfs = sorted(PDF_DIR.glob("*.pdf"))
print(f"Total PDFs na pasta: {len(pdfs)}")
print()

mapped_ids = set()
unmapped_pdfs = []

print("=" * 120)
print(f"{'ID':>3}  {'PDF (primeiros 80 chars)':<80}  STATUS")
print("-" * 120)

for pdf in pdfs:
    fname = pdf.stem  # nome sem .pdf
    bid = None
    for prefix, pid in FULL_MAP.items():
        if fname.startswith(prefix):
            bid = pid
            break
    
    if bid:
        mapped_ids.add(bid)
        is_new = any(fname.startswith(p) for p in NEW_MAP)
        status = "NOVO" if is_new else "existente"
        print(f"{bid:3d}  {fname[:80]:<80}  {status}")
    else:
        unmapped_pdfs.append(fname)
        print(f"  ?  {fname[:80]:<80}  NAO MAPEADO")

# IDs ainda sem PDF
all_ids = set(range(1, 49))
sem_pdf = sorted(all_ids - mapped_ids)

print(f"\nIDs mapeados: {len(mapped_ids)}/48")
print(f"IDs sem PDF: {sem_pdf} ({len(sem_pdf)} estudos)")
if unmapped_pdfs:
    print(f"PDFs não mapeados: {unmapped_pdfs}")

# Ler bd_extracao para mostrar detalhes dos que faltam
tmp = Path(tempfile.gettempdir()) / "bd_copy2.xlsx"
shutil.copy2(TAB / "bd_extracao.xlsx", tmp)
wb = openpyxl.load_workbook(tmp, read_only=True)
ws = wb.active
seen = set()
print(f"\n{'='*120}")
print("ESTUDOS SEM PDF (excluir da meta-análise)")
print("=" * 120)
for row in ws.iter_rows(min_row=2, values_only=True):
    vals = list(row)
    sid = vals[0]
    if sid in sem_pdf and sid not in seen:
        seen.add(sid)
        print(f"  ID={sid:3d}  {str(vals[1])[:30]:<30}  {str(vals[3])[:60]}")
wb.close()

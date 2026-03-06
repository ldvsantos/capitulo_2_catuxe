# ================================================================
# 09_integrar_wos_manual.py
# Integra dados exportados manualmente do Web of Science com a
# base Scopus existente (busca_consolidada_final.xlsx).
#
# PASSO A PASSO:
# 1. Acesse https://www.webofscience.com/wos/woscc/advanced-search
# 2. Cole a query gerada por este script (impressa no terminal)
# 3. Aplique os filtros de ano (2016–2026) e tipo (Article, Review)
# 4. Exporte TODOS os resultados em formato "Tab delimited"
#    (selecione "Full Record" para obter título, autores, abstract etc.)
#    O arquivo será salvo como "savedrecs.txt"
# 5. Coloque o arquivo na pasta 2-DADOS/2-BANCO_DADOS/
# 6. Execute este script:
#    python 09_integrar_wos_manual.py
#
# Dependências: pip install pandas openpyxl
# ================================================================

import sys
import re
import logging
from pathlib import Path
from datetime import datetime

import pandas as pd

# ---------------------------------------------------------------
# CONFIGURAÇÃO
# ---------------------------------------------------------------

DIR_BASE   = Path(__file__).resolve().parent.parent  # 2-DADOS/
DIR_DB     = DIR_BASE / "2-BANCO_DADOS"
DIR_BIB    = DIR_BASE / "3-BIB_EXPORTS"

# Arquivo Scopus existente
SCOPUS_FILE = DIR_DB / "busca_consolidada_final.xlsx"

# Arquivo WoS exportado manualmente (Tab delimited)
# O WoS geralmente salva como "savedrecs.txt"
# Coloque na pasta 2-BANCO_DADOS/ e renomeie se quiser
WOS_EXPORT_FILE = DIR_DB / "savedrecs.txt"

# Alternativas possíveis de nome
WOS_ALT_NAMES = [
    "savedrecs.txt",
    "wos_export.txt",
    "wos_manual.txt",
    "savedrecs.xls",
    "wos_export.xls",
    "savedrecs.csv",
]

# Tipos documentais aceitos (PICOS §2.3)
DOC_TYPES_ACEITOS = ["Article", "Review"]

# Janela temporal
ANO_INICIO = 2016
ANO_FIM    = 2026

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger(__name__)


# ---------------------------------------------------------------
# QUERY WoS (mesmos blocos semânticos do script 08)
# ---------------------------------------------------------------

BLOCO1_EN = [
    '"traditional agricultural system*"',
    '"traditional ecological knowledge"',
    '"indigenous farming"',
    '"quilombola"',
    '"smallholder"',
    '"agrobiodiversity"',
    '"agroecology"',
    '"traditional farming system*"',
    '"ethnobotanical knowledge"',
    '"local ecological knowledge"',
    '"biocultural heritage"',
    '"indigenous knowledge"',
    '"peasant agriculture"',
]
BLOCO2_EN = [
    "safeguard*",
    '"documentation"',
    '"heritage registration"',
    '"legal protection"',
    '"intangible heritage"',
    '"biocultural conservation"',
    '"community governance"',
    '"knowledge protection"',
    '"cultural heritage preservation"',
    '"community protocol*"',
    '"geographical indication"',
    '"patrimoni* register"',
]
BLOCO3_EN = [
    '"vulnerability"',
    '"erosion"',
    '"knowledge loss"',
    '"intergenerational transmission"',
    '"biodiversity index"',
    '"cultural complexity"',
    '"documentation status"',
    '"knowledge transmission"',
    '"biocultural diversity"',
    '"species richness"',
    '"ethnobotanical diversity"',
    '"social-ecological resilience"',
]

# Português
BLOCO1_PT = [
    '"sistema agrícola tradicional"',
    '"conhecimento ecológico tradicional"',
    '"agricultura indígena"',
    '"quilombola"',
    '"agricultura familiar"',
    '"agrobiodiversidade"',
    '"agroecologia"',
    '"saber tradicional"',
]
BLOCO2_PT = [
    '"salvaguarda"',
    '"documentação"',
    '"registro patrimonial"',
    '"proteção jurídica"',
    '"patrimônio imaterial"',
    '"conservação biocultural"',
    '"governança comunitária"',
    '"protocolo comunitário"',
]
BLOCO3_PT = [
    '"vulnerabilidade"',
    '"erosão"',
    '"perda de conhecimento"',
    '"transmissão intergeracional"',
    '"diversidade biocultural"',
    '"complexidade cultural"',
]

# Espanhol
BLOCO1_ES = [
    '"sistema agrícola tradicional"',
    '"conocimiento ecológico tradicional"',
    '"agricultura indígena"',
    '"agricultura campesina"',
    '"agrobiodiversidad"',
    '"agroecología"',
]
BLOCO2_ES = [
    '"salvaguardia"',
    '"documentación"',
    '"registro patrimonial"',
    '"protección jurídica"',
    '"patrimonio inmaterial"',
    '"conservación biocultural"',
    '"gobernanza comunitaria"',
]
BLOCO3_ES = [
    '"vulnerabilidad"',
    '"erosión"',
    '"pérdida de conocimiento"',
    '"transmisión intergeneracional"',
    '"diversidad biocultural"',
]


def build_wos_query() -> str:
    """Gera a query para WoS Advanced Search."""
    b1 = " OR ".join(BLOCO1_EN + BLOCO1_PT + BLOCO1_ES)
    b2 = " OR ".join(BLOCO2_EN + BLOCO2_PT + BLOCO2_ES)
    b3 = " OR ".join(BLOCO3_EN + BLOCO3_PT + BLOCO3_ES)
    return f"TS=(({b1}) AND ({b2}) AND ({b3}))"


def print_query():
    """Imprime a query e instruções para busca manual."""
    query = build_wos_query()

    print("\n" + "=" * 70)
    print("  QUERY PARA WEB OF SCIENCE — ADVANCED SEARCH")
    print("=" * 70)
    print()
    print("1. Acesse: https://www.webofscience.com/wos/woscc/advanced-search")
    print()
    print("2. Cole a query abaixo no campo de busca avançada:")
    print()
    print("-" * 70)
    print(query)
    print("-" * 70)
    print()
    print(f"3. Adicione filtro de período: {ANO_INICIO}–{ANO_FIM}")
    print("   (No WoS: Timespan > Custom year range > 2016 to 2026)")
    print()
    print("4. Na lista de resultados, clique em 'Export' (canto superior)")
    print("   - Formato: 'Tab delimited file'")
    print("   - Conteúdo: 'Full Record'")
    print("   - Registros: 'All records' (se < 1000)")
    print("     Se > 500, exporte em lotes de 500:")
    print("       Lote 1: Records 1 to 500   → savedrecs.txt")
    print("       Lote 2: Records 501 to 1000 → savedrecs (1).txt")
    print("       etc.")
    print()
    print(f"5. Coloque o(s) arquivo(s) em: {DIR_DB}")
    print()
    print("6. Re-execute este script para integrar com os dados Scopus.")
    print()

    # Salvar query em arquivo para referência
    query_file = DIR_DB / "wos_query_manual.txt"
    query_file.write_text(
        f"WoS Advanced Search Query\n"
        f"Gerada em: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
        f"Período: {ANO_INICIO}–{ANO_FIM}\n\n"
        f"{query}\n",
        encoding="utf-8"
    )
    print(f"Query salva em: {query_file}")
    print("=" * 70)

    return query


# ---------------------------------------------------------------
# LEITURA DO ARQUIVO WoS (Tab delimited)
# ---------------------------------------------------------------

def find_wos_files() -> list[Path]:
    """Procura arquivos WoS exportados na pasta."""
    found = []
    for name in WOS_ALT_NAMES:
        f = DIR_DB / name
        if f.exists():
            found.append(f)

    # Procurar também savedrecs (1).txt, savedrecs (2).txt etc.
    for f in DIR_DB.glob("savedrecs*.txt"):
        if f not in found:
            found.append(f)

    for f in DIR_DB.glob("wos*.txt"):
        if f not in found and "query" not in f.name.lower():
            found.append(f)

    return sorted(set(found))


def read_wos_tabdelimited(filepath: Path) -> pd.DataFrame:
    """
    Lê arquivo WoS em formato Tab delimited (Full Record).
    Colunas principais do WoS Tab delimited:
      PT  = Publication Type (J=Journal, B=Book, S=Series, P=Patent)
      AU  = Authors
      TI  = Title
      SO  = Source (Journal)
      DT  = Document Type
      DE  = Author Keywords
      ID  = Keywords Plus
      AB  = Abstract
      PY  = Publication Year
      VL  = Volume
      IS  = Issue
      BP  = Beginning Page
      EP  = Ending Page
      DI  = DOI
      UT  = Unique Tag (WoS Accession Number)
      TC  = Times Cited
      SN  = ISSN
      EI  = eISSN
    """
    log.info(f"Lendo arquivo WoS: {filepath}")

    # WoS Tab delimited começa com linhas BOM + header
    try:
        df = pd.read_csv(
            filepath,
            sep="\t",
            encoding="utf-8-sig",  # lida com BOM
            on_bad_lines="skip",
            dtype=str,
        )
    except Exception as e:
        log.warning(f"Falha UTF-8, tentando latin-1: {e}")
        df = pd.read_csv(
            filepath,
            sep="\t",
            encoding="latin-1",
            on_bad_lines="skip",
            dtype=str,
        )

    log.info(f"  Colunas encontradas: {list(df.columns)}")
    log.info(f"  Registros: {len(df)}")

    # Mapear para formato padronizado
    records = []
    for _, row in df.iterrows():
        records.append({
            "source_db":  "WoS",
            "uid":        str(row.get("UT", "")).strip(),
            "doi":        str(row.get("DI", "")).strip(),
            "issn":       str(row.get("SN", row.get("EI", ""))).strip(),
            "title":      str(row.get("TI", "")).strip(),
            "authors":    str(row.get("AU", "")).strip(),
            "journal":    str(row.get("SO", "")).strip(),
            "year":       str(row.get("PY", "")).strip()[:4],
            "volume":     str(row.get("VL", "")).strip(),
            "pages":      f"{row.get('BP', '')}-{row.get('EP', '')}".strip("-"),
            "abstract":   str(row.get("AB", "")).strip(),
            "keywords":   str(row.get("DE", "")).strip(),
            "keywords_plus": str(row.get("ID", "")).strip(),
            "citations":  str(row.get("TC", "0")).strip(),
            "doc_type":   str(row.get("DT", "")).strip(),
        })

    result = pd.DataFrame(records)

    # Limpar valores "nan" que vieram do pandas
    for col in result.columns:
        result[col] = result[col].replace("nan", "")

    return result


# ---------------------------------------------------------------
# FILTRO E DEDUPLICAÇÃO
# ---------------------------------------------------------------

def filtrar_tipo_documento(df: pd.DataFrame) -> pd.DataFrame:
    """Mantém registros cujo doc_type contenha 'Article' ou 'Review'.
    Isso inclui variantes do WoS como 'Article; Early Access',
    'Article; Book Chapter' etc., que são artigos válidos."""
    n_before = len(df)
    mask = df["doc_type"].str.contains("Article|Review", case=False, na=False)
    df_filtrado = df[mask].reset_index(drop=True)
    n_after = len(df_filtrado)
    removidos = n_before - n_after
    if removidos > 0:
        excluidos = df[~mask]["doc_type"].value_counts()
        log.info(f"Filtro doc_type WoS: {n_before} → {n_after} ({removidos} removidos)")
        for dt, c in excluidos.items():
            log.info(f"  Removido: {dt} ({c})")
    else:
        log.info(f"Filtro doc_type: todos os {n_before} registros são Article/Review.")
    return df_filtrado


def deduplicate_cross(df: pd.DataFrame) -> pd.DataFrame:
    """Remove duplicatas por DOI e título normalizado (cross-database)."""
    n_before = len(df)

    # Passo 1: DOI
    df["doi_clean"] = df["doi"].astype(str).str.strip().str.lower()
    df.loc[df["doi_clean"].isin(["", "nan", "none"]), "doi_clean"] = pd.NA
    df = df.drop_duplicates(subset="doi_clean", keep="first")

    # Passo 2: título normalizado
    df["title_norm"] = (
        df["title"]
        .astype(str)
        .str.lower()
        .str.replace(r"[^a-z0-9\s]", "", regex=True)
        .str.strip()
    )
    df = df.drop_duplicates(subset="title_norm", keep="first")
    df = df.drop(columns=["doi_clean", "title_norm"])

    n_after = len(df)
    log.info(f"Deduplicação cross-database: {n_before} → {n_after} "
             f"({n_before - n_after} duplicatas removidas)")
    return df.reset_index(drop=True)


# ---------------------------------------------------------------
# EXPORTAÇÃO BibTeX
# ---------------------------------------------------------------

def export_bibtex(df: pd.DataFrame, filename: str):
    """Exporta DataFrame em formato BibTeX."""
    lines = []
    for i, row in df.iterrows():
        author_key = re.sub(
            r"[^a-zA-Z]", "",
            str(row.get("authors", "")).split(",")[0].split(";")[0]
        )[:15]
        year = str(row.get("year", "0000"))[:4]
        key = f"{author_key}{year}_{i}"

        lines.append(f"@article{{{key},")
        lines.append(f'  title = {{{row.get("title", "")}}},')
        lines.append(f'  author = {{{row.get("authors", "")}}},')
        lines.append(f'  journal = {{{row.get("journal", "")}}},')
        lines.append(f'  year = {{{year}}},')
        if row.get("doi"):
            lines.append(f'  doi = {{{row.get("doi")}}},')
        if row.get("keywords"):
            lines.append(f'  keywords = {{{row.get("keywords")}}},')
        if row.get("abstract"):
            lines.append(f'  abstract = {{{row.get("abstract")}}},')
        lines.append("}")
        lines.append("")

    filepath = DIR_BIB / filename
    DIR_BIB.mkdir(parents=True, exist_ok=True)
    filepath.write_text("\n".join(lines), encoding="utf-8")
    log.info(f"BibTeX exportado: {filepath} ({len(df)} entradas)")


# ---------------------------------------------------------------
# EXECUÇÃO PRINCIPAL
# ---------------------------------------------------------------

def main():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")

    # Sempre imprimir a query para referência
    query = print_query()

    # Procurar arquivos WoS exportados
    wos_files = find_wos_files()

    if not wos_files:
        print("\n⚠ Nenhum arquivo WoS encontrado na pasta.")
        print(f"  Pasta: {DIR_DB}")
        print("  Nomes esperados: savedrecs.txt, wos_export.txt, etc.")
        print("\n  Siga as instruções acima para exportar do WoS e")
        print("  depois re-execute este script.")
        sys.exit(0)

    # Ler todos os arquivos WoS
    wos_dfs = []
    for f in wos_files:
        try:
            df = read_wos_tabdelimited(f)
            wos_dfs.append(df)
            log.info(f"  → {len(df)} registros de {f.name}")
        except Exception as e:
            log.error(f"Erro ao ler {f}: {e}")

    if not wos_dfs:
        log.error("Não foi possível ler nenhum arquivo WoS.")
        sys.exit(1)

    df_wos = pd.concat(wos_dfs, ignore_index=True)
    log.info(f"\nTotal WoS bruto: {len(df_wos)} registros")

    # Filtrar tipo documental
    df_wos_filtrado = filtrar_tipo_documento(df_wos)

    # Filtrar janela temporal (2016–2026)
    df_wos_filtrado["_year_int"] = pd.to_numeric(
        df_wos_filtrado["year"], errors="coerce"
    )
    mask_year = (
        df_wos_filtrado["_year_int"].between(ANO_INICIO, ANO_FIM)
        | df_wos_filtrado["_year_int"].isna()
    )
    n_fora_janela = (~mask_year).sum()
    if n_fora_janela > 0:
        log.info(
            f"Filtro temporal WoS: removidos {n_fora_janela} registros "
            f"fora de {ANO_INICIO}–{ANO_FIM}"
        )
    df_wos_filtrado = df_wos_filtrado[mask_year].drop(columns="_year_int").reset_index(drop=True)
    n_wos_filtrado = len(df_wos_filtrado)

    # Exportar BibTeX do WoS
    export_bibtex(df_wos_filtrado, f"wos_manual_{timestamp}.bib")

    # Ler Scopus existente (filtra apenas registros Scopus do consolidado)
    if SCOPUS_FILE.exists():
        log.info(f"\nLendo base existente: {SCOPUS_FILE}")
        df_scopus = pd.read_excel(SCOPUS_FILE, engine="openpyxl", dtype=str)
        if "source_db" in df_scopus.columns:
            df_scopus = df_scopus[df_scopus["source_db"] == "Scopus"].reset_index(drop=True)
        log.info(f"  Scopus: {len(df_scopus)} registros")
    else:
        log.warning(f"Arquivo Scopus não encontrado: {SCOPUS_FILE}")
        df_scopus = pd.DataFrame()

    # Consolidar Scopus + WoS
    # Garantir mesmas colunas
    all_cols = sorted(set(list(df_scopus.columns) + list(df_wos_filtrado.columns)))
    for col in all_cols:
        if col not in df_scopus.columns:
            df_scopus[col] = ""
        if col not in df_wos_filtrado.columns:
            df_wos_filtrado[col] = ""

    df_all = pd.concat([df_scopus, df_wos_filtrado], ignore_index=True)
    n_bruto = len(df_all)
    log.info(f"\nTotal bruto (Scopus + WoS): {n_bruto}")

    # Deduplicar cross-database
    df_dedup = deduplicate_cross(df_all)

    # Exportar consolidado
    xlsx_path = DIR_DB / f"busca_consolidada_scopus_wos_{timestamp}.xlsx"
    df_dedup.to_excel(xlsx_path, index=False, engine="openpyxl")
    log.info(f"\nPlanilha consolidada: {xlsx_path}")

    export_bibtex(df_dedup, f"consolidado_scopus_wos_{timestamp}.bib")

    # Contagens PRISMA
    n_wos_only = len(df_dedup[df_dedup["source_db"] == "WoS"])
    n_scopus_only = len(df_dedup[df_dedup["source_db"] == "Scopus"])

    print("\n" + "=" * 60)
    print("  CONTAGENS PRISMA (Scopus + WoS)")
    print("=" * 60)
    print(f"  Scopus (bruto):              {len(df_scopus)}")
    print(f"  WoS (bruto):                 {len(df_wos)}")
    print(f"  WoS após filtro doc_type:    {n_wos_filtrado}")
    print(f"  Total combinado:             {n_bruto}")
    print(f"  Após deduplicação:           {len(df_dedup)}")
    print(f"  Duplicatas removidas:        {n_bruto - len(df_dedup)}")
    print(f"  ─────────────────────────")
    print(f"  Registros Scopus únicos:     {n_scopus_only}")
    print(f"  Registros WoS únicos:        {n_wos_only}")
    print(f"  Sobreposição estimada:       {n_bruto - len(df_dedup)} registros")
    print("=" * 60)

    # Planilha de triagem
    df_triagem = df_dedup.copy()
    df_triagem["decisao_rev1"] = ""
    df_triagem["decisao_rev2"] = ""
    df_triagem["motivo_exclusao"] = ""
    df_triagem["dimensao_V"] = ""

    triagem_path = DIR_DB / f"triagem_scopus_wos_{timestamp}.xlsx"
    df_triagem.to_excel(triagem_path, index=False, engine="openpyxl")
    log.info(f"Planilha de triagem: {triagem_path}")

    print(f"\n✔ Integração concluída. Arquivo final: {xlsx_path}")


if __name__ == "__main__":
    main()

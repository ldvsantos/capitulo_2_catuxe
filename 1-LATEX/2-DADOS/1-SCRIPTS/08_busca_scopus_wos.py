# ================================================================
# 08_busca_scopus_wos.py — Raspagem automatizada Scopus + WoS
# Artigo 2: Meta-análise de vulnerabilidade biocultural (V1–V6)
#
# Executa as buscas dos 3 blocos semânticos descritos no §2.4
# do manuscrito (PRISMA 2020) nas bases Scopus e Web of Science.
#
# Dependências:
#   pip install pybliometrics requests pandas openpyxl
#
# Configuração necessária:
#   - Scopus: chave de API Elsevier (https://dev.elsevier.com/)
#   - WoS: API Key do Web of Science Starter API
#           (https://developer.clarivate.com/apis/wos-starter)
# ================================================================

import os
import re
import json
import time
import logging
from pathlib import Path
from datetime import datetime

import pandas as pd
import requests

# ---------------------------------------------------------------
# CONFIGURAÇÃO
# ---------------------------------------------------------------

# Chaves de API — preencher ou definir como variáveis de ambiente
SCOPUS_API_KEY = os.environ.get("SCOPUS_API_KEY", "465a2fe04ff2d247552d79c320c3c7c6")
WOS_API_KEY    = os.environ.get("WOS_API_KEY",    "7175a765485c628a89aaff8be29d05257e9e176e")

# Diretórios de saída
DIR_BASE   = Path(__file__).resolve().parent.parent  # 2-DADOS/
DIR_OUTPUT = DIR_BASE / "2-BANCO_DADOS"
DIR_BIB    = DIR_BASE / "3-BIB_EXPORTS"
DIR_OUTPUT.mkdir(parents=True, exist_ok=True)
DIR_BIB.mkdir(parents=True, exist_ok=True)

# Janela temporal (§2.3 PICOS) — últimos 10 anos
ANO_INICIO = 2016
ANO_FIM    = 2026

# Logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger(__name__)

# ---------------------------------------------------------------
# 1. BLOCOS SEMÂNTICOS (§2.4 do manuscrito)
# ---------------------------------------------------------------
# Bloco 1 (População): SAT / TEK
# Bloco 2 (Intervenção/Exposição): Salvaguarda
# Bloco 3 (Desfechos): Vulnerabilidade

# --- INGLÊS ---
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

# --- PORTUGUÊS ---
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

# --- ESPANHOL ---
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


def build_or_block(terms: list[str]) -> str:
    """Conecta termos com OR."""
    return " OR ".join(terms)


# ===============================================================
# 2. SCOPUS — via Elsevier Search API
# ===============================================================

SCOPUS_BASE_URL = "https://api.elsevier.com/content/search/scopus"

def build_scopus_query() -> str:
    """
    Constrói a query Scopus no formato:
    TITLE-ABS-KEY( (bloco1) AND (bloco2) AND (bloco3) )
    AND PUBYEAR > 1999 AND PUBYEAR < 2026
    """
    b1 = build_or_block(BLOCO1_EN + BLOCO1_PT + BLOCO1_ES)
    b2 = build_or_block(BLOCO2_EN + BLOCO2_PT + BLOCO2_ES)
    b3 = build_or_block(BLOCO3_EN + BLOCO3_PT + BLOCO3_ES)

    query = (
        f"TITLE-ABS-KEY( ({b1}) AND ({b2}) AND ({b3}) ) "
        f"AND PUBYEAR > {ANO_INICIO - 1} AND PUBYEAR < {ANO_FIM + 1}"
    )
    return query


def scopus_search(query: str, max_results: int = 2000) -> pd.DataFrame:
    """Executa busca paginada na API do Scopus."""
    headers = {
        "X-ELS-APIKey": SCOPUS_API_KEY,
        "Accept": "application/json",
    }
    results = []
    start = 0
    count = 25  # máximo por requisição

    log.info("Iniciando busca Scopus...")
    log.info(f"Query: {query[:200]}...")

    while start < max_results:
        params = {
            "query": query,
            "start": start,
            "count": count,
            "sort": "relevancy",
            "field": "dc:title,dc:creator,prism:publicationName,prism:coverDate,"
                     "prism:doi,dc:description,authkeywords,citedby-count,"
                     "prism:aggregationType,subtypeDescription,eid",
        }

        resp = requests.get(SCOPUS_BASE_URL, headers=headers, params=params, timeout=30)

        if resp.status_code == 429:
            log.warning("Rate limit Scopus. Aguardando 10s...")
            time.sleep(10)
            continue

        if resp.status_code != 200:
            log.error(f"Scopus HTTP {resp.status_code}: {resp.text[:300]}")
            break

        data = resp.json().get("search-results", {})
        total = int(data.get("opensearch:totalResults", 0))

        if start == 0:
            log.info(f"Total de resultados Scopus: {total}")
            max_results = min(max_results, total)

        entries = data.get("entry", [])
        if not entries or entries[0].get("error"):
            break

        for e in entries:
            results.append({
                "source_db":    "Scopus",
                "eid":          e.get("eid", ""),
                "doi":          e.get("prism:doi", ""),
                "title":        e.get("dc:title", ""),
                "authors":      e.get("dc:creator", ""),
                "journal":      e.get("prism:publicationName", ""),
                "year":         str(e.get("prism:coverDate", ""))[:4],
                "abstract":     e.get("dc:description", ""),
                "keywords":     e.get("authkeywords", ""),
                "citations":    e.get("citedby-count", ""),
                "doc_type":     e.get("subtypeDescription", ""),
            })

        start += count
        time.sleep(0.3)  # respeitar rate limit

    df = pd.DataFrame(results)
    log.info(f"Scopus: {len(df)} registros recuperados.")
    return df


# ===============================================================
# 3. WEB OF SCIENCE — via WoS Starter API v1 (Clarivate)
#    Docs: https://developer.clarivate.com/apis/wos-starter
#    Swagger: https://developer.clarivate.com/apis/wos-starter/swagger
#    Endpoints:
#      GET /documents         — q*, db, limit, page, sortField,
#                               publishTimeSpan, modifiedTimeSpan,
#                               tcModifiedTimeSpan, detail, edition
#      GET /documents/{uid}   — uid*, detail
#      GET /journals           — issn
#      GET /journals/{id}      — id*
#    Auth: X-ApiKey header
#    Plans: Free Trial = 1 req/s, 50 req/dia
#    Field tags: TI, IS, SO, VL, PG, CS, PY, FPY, DOP,
#                AU, AI, UT, DO, DT, PMID, OG, TS, SUR
# ===============================================================

WOS_BASE_URL = "https://api.clarivate.com/apis/wos-starter/v1/documents"

# Limite diário do Free Trial Plan
WOS_MAX_REQUESTS_DAY = 50
_wos_requests_today = 0


def wos_health_check() -> bool:
    """Testa conectividade com a WoS Starter API antes da busca."""
    headers = {"X-ApiKey": WOS_API_KEY}
    try:
        r = requests.get(
            WOS_BASE_URL,
            headers=headers,
            params={"q": "PY=2020", "db": "WOS", "limit": 1, "page": 1},
            timeout=15,
        )
        if r.status_code == 200:
            log.info("WoS health check OK.")
            remaining = r.headers.get("x-ratelimit-remaining-day", "?")
            log.info(f"  Rate-limit restante hoje: {remaining}")
            return True
        elif r.status_code == 401:
            log.error("WoS health check FALHOU: chave inválida (401).")
            return False
        elif r.status_code >= 500:
            log.error(f"WoS health check FALHOU: erro de servidor ({r.status_code}).")
            log.error(f"  Detalhes: {r.text[:300]}")
            return False
        else:
            log.warning(f"WoS health check retornou HTTP {r.status_code}.")
            return False
    except requests.RequestException as e:
        log.error(f"WoS health check erro de rede: {e}")
        return False


def build_wos_query() -> str:
    """
    Constrói a query WoS Starter no formato TS=(bloco1 AND bloco2 AND bloco3).
    O parâmetro 'q' aceita field tags: TS (Topic Search) busca em
    Title, Abstract, Author keywords e Keywords Plus.
    """
    b1 = build_or_block(BLOCO1_EN + BLOCO1_PT + BLOCO1_ES)
    b2 = build_or_block(BLOCO2_EN + BLOCO2_PT + BLOCO2_ES)
    b3 = build_or_block(BLOCO3_EN + BLOCO3_PT + BLOCO3_ES)

    query = f"TS=(({b1}) AND ({b2}) AND ({b3}))"
    return query


def wos_search(query: str, max_results: int = 2000) -> pd.DataFrame:
    """
    Executa busca paginada na WoS Starter API.
    GET https://api.clarivate.com/apis/wos-starter/v1/documents

    Params (Swagger v1):
      q*               — advanced search query (field tags: TS, TI, AU, etc.)
      db               — database (default WOS)
      limit            — records per page, 1–50 (default 10)
      page             — result page, 1-based (default 1)
      sortField        — e.g. PY+D, RS+D, TC+D, LD+D
      publishTimeSpan  — yyyy-mm-dd+yyyy-mm-dd
      edition          — e.g. WOS+SCI,WOS+SSCI
      detail           — omit or 'short'

    Response JSON:
      metadata: { total, page, limit }
      hits: [ { uid, title, types, sourceTypes, source, names,
               links, citations, identifiers, keywords } ]
    """
    global _wos_requests_today
    headers = {
        "X-ApiKey": WOS_API_KEY,
        "Accept": "application/json",
    }
    results = []
    page = 1
    limit = 50  # WoS Starter permite máximo 50 por página

    log.info("Iniciando busca Web of Science (Starter API v1)...")
    log.info(f"Query: {query[:200]}...")

    while True:
        # Controle de limite diário (Free Trial = 50 req/dia)
        if _wos_requests_today >= WOS_MAX_REQUESTS_DAY:
            log.warning(f"Limite diário WoS atingido ({WOS_MAX_REQUESTS_DAY} req). "
                        "Interrompendo busca. Retomar amanhã.")
            break

        params = {
            "db": "WOS",
            "q": query,
            "limit": limit,
            "page": page,
            "sortField": "PY+D",  # Publication Year Descending
            "publishTimeSpan": f"{ANO_INICIO}-01-01+{ANO_FIM}-12-31",
        }

        resp = requests.get(WOS_BASE_URL, headers=headers, params=params, timeout=60)
        _wos_requests_today += 1

        # Log do rate-limit restante
        remaining_day = resp.headers.get("x-ratelimit-remaining-day", "?")
        if page == 1 or page % 10 == 0:
            log.info(f"  [WoS] página {page} | rate-limit restante: {remaining_day}/dia")

        if resp.status_code == 429:
            retry_after = int(resp.headers.get("Retry-After", 10))
            log.warning(f"Rate limit WoS (429). Aguardando {retry_after}s...")
            time.sleep(retry_after)
            continue

        if resp.status_code >= 500:
            log.error(f"WoS Starter HTTP {resp.status_code} (servidor): {resp.text[:500]}")
            log.error("Possível outage na Clarivate. Tente novamente mais tarde.")
            break

        if resp.status_code != 200:
            log.error(f"WoS Starter HTTP {resp.status_code}: {resp.text[:500]}")
            break

        data = resp.json()
        metadata = data.get("metadata", {})
        total = int(metadata.get("total", 0))

        if page == 1:
            log.info(f"Total de resultados WoS: {total}")
            max_results = min(max_results, total)

        hits = data.get("hits", [])
        if not hits:
            break

        for rec in hits:
            # --- UID ---
            uid = rec.get("uid", rec.get("UID", ""))

            # --- Título ---
            title_obj = rec.get("title", "")
            title = title_obj if isinstance(title_obj, str) else str(title_obj)

            # --- Autores (Swagger: names.authors[].wosStandard / displayName) ---
            names = rec.get("names", {})
            authors_list = names.get("authors", []) if isinstance(names, dict) else []
            if isinstance(authors_list, list):
                author_str = "; ".join(
                    a.get("wosStandard", a.get("displayName", str(a)))
                    for a in authors_list if isinstance(a, dict)
                )
            else:
                author_str = str(authors_list)

            # --- Source / Journal ---
            source = rec.get("source", {})
            if isinstance(source, dict):
                journal = source.get("sourceTitle", source.get("title", ""))
                year = str(source.get("publishYear", source.get("publishMonth", "")))[:4]
                pages = source.get("pages", {}).get("range", "")
                volume = source.get("volume", "")
            else:
                journal, year, pages, volume = "", "", "", ""

            # --- DOI, ISSN e outros identificadores ---
            # Swagger: identifiers.doi, identifiers.issn, identifiers.eissn,
            #          identifiers.isbn, identifiers.eisbn, identifiers.pmid
            identifiers = rec.get("identifiers", {})
            doi = ""
            issn = ""
            if isinstance(identifiers, dict):
                doi = identifiers.get("doi", "")
                issn = identifiers.get("issn", identifiers.get("eissn", ""))
                if isinstance(doi, list):
                    doi = doi[0] if doi else ""

            # --- Keywords ---
            kw_raw = rec.get("keywords", {})
            if isinstance(kw_raw, dict):
                kw_list = kw_raw.get("authorKeywords", [])
            elif isinstance(kw_raw, list):
                kw_list = kw_raw
            else:
                kw_list = []
            kw_str = "; ".join(str(k) for k in kw_list) if kw_list else ""

            # --- Citações ---
            citations = rec.get("citations", [])
            cite_count = 0
            if isinstance(citations, list) and citations:
                c = citations[0]
                cite_count = c.get("count", 0) if isinstance(c, dict) else 0
            elif isinstance(citations, (int, float)):
                cite_count = int(citations)

            # --- Tipo de documento ---
            # Swagger: types[] (normalized) e sourceTypes[] (source)
            doc_types = rec.get("types", rec.get("sourceTypes", []))
            if isinstance(doc_types, list) and doc_types:
                doc_type = doc_types[0] if isinstance(doc_types[0], str) else str(doc_types[0])
            elif isinstance(doc_types, str):
                doc_type = doc_types
            else:
                doc_type = ""

            # --- Link para o registro WoS ---
            links = rec.get("links", {})
            wos_url = links.get("record", "") if isinstance(links, dict) else ""

            results.append({
                "source_db":  "WoS",
                "uid":        uid,
                "doi":        doi,
                "issn":       issn,
                "title":      title,
                "authors":    author_str,
                "journal":    journal,
                "year":       year[:4] if year else "",
                "volume":     volume,
                "pages":      pages,
                "abstract":   "",  # WoS Starter não retorna abstract
                "keywords":   kw_str,
                "citations":  cite_count,
                "doc_type":   doc_type,
                "wos_url":    wos_url,
            })

        # Verificar se já coletou tudo
        collected = page * limit
        if collected >= max_results or collected >= total:
            break

        page += 1
        time.sleep(1.1)  # Free Trial: max 1 req/s

    df = pd.DataFrame(results)
    log.info(f"WoS Starter: {len(df)} registros recuperados.")
    return df


# ===============================================================
# 4. DEDUPLICAÇÃO E EXPORTAÇÃO
# ===============================================================

# Tipos de documento aceitos (PICOS §2.3)
DOC_TYPES_ACEITOS = ["Article", "Review"]


def filtrar_tipo_documento(df: pd.DataFrame) -> pd.DataFrame:
    """Mantém apenas Articles e Reviews, removendo Conference Papers,
    Book Chapters, Editorials e outros tipos não elegíveis."""
    n_before = len(df)
    df_filtrado = df[df["doc_type"].isin(DOC_TYPES_ACEITOS)].reset_index(drop=True)
    n_after = len(df_filtrado)
    removidos = n_before - n_after
    if removidos > 0:
        excluidos = df[~df["doc_type"].isin(DOC_TYPES_ACEITOS)]["doc_type"].value_counts()
        log.info(f"Filtro doc_type: {n_before} → {n_after} ({removidos} removidos)")
        for dt, c in excluidos.items():
            log.info(f"  Removido: {dt} ({c})")
    else:
        log.info(f"Filtro doc_type: todos os {n_before} registros são Article/Review.")
    return df_filtrado


def deduplicate(df: pd.DataFrame) -> pd.DataFrame:
    """Remove duplicatas por DOI e por título fuzzy."""
    n_before = len(df)

    # Passo 1: normalizar DOI
    df["doi_clean"] = df["doi"].astype(str).str.strip().str.lower()
    df = df.drop_duplicates(subset="doi_clean", keep="first")

    # Passo 2: normalizar título para matching
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
    log.info(f"Deduplicação: {n_before} → {n_after} ({n_before - n_after} removidos)")
    return df.reset_index(drop=True)


def export_bibtex(df: pd.DataFrame, filename: str):
    """Exporta DataFrame em formato BibTeX simplificado."""
    lines = []
    for i, row in df.iterrows():
        # Gerar chave: PrimeiroAutor_Ano_i
        author_key = re.sub(r"[^a-zA-Z]", "", str(row.get("authors", "")).split(",")[0].split(";")[0])[:15]
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
    filepath.write_text("\n".join(lines), encoding="utf-8")
    log.info(f"BibTeX exportado: {filepath} ({len(df)} entradas)")


# ===============================================================
# 5. EXECUÇÃO PRINCIPAL
# ===============================================================

def main():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")

    # --- Strings de busca (salvar para auditoria PRISMA) ---
    scopus_query = build_scopus_query()
    wos_query    = build_wos_query()

    strings_file = DIR_OUTPUT / f"search_strings_{timestamp}.txt"
    strings_file.write_text(
        f"=== SCOPUS ===\n{scopus_query}\n\n=== WOS ===\n{wos_query}\n",
        encoding="utf-8"
    )
    log.info(f"Strings de busca salvas em: {strings_file}")

    # --- Scopus ---
    df_scopus = pd.DataFrame()
    if SCOPUS_API_KEY and "SUA_CHAVE" not in SCOPUS_API_KEY:
        df_scopus = scopus_search(scopus_query)
        export_bibtex(df_scopus, f"scopus_{timestamp}.bib")
    else:
        log.warning("SCOPUS_API_KEY não configurada. Pulando Scopus.")

    # --- Web of Science ---
    df_wos = pd.DataFrame()
    if WOS_API_KEY and "SUA_CHAVE" not in WOS_API_KEY:
        if wos_health_check():
            df_wos = wos_search(wos_query)
            export_bibtex(df_wos, f"wos_{timestamp}.bib")
        else:
            log.error("WoS health check falhou. Verifique a chave ou tente mais tarde.")
    else:
        log.warning("WOS_API_KEY não configurada. Pulando WoS.")

    # --- Consolidar e deduplicar ---
    df_all = pd.concat([df_scopus, df_wos], ignore_index=True)

    if df_all.empty:
        log.warning("Nenhum resultado recuperado. Verifique as chaves de API.")
        return

    n_bruto = len(df_all)

    # --- Filtrar tipos de documento (manter apenas Article e Review) ---
    df_filtrado = filtrar_tipo_documento(df_all)
    n_pos_filtro = len(df_filtrado)

    df_dedup = deduplicate(df_filtrado)

    # --- Exportar ---
    xlsx_path = DIR_OUTPUT / f"busca_consolidada_{timestamp}.xlsx"
    df_dedup.to_excel(xlsx_path, index=False, engine="openpyxl")
    log.info(f"Planilha consolidada: {xlsx_path}")

    export_bibtex(df_dedup, f"consolidado_{timestamp}.bib")

    # --- Contagens PRISMA ---
    log.info("\n=== CONTAGENS PRISMA ===")
    log.info(f"  Scopus:              {len(df_scopus)}")
    log.info(f"  Web of Science:      {len(df_wos)}")
    log.info(f"  Total bruto:         {n_bruto}")
    log.info(f"  Após filtro doc_type:{n_pos_filtro}")
    log.info(f"  Após deduplicação:   {len(df_dedup)}")
    log.info(f"  Duplicatas removidas:{n_pos_filtro - len(df_dedup)}")

    # --- Adicionar colunas de triagem ---
    df_triagem = df_dedup.copy()
    df_triagem["decisao_rev1"] = ""
    df_triagem["decisao_rev2"] = ""
    df_triagem["motivo_exclusao"] = ""
    df_triagem["dimensao_V"] = ""

    triagem_path = DIR_OUTPUT / f"triagem_{timestamp}.xlsx"
    df_triagem.to_excel(triagem_path, index=False, engine="openpyxl")
    log.info(f"Planilha de triagem: {triagem_path}")

    log.info("✔ Busca concluída com sucesso.")


if __name__ == "__main__":
    main()

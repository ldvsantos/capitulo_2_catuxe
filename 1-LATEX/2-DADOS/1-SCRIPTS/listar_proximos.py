"""
Script para identificar próximos estudos para codificação
"""
import pandas as pd
import json
import os
import fitz

pdf_dir = r'c:\Users\vidal\OneDrive\Documentos\13 - CLONEGIT\artigo_2_catuxe\1-LATEX\2-DADOS\2-BANCO_DADOS\1-ARTIGOS_SELECIONADOS'

# PDFs acessíveis
acessiveis = []
for f in os.listdir(pdf_dir):
    if f.endswith('.pdf'):
        try:
            doc = fitz.open(os.path.join(pdf_dir, f))
            doc.close()
            acessiveis.append(f)
        except:
            pass

print(f'PDFs acessíveis: {len(acessiveis)}')

# Carregar mapeamento e planilha
with open(r'c:\Users\vidal\OneDrive\Documentos\13 - CLONEGIT\artigo_2_catuxe\1-LATEX\2-DADOS\2-BANCO_DADOS\3-OUTPUT\pdf_to_bdid_map.json', 'r', encoding='utf-8') as f:
    mapping = json.load(f)

df = pd.read_excel(r'c:\Users\vidal\OneDrive\Documentos\13 - CLONEGIT\artigo_2_catuxe\1-LATEX\2-DADOS\2-BANCO_DADOS\2-DADOS_TABULADOS\bd_codificacao_qualitativa.xlsx', sheet_name='CODIFICACAO')

# IDs não codificados
nao_codificados = set(df[df['Direcao_efeito'].isna()]['Study_ID'].unique())
print(f'Estudos não codificados: {len(nao_codificados)}')

# Encontrar IDs com PDF acessível
ids_com_pdf = {}
for item in mapping['matched']:
    if item['file'] in acessiveis and item['matched_id'] is not None:
        ids_com_pdf[item['matched_id']] = item['file']

# Interseção
disponiveis = nao_codificados.intersection(set(ids_com_pdf.keys()))
print(f'Estudos não codificados COM PDF acessível: {len(disponiveis)}')
print()

# Mostrar detalhes
print('='*70)
print('PRÓXIMOS ESTUDOS PARA CODIFICAÇÃO:')
print('='*70)
for sid in sorted(disponiveis)[:10]:
    row = df[df['Study_ID'] == sid].iloc[0]
    pdf = ids_com_pdf[sid]
    print(f"\nID={sid}: {row['Study']} ({row['Year']})")
    print(f"  Tier: {row['Tier']}")
    print(f"  PDF: {pdf[:60]}...")

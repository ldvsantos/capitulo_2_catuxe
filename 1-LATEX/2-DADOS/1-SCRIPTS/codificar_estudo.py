"""
Script para registrar codificações na planilha bd_codificacao_qualitativa.xlsx
"""
import pandas as pd

file_path = r'c:\Users\vidal\OneDrive\Documentos\13 - CLONEGIT\artigo_2_catuxe\1-LATEX\2-DADOS\2-BANCO_DADOS\2-DADOS_TABULADOS\bd_codificacao_qualitativa.xlsx'

# Carregar planilha
df = pd.read_excel(file_path, sheet_name='CODIFICACAO')

# Codificações do estudo ID=2 (Calvet-Mir et al. 2016)
# Estudo descritivo sobre transmissão de conhecimento em hortas domésticas (Pirineus Catalães)
codificacoes = {
    'V1': {
        'Direcao_efeito': -1, 
        'Intensidade': 2,
        'Notas_codificador': 'V1: Sistema com diversidade preservada. 55 elementos culturais identificados. Evidência qualitativa.'
    },
    'V2': {
        'Direcao_efeito': -1, 
        'Intensidade': 2,
        'Notas_codificador': 'V2: Transmissão ativa pais->filhos. Múltiplos canais funcionando. Confere resiliência.'
    },
    'V3': {
        'Direcao_efeito': -1, 
        'Intensidade': 2,
        'Notas_codificador': 'V3: Alta complexidade - 55 manifestações culturais (ditados, práticas, receitas). Múltiplas categorias de manejo.'
    },
    'V4': {
        'Direcao_efeito': -1, 
        'Intensidade': 1,
        'Notas_codificador': 'V4: Sistema produtivo ativo contribui para alimentação. Evidência indireta, não medida diretamente.'
    },
    'V5': {
        'Direcao_efeito': 1, 
        'Intensidade': 1,
        'Notas_codificador': 'V5: Sem sistema formal de registro mencionado. Conhecimento oral sem inventário institucional.'
    },
    'V6': {
        'Direcao_efeito': 0, 
        'Intensidade': 2,
        'Notas_codificador': 'V6: Pressões externas (urbanização, globalização) mas sistema resiste como refugio biocultural.'
    },
}

# Atualizar linhas do estudo ID=2
for idx, row in df.iterrows():
    if row['Study_ID'] == 2:
        dim = row['Dimensao']
        if dim in codificacoes:
            df.at[idx, 'Direcao_efeito'] = codificacoes[dim]['Direcao_efeito']
            df.at[idx, 'Intensidade'] = codificacoes[dim]['Intensidade']
            df.at[idx, 'Revisor'] = 'R1_Diego'
            df.at[idx, 'Confianca_codificacao'] = 'media'
            df.at[idx, 'Notas_codificador'] = codificacoes[dim]['Notas_codificador']

# Salvar
with pd.ExcelWriter(file_path, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
    df.to_excel(writer, sheet_name='CODIFICACAO', index=False)

print('=' * 60)
print('Estudo ID=2 (Calvet-Mir et al. 2016) codificado com sucesso!')
print('=' * 60)
print()
print('Resumo das codificações:')
for dim, vals in codificacoes.items():
    dir_str = '+1' if vals['Direcao_efeito'] == 1 else str(vals['Direcao_efeito'])
    print(f"  {dim}: Direção={dir_str}, Intensidade={vals['Intensidade']}")
print()
print('Progresso: 1/199 registros codificados (0.5%)')

# Protocolo de CodificaÃ§Ã£o de EvidÃªncia Qualitativa e Semi-Quantitativa

## RevisÃ£o SistemÃ¡tica e Meta-AnÃ¡lise â€” Artigo 2 (Catuxe)

**VersÃ£o:** 1.0  
**Data:** 2 de marÃ§o de 2026  
**ResponsÃ¡vel:** Diego Vidal  
**Arquivo de trabalho:** `bd_codificacao_qualitativa.xlsx` (aba CODIFICACAO)  
**Registros para codificaÃ§Ã£o:** 199  

---

## 1. Objetivo

Este protocolo instrui dois revisores independentes (R1 e R2) a codificar 199 registros de estudos primÃ¡rios que nÃ£o possuem dados quantitativos completos (mÃ©dia, desvio-padrÃ£o e n para ambos os grupos). Cada registro corresponde a uma comparaÃ§Ã£o entre um grupo/condiÃ§Ã£o de tratamento (sistemas tradicionais, intervenÃ§Ãµes de salvaguarda) e um grupo/condiÃ§Ã£o de controle (sistemas convencionais, ausÃªncia de intervenÃ§Ã£o), avaliada em uma das seis dimensÃµes de vulnerabilidade biocultural (V1â€“V6).

A codificaÃ§Ã£o converte a evidÃªncia narrativa em dois valores numÃ©ricos (direÃ§Ã£o e intensidade do efeito) que serÃ£o posteriormente transformados em tamanhos de efeito (lnRR) pelo script de conversÃ£o automatizado. A qualidade desta codificaÃ§Ã£o determina diretamente a robustez da meta-anÃ¡lise.

---

## 2. Contexto do Banco de Dados

### 2.1 ClassificaÃ§Ã£o dos registros por tier de evidÃªncia

| Tier | DescriÃ§Ã£o | Registros | O que o revisor precisa fazer |
|------|-----------|:---------:|-------------------------------|
| **T1** | Quantitativo completo (n, mÃ©dia, SD para ambos os grupos) | 17 | Nada. JÃ¡ processados automaticamente. |
| **T2a** | Possui p-values numÃ©ricos extraÃ­dos do texto | 49 | Codificar **direÃ§Ã£o** do efeito e extrair **n** se possÃ­vel. Intensidade Ã© derivada do p-value. |
| **T2b** | Possui ANOVA/Kruskal-Wallis mas sem p-value explÃ­cito | 25 | Codificar **direÃ§Ã£o**, **intensidade** e extrair **n** se possÃ­vel. |
| **T3** | Resultados reportados (tabelas, comparaÃ§Ãµes) sem estatÃ­sticas formais | 94 | Codificar **direÃ§Ã£o**, **intensidade** e extrair **n** se possÃ­vel. |
| **T4** | Qualitativo puro (narrativa, sem dados numÃ©ricos) | 31 | Codificar **direÃ§Ã£o**, **intensidade**. Tamanho amostral raramente disponÃ­vel. |
| EX | Sem acesso ao artigo ou sem resultados | 72 | ExcluÃ­dos. NÃ£o codificar. |

### 2.2 DistribuiÃ§Ã£o por dimensÃ£o (apenas registros para codificaÃ§Ã£o)

| DimensÃ£o | CÃ³digo | T2a | T2b | T3 | T4 | Total |
|----------|:------:|:---:|:---:|:--:|:--:|:-----:|
| ErosÃ£o Intergeracional | V1 | 8 | 4 | 16 | 5 | 33 |
| Complexidade Biocultural | V2 | 8 | 4 | 15 | 5 | 32 |
| Singularidade Territorial | V3 | 9 | 5 | 15 | 5 | 34 |
| Status de DocumentaÃ§Ã£o | V4 | 8 | 4 | 16 | 6 | 34 |
| Vulnerabilidade JurÃ­dica | V5 | 8 | 4 | 16 | 5 | 33 |
| OrganizaÃ§Ã£o Social | V6 | 8 | 4 | 16 | 5 | 33 |

---

## 3. DefiniÃ§Ã£o das DimensÃµes de Vulnerabilidade

Antes de codificar, o revisor deve compreender o que cada dimensÃ£o mede e o que constitui agravamento vs. reduÃ§Ã£o de vulnerabilidade.

### V1 â€” ErosÃ£o Intergeracional
Riqueza e diversidade de variedades locais, espÃ©cies cultivadas e manejadas. Indicadores tÃ­picos incluem Ã­ndice de Shannon (H'), riqueza de espÃ©cies, contagem de variedades locais.

- **Vulnerabilidade agravada (+1):** reduÃ§Ã£o de diversidade, perda de variedades locais, substituiÃ§Ã£o por monocultura, simplificaÃ§Ã£o do sistema.
- **Vulnerabilidade reduzida (âˆ’1):** aumento de diversidade, conservaÃ§Ã£o in situ bem-sucedida, recuperaÃ§Ã£o de variedades perdidas.

### V2 â€” Complexidade Biocultural
Continuidade da transferÃªncia vertical de conhecimento entre geraÃ§Ãµes. Indicadores tÃ­picos incluem knowledge scores por faixa etÃ¡ria, frequÃªncia de eventos de transmissÃ£o, proporÃ§Ã£o de jovens com domÃ­nio do saber.

- **Vulnerabilidade agravada (+1):** queda no knowledge score dos jovens em comparaÃ§Ã£o a idosos, reduÃ§Ã£o de eventos de transmissÃ£o, abandono de prÃ¡ticas pedagÃ³gicas tradicionais.
- **Vulnerabilidade reduzida (âˆ’1):** jovens demonstram conhecimento equivalente ou crescente, programas de mentoria ativos, eventos de transmissÃ£o frequentes.

### V3 â€” Singularidade Territorial
Exclusividade geogrÃ¡fica e cosmolÃ³gica das prÃ¡ticas, riqueza de interaÃ§Ãµes ecolÃ³gicas codificadas nos sistemas. Indicadores tÃ­picos incluem beta-diversidade entre comunidades (Jaccard, Bray-Curtis), taxa de endemismo de variedades, complexidade da cadeia operatÃ³ria.

- **Vulnerabilidade agravada (+1):** homogeneizaÃ§Ã£o entre comunidades, perda de singularidade, simplificaÃ§Ã£o de prÃ¡ticas complexas.
- **Vulnerabilidade reduzida (âˆ’1):** manutenÃ§Ã£o de prÃ¡ticas distintas, alta beta-diversidade, preservaÃ§Ã£o de saberes Ãºnicos.

### V4 â€” Status de DocumentaÃ§Ã£o
Capacidade dos sistemas tradicionais de prover autonomia alimentar e nutricional. Indicadores tÃ­picos incluem diversidade dietÃ©tica, autossuficiÃªncia alimentar, contagem de espÃ©cies alimentÃ­cias utilizadas.

- **Vulnerabilidade agravada (+1):** reduÃ§Ã£o na diversidade dietÃ©tica, dependÃªncia de alimentos industrializados, abandono de cultivos alimentÃ­cios tradicionais.
- **Vulnerabilidade reduzida (âˆ’1):** manutenÃ§Ã£o ou aumento da diversidade alimentar, contribuiÃ§Ã£o significativa Ã  dieta, soberania alimentar.

### V5 â€” Vulnerabilidade JurÃ­dica
Grau de registro formal dos saberes em inventÃ¡rios, acervos e bases de dados. Indicadores tÃ­picos incluem contagem de saberes inventariados, completude de fichas tÃ©cnicas, taxa de digitalizaÃ§Ã£o.

- **Vulnerabilidade agravada (+1):** saberes sem registro, perda de documentaÃ§Ã£o existente, ausÃªncia de inventÃ¡rio, risco de desaparecimento sem registro.
- **Vulnerabilidade reduzida (âˆ’1):** inventariamento ativo, bases de dados comunitÃ¡rias, documentaÃ§Ã£o em vÃ­deo/Ã¡udio, fichas completas.

### V6 â€” OrganizaÃ§Ã£o Social
Vitalidade das estruturas comunitÃ¡rias de ensino, governanÃ§a e gestÃ£o do conhecimento. Indicadores tÃ­picos incluem nÃºmero de mestres de saberes ativos, existÃªncia de protocolos comunitÃ¡rios, frequÃªncia de aÃ§Ãµes coletivas.

- **Vulnerabilidade agravada (+1):** desarticulaÃ§Ã£o social, ausÃªncia de governanÃ§a, mestres sem sucessores, colapso de instituiÃ§Ãµes comunitÃ¡rias.
- **Vulnerabilidade reduzida (âˆ’1):** governanÃ§a ativa, protocolos comunitÃ¡rios funcionais, lideranÃ§as reconhecidas, aÃ§Ã£o coletiva efetiva.

---

## 4. Campos a Preencher na Planilha

A aba CODIFICACAO contÃ©m 19 colunas. As colunas com fundo **amarelo** devem ser preenchidas pelo revisor. As demais sÃ£o preenchidas automaticamente e nÃ£o devem ser alteradas.

### 4.1 Direcao_efeito (OBRIGATÃ“RIO)

Indica se a intervenÃ§Ã£o/condiÃ§Ã£o de tratamento **agrava ou reduz** a vulnerabilidade na dimensÃ£o atribuÃ­da.

| Valor | Significado | Quando usar |
|:-----:|-------------|-------------|
| **+1** | Vulnerabilidade **agravada** | O indicador piorou no grupo tratamento em relaÃ§Ã£o ao controle, OU a comparaÃ§Ã£o temporal mostra deterioraÃ§Ã£o. |
| **0** | **Neutro** / sem diferenÃ§a | Nenhuma diferenÃ§a perceptÃ­vel entre grupos, ou o estudo reporta explicitamente ausÃªncia de efeito. |
| **âˆ’1** | Vulnerabilidade **reduzida** | O indicador melhorou no grupo tratamento em relaÃ§Ã£o ao controle, OU a comparaÃ§Ã£o temporal mostra melhoria. |

**ATENÃ‡ÃƒO CRÃTICA:** A direÃ§Ã£o refere-se Ã  **vulnerabilidade**, nÃ£o ao indicador bruto. Por exemplo:
- Aumento de diversidade de espÃ©cies â†’ reduÃ§Ã£o de vulnerabilidade â†’ **âˆ’1**
- Aumento de knowledge score em jovens â†’ reduÃ§Ã£o de vulnerabilidade â†’ **âˆ’1**
- Perda de variedades locais â†’ agravamento de vulnerabilidade â†’ **+1**
- ReduÃ§Ã£o de eventos de transmissÃ£o â†’ agravamento de vulnerabilidade â†’ **+1**

### 4.2 Intensidade (OBRIGATÃ“RIO)

Magnitude percebida do efeito, avaliada pelo revisor com base no conteÃºdo do artigo original.

| Valor | Categoria | CritÃ©rios para atribuiÃ§Ã£o |
|:-----:|-----------|--------------------------|
| **1** | Fraca | DiferenÃ§a marginal, tendÃªncia sem significÃ¢ncia, p > 0.10, autores descrevem o efeito como pequeno ou nÃ£o significante. |
| **2** | Moderada | DiferenÃ§a notÃ¡vel, significÃ¢ncia estatÃ­stica borderline ou moderada (p < 0.05), autores enfatizam o resultado como relevante. |
| **3** | Forte | Grande diferenÃ§a, alta significÃ¢ncia (p < 0.01), mudanÃ§a qualitativa clara, autores descrevem como resultado principal do estudo. |

**Dicas para atribuiÃ§Ã£o quando nÃ£o hÃ¡ estatÃ­sticas formais (T3 e T4):**

- Use o **tom narrativo** do artigo: se os autores usam palavras como "drastic", "substantial", "complete loss", "dramatic decline" â†’ intensidade 3.
- Se usam "some", "slight", "tendency", "marginal" â†’ intensidade 1.
- Termos como "significant", "considerable", "important", "clear" â†’ intensidade 2.
- Se o artigo apresenta tabelas com nÃºmeros (sem teste estatÃ­stico), avalie a magnitude da diferenÃ§a relativa entre os grupos: diferenÃ§a < 20% â†’ 1, entre 20â€“50% â†’ 2, acima de 50% â†’ 3.
- Na dÃºvida, atribua intensidade 2 (moderada) como default conservador.

### 4.3 n_T_codificado (QUANDO DISPONÃVEL)

Tamanho amostral do grupo/condiÃ§Ã£o de **tratamento** (intervenÃ§Ã£o, sistema tradicional, etc.) extraÃ­do do texto do artigo.

- Se o artigo reporta n total sem separar grupos, coloque n/2 em cada campo e anote nas Notas_codificador.
- Se nÃ£o hÃ¡ informaÃ§Ã£o amostral, deixe em branco (o script usarÃ¡ um fallback conservador de n=30 por grupo).
- Procure na seÃ§Ã£o "Methods", "Study area", "Sampling", "Data collection" ou nas legendas das tabelas.

### 4.4 n_C_codificado (QUANDO DISPONÃVEL)

Mesmo critÃ©rio acima, para o grupo/condiÃ§Ã£o de **controle** (convencional, sem intervenÃ§Ã£o, etc.).

### 4.5 Revisor (OBRIGATÃ“RIO)

IdentificaÃ§Ã£o do revisor: preencha **R1** ou **R2**.

### 4.6 Confianca_codificacao (OBRIGATÃ“RIO)

Grau de confianÃ§a do revisor na codificaÃ§Ã£o atribuÃ­da.

| Valor | Significado |
|-------|-------------|
| **Alta** | Dados claros no texto, tabelas com nÃºmeros, ou estatÃ­sticas explÃ­citas que sustentam a codificaÃ§Ã£o sem ambiguidade. |
| **Moderada** | Inferido a partir de figuras, contexto narrativo ou combinaÃ§Ã£o de indicadores indiretos. |
| **Baixa** | InterpretaÃ§Ã£o subjetiva de narrativa qualitativa, sem dados numÃ©ricos de suporte. Pouca informaÃ§Ã£o disponÃ­vel no trecho relevante. |

### 4.7 Notas_codificador (OPCIONAL)

Campo livre para o revisor registrar justificativas, trechos do artigo que sustentam a decisÃ£o, dÃºvidas, ou qualquer observaÃ§Ã£o relevante para a fase de consenso. Recomendado especialmente quando Confianca = Baixa.

---

## 5. Procedimento Operacional por Tier

### 5.1 Tier T2a (49 registros) â€” Estudos com p-values

Estes registros jÃ¡ possuem p-values extraÃ­dos automaticamente do texto (coluna `p_values_extraidos`). O que o revisor precisa fazer:

1. **Abrir o PDF** do artigo (use o DOI na coluna C para localizar).
2. **Localizar** a seÃ§Ã£o de resultados correspondente Ã  dimensÃ£o e proxy atribuÃ­dos.
3. **Confirmar a direÃ§Ã£o:** o p-value Ã© significativo, mas nÃ£o indica se o efeito Ã© positivo ou negativo. O revisor deve ler o contexto e determinar se a vulnerabilidade aumentou (+1) ou diminuiu (âˆ’1).
4. **Atribuir Intensidade** com base na magnitude reportada e no p-value:
   - p < 0.01 e efeito grande â†’ 3
   - p < 0.05 e efeito moderado â†’ 2
   - p < 0.10 ou efeito marginal â†’ 1
5. **Extrair n** se possÃ­vel (colunas n_T_codificado e n_C_codificado).
6. **Preencher** Revisor e Confianca.

**Exemplo:**  
*Bastos J.G. (2022)*, V1 (Erosao Intergeracional), Proxy: Plant species richness.  
p-values extraÃ­dos: 0.002, 0.021, 0.165, 0.260, 0.366.  
O revisor abre o artigo, identifica que p=0.002 refere-se Ã  comparaÃ§Ã£o "antes vs. depois" de uma intervenÃ§Ã£o de conservaÃ§Ã£o que aumentou a riqueza de espÃ©cies.  
CodificaÃ§Ã£o: Direcao = âˆ’1, Intensidade = 3, Confianca = Alta.

### 5.2 Tier T2b (25 registros) â€” Estudos com ANOVA/KW sem p-value explÃ­cito

O texto indica "[TEM_STAT]" ou "Has ANOVA/KW". O estudo fez anÃ¡lise estatÃ­stica, mas o p-value especÃ­fico nÃ£o foi extraÃ­do automaticamente.

1. **Abrir o PDF** e localizar a tabela/seÃ§Ã£o de ANOVA ou Kruskal-Wallis.
2. **Extrair o p-value** manualmente se possÃ­vel, e anotÃ¡-lo nas Notas_codificador.
3. Se nÃ£o for possÃ­vel extrair o p-value, codificar com base na significÃ¢ncia reportada pelo autor:
   - Autor diz "significante" sem qualificar â†’ Intensidade = 2
   - Autor diz "altamente significante" â†’ Intensidade = 3
   - Autor diz "nÃ£o significante" â†’ Intensidade = 1
4. **Codificar direÃ§Ã£o** com base no sentido da diferenÃ§a entre os grupos.
5. **Extrair n** quando disponÃ­vel.

**Exemplo:**  
*Suwardi A.B. (2025)*, V1 (Erosao Intergeracional).  
Notas: "[TEM_STAT] | Has ANOVA/KW"  
O revisor abre o artigo, encontra ANOVA com F(2,45) = 8.32, p < 0.001, onde a diversidade Ã© maior em sistemas tradicionais que em convencionais.  
CodificaÃ§Ã£o: Direcao = âˆ’1, Intensidade = 3, n_T = 16, n_C = 15, Confianca = Alta.  
Notas_codificador: "ANOVA F(2,45)=8.32, p<0.001. Diversidade Shannon maior em sistemas tradicionais."

### 5.3 Tier T3 (94 registros) â€” Resultados sem estatÃ­sticas formais

Maior grupo. O estudo reporta resultados com tabelas, comparaÃ§Ãµes e dados descritivos, mas sem testes de hipÃ³tese formais.

1. **Abrir o PDF** e ler seÃ§Ã£o de resultados focando na dimensÃ£o/proxy atribuÃ­dos.
2. **Identificar a comparaÃ§Ã£o principal:** buscar diferenÃ§as entre grupos (tradicional vs. convencional, antes vs. depois, jovens vs. idosos, etc.).
3. **Avaliar a direÃ§Ã£o:** a vulnerabilidade aumentou, diminuiu ou ficou estÃ¡vel?
4. **Avaliar a intensidade:**
   - Se hÃ¡ nÃºmeros nas tabelas, calcular a diferenÃ§a relativa:
     - < 20% de diferenÃ§a â†’ Intensidade 1
     - 20â€“50% de diferenÃ§a â†’ Intensidade 2
     - > 50% de diferenÃ§a â†’ Intensidade 3
   - Se nÃ£o hÃ¡ nÃºmeros, usar o tom narrativo (ver SeÃ§Ã£o 4.2).
5. **Extrair n** das seÃ§Ãµes de mÃ©todos, tabelas ou legendas de figuras.
6. **Documentar** nas Notas_codificador o trecho ou tabela que sustenta a codificaÃ§Ã£o.

**Exemplo:**  
*Romero-Silva M.J. (2026)*, V1 (Erosao Intergeracional).  
O revisor lÃª os resultados e encontra uma tabela mostrando que comunidades com prÃ¡ticas tradicionais manejam 42 espÃ©cies vs. 18 em comunidades sem tradiÃ§Ã£o (diferenÃ§a de 133%).  
CodificaÃ§Ã£o: Direcao = âˆ’1, Intensidade = 3, n_T = 85, n_C = 45, Confianca = Moderada.  
Notas_codificador: "Tabela 3. Riqueza de espÃ©cies: tradicional=42, convencional=18. DiferenÃ§a > 100%."

### 5.4 Tier T4 (31 registros) â€” Qualitativo puro

O estudo apresenta apenas narrativa, sem nÃºmeros ou tabelas quantitativas. A codificaÃ§Ã£o Ã© inteiramente interpretativa.

1. **Abrir o PDF** e ler abstract, resultados e discussÃ£o.
2. **Identificar se o estudo aborda** a dimensÃ£o/proxy atribuÃ­dos (pode ser tangencial).
3. **Codificar direÃ§Ã£o e intensidade** com base exclusiva no texto narrativo.
4. **ConfianÃ§a serÃ¡ geralmente** Moderada ou Baixa.
5. **Documentar extensivamente** nas Notas_codificador, citando trechos do texto original.

**Exemplo:**  
*Calvet-Mir L. (2016)*, V1 (Erosao Intergeracional).  
O revisor lÃª o artigo e encontra a conclusÃ£o: "Traditional home gardens maintained significantly higher crop diversity compared to market-oriented production systems."  
CodificaÃ§Ã£o: Direcao = âˆ’1, Intensidade = 2, Confianca = Baixa.  
Notas_codificador: "ConclusÃ£o afirma diversidade maior em jardins tradicionais. Sem dados numÃ©ricos. 'Significantly' usado no sentido coloquial, nÃ£o estatÃ­stico."

---

## 6. Procedimento Dupla-Cega e ConcordÃ¢ncia

### 6.1 Fase 1 â€” CodificaÃ§Ã£o independente

1. Cada revisor (R1 e R2) recebe uma **cÃ³pia separada** da planilha `bd_codificacao_qualitativa.xlsx`.
2. Cada um preenche **todos os 199 registros** de forma independente, sem consultar o outro revisor.
3. Ao preencher, cada revisor marca na coluna Revisor seu identificador (R1 ou R2).
4. Manter um **log de tempo** aproximado: Ã© esperado entre 5â€“10 minutos por registro para T2a/T2b e 10â€“20 minutos para T3/T4.

### 6.2 Fase 2 â€” CÃ¡lculo de concordÃ¢ncia

ApÃ³s ambos os revisores concluÃ­rem, calcular a concordÃ¢ncia inter-avaliadores usando o **kappa de Cohen (Îº)** para as duas variÃ¡veis ordinais.

**Kappa para DireÃ§Ã£o do Efeito** (variÃ¡vel com 3 categorias: âˆ’1, 0, +1):

$$\kappa = \frac{P_o - P_e}{1 - P_e}$$

onde $P_o$ Ã© a proporÃ§Ã£o de concordÃ¢ncia observada e $P_e$ Ã© a proporÃ§Ã£o de concordÃ¢ncia esperada ao acaso.

**Kappa ponderado para Intensidade** (variÃ¡vel ordinal com 3 nÃ­veis: 1, 2, 3):

Usar Îº ponderado quadrÃ¡tico, que atribui pesos proporcionais Ã  distÃ¢ncia entre categorias discordantes.

**Limiares de aceitaÃ§Ã£o:**

| Îº | InterpretaÃ§Ã£o | AÃ§Ã£o |
|---|---------------|------|
| â‰¥ 0.81 | Quase perfeita | Aceitar. Resolver discordÃ¢ncias residuais por consenso. |
| 0.61â€“0.80 | Substancial | Aceitar. Resolver discordÃ¢ncias em reuniÃ£o de consenso. |
| 0.41â€“0.60 | Moderada | Revisar protocolo. Recalibrar com 20 registros de treino e recodificar os discordantes. |
| â‰¤ 0.40 | Fraca ou pobre | Parar. Revisar critÃ©rios, treinar e reiniciar codificaÃ§Ã£o. |

**Meta mÃ­nima:** Îº â‰¥ 0.61 antes de prosseguir para a conversÃ£o.

### 6.3 Fase 3 â€” Consenso

1. Gerar uma planilha de discordÃ¢ncias contendo apenas os registros onde R1 â‰  R2 em Direcao ou Intensidade.
2. Para cada discordÃ¢ncia, ambos os revisores discutem e chegam a um valor de consenso.
3. A versÃ£o final (consensuada) Ã© salva como a definitiva na planilha.
4. Se a discordÃ¢ncia persistir, um terceiro revisor (ou o pesquisador sÃªnior) decide.

### 6.4 Script para cÃ¡lculo do kappa

```python
# Calcular kappa de Cohen para duas listas de codificaÃ§Ã£o
def cohen_kappa(r1, r2):
    """r1 e r2 sÃ£o listas com os valores codificados por cada revisor."""
    from collections import Counter
    n = len(r1)
    assert n == len(r2)
    
    categories = sorted(set(r1) | set(r2))
    
    # ConcordÃ¢ncia observada
    po = sum(1 for a, b in zip(r1, r2) if a == b) / n
    
    # ConcordÃ¢ncia esperada
    count1 = Counter(r1)
    count2 = Counter(r2)
    pe = sum((count1[c] / n) * (count2[c] / n) for c in categories)
    
    kappa = (po - pe) / (1 - pe) if pe < 1 else 1.0
    return kappa, po, pe

# Uso:
# direcao_r1 = [+1, -1, 0, +1, -1, ...]  (lista de 199 valores)
# direcao_r2 = [+1, -1, +1, +1, -1, ...]
# k, po, pe = cohen_kappa(direcao_r1, direcao_r2)
# print(f"Îº = {k:.3f}, Po = {po:.3f}, Pe = {pe:.3f}")
```

---

## 7. Fluxo de Trabalho Completo

```
   â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
   â”‚  FASE 0 â€” PreparaÃ§Ã£o                                    â”‚
   â”‚  â€¢ Script 30 jÃ¡ executado â†’ bd_codificacao_qualitativa   â”‚
   â”‚  â€¢ Duplicar planilha: cÃ³pia_R1.xlsx e cÃ³pia_R2.xlsx     â”‚
   â”‚  â€¢ Calibrar com 10 registros-piloto juntos               â”‚
   â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
                           â”‚
   â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â–¼â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
   â”‚  FASE 1 â€” CodificaÃ§Ã£o Independente (R1 e R2)            â”‚
   â”‚  â€¢ 199 registros Ã— 7 campos amarelos                    â”‚
   â”‚  â€¢ Tempo estimado: 25â€“40 horas por revisor              â”‚
   â”‚  â€¢ Priorizar T2a (mais rÃ¡pidos) â†’ T3 â†’ T2b â†’ T4        â”‚
   â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
                           â”‚
   â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â–¼â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
   â”‚  FASE 2 â€” ConcordÃ¢ncia                                  â”‚
   â”‚  â€¢ Mesclar planilhas R1 + R2                             â”‚
   â”‚  â€¢ Calcular Îº (direÃ§Ã£o) e Îº_w (intensidade)             â”‚
   â”‚  â€¢ Se Îº < 0.61 â†’ recalibrar e recodificar               â”‚
   â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
                           â”‚
   â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â–¼â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
   â”‚  FASE 3 â€” Consenso                                      â”‚
   â”‚  â€¢ Resolver discordÃ¢ncias (reuniÃ£o presencial/remota)    â”‚
   â”‚  â€¢ Salvar versÃ£o final em bd_codificacao_qualitativa     â”‚
   â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
                           â”‚
   â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â–¼â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
   â”‚  FASE 4 â€” ConversÃ£o Automatizada                        â”‚
   â”‚  â€¢ Executar: python 31_converter_quali_para_lnRR.py     â”‚
   â”‚  â€¢ SaÃ­da: bd_extracao_convertido.xlsx                    â”‚
   â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
                           â”‚
   â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â–¼â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
   â”‚  FASE 5 â€” Meta-AnÃ¡lise                                  â”‚
   â”‚  â€¢ Executar: Rscript 02b_integrar_evidencia_mista.R     â”‚
   â”‚  â€¢ Executar: Rscript 03b_modelo_bayesiano_brms.R        â”‚
   â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
```

---

## 8. Regras de DecisÃ£o para Casos AmbÃ­guos

### 8.1 O estudo nÃ£o aborda a dimensÃ£o atribuÃ­da
Se o estudo claramente nÃ£o trata da dimensÃ£o V1â€“V6 indicada na coluna `Dimensao`, codificar como **Direcao = 0, Intensidade = 1, Confianca = Baixa** e anotar nas Notas_codificador: "Estudo nÃ£o aborda esta dimensÃ£o de forma direta."

### 8.2 MÃºltiplas comparaÃ§Ãµes no mesmo estudo/dimensÃ£o
Se o artigo reporta vÃ¡rias comparaÃ§Ãµes dentro da mesma dimensÃ£o (ex.: diversidade por gÃªnero E por faixa etÃ¡ria), codificar a **comparaÃ§Ã£o que mais diretamente testa o efeito sobre a vulnerabilidade**. Anotar qual comparaÃ§Ã£o foi selecionada e quais foram descartadas.

### 8.3 Resultados mistos (parte favorÃ¡vel, parte desfavorÃ¡vel)
Codificar o **resultado predominante** descrito pelo prÃ³prio autor na seÃ§Ã£o de discussÃ£o/conclusÃ£o. Se equilibrado, codificar como **Direcao = 0** com justificativa.

### 8.4 Artigo nÃ£o acessÃ­vel / paywall
Se o DOI nÃ£o dÃ¡ acesso ao texto completo e o abstract Ã© insuficiente, **nÃ£o codificar** (deixar Direcao em branco). Anotar "Sem acesso ao texto completo" nas Notas.

### 8.5 DÃºvida sobre a direÃ§Ã£o da vulnerabilidade
Quando o indicador aumenta mas a vulnerabilidade pode tanto aumentar quanto diminuir dependendo da interpretaÃ§Ã£o, consultar a definiÃ§Ã£o da dimensÃ£o (SeÃ§Ã£o 3 deste protocolo) e priorizar a interpretaÃ§Ã£o que o autor expressa. Em caso de ambiguidade genuÃ­na, usar Direcao = 0 e Confianca = Baixa.

---

## 9. CalibraÃ§Ã£o PrÃ©via (Treino)

Antes de iniciar a codificaÃ§Ã£o dos 199 registros, R1 e R2 devem:

1. **Ler este protocolo na Ã­ntegra.**
2. **Ler a aba INSTRUCOES** da planilha `bd_codificacao_qualitativa.xlsx`.
3. **Codificar conjuntamente 10 registros-piloto** (sugestÃ£o: 3 de T2a, 2 de T2b, 3 de T3, 2 de T4), discutindo cada decisÃ£o atÃ© chegar a consenso.
4. **Verificar o alinhamento:** se durante o piloto houver discordÃ¢ncia em mais de 3 dos 10 registros, revisar os critÃ©rios antes de prosseguir.

---

## 10. O que Acontece com os Dados Codificados

ApÃ³s a codificaÃ§Ã£o final (consensuada), o script `31_converter_quali_para_lnRR.py` executa as seguintes conversÃµes:

**T2a (p â†’ lnRR):**
$$p \xrightarrow{\Phi^{-1}} z \xrightarrow{\text{Borenstein}} d \xrightarrow{\text{Hasselblad}} lnOR \xrightarrow{\text{Zhang\&Yu}} lnRR$$

com inflaÃ§Ã£o de variÃ¢ncia $\sigma_{conv}^2 = 0.15^2$

**T2b (threshold â†’ lnRR):**
Mesma cadeia, usando $p = 0.05$ (intensidade 2â€“3) ou $p = 0.10$ (intensidade 1) como threshold conservador.  
InflaÃ§Ã£o: $\sigma_{conv}^2 = 0.25^2$

**T3 (ordinal â†’ lnRR):**
$$\text{(DireÃ§Ã£o} \times \text{Intensidade)} \rightarrow lnOR_{logit} \rightarrow lnRR$$

Mapeamento logit-normal: intensidade 1 â†’ lnOR = âˆ’0.405, intensidade 2 â†’ lnOR = +0.405, intensidade 3 â†’ lnOR = +1.386  
InflaÃ§Ã£o: $\sigma_{conv}^2 = 0.35^2$

**T4 (qualitativo â†’ lnRR):**
Mesma conversÃ£o ordinal, com inflaÃ§Ã£o adicional: $\sigma_{conv}^2 = 0.50^2$ e fator multiplicativo de 1.5 sobre a variÃ¢ncia.

A inflaÃ§Ã£o de variÃ¢ncia garante que registros convertidos recebem **peso menor** na meta-anÃ¡lise hierÃ¡rquica, proporcional Ã  incerteza da conversÃ£o. T1 (sem inflaÃ§Ã£o) sempre domina a estimativa quando disponÃ­vel.

---

## 11. Checklist Final do Revisor

Antes de entregar a planilha preenchida, verificar:

- [ ] Todos os 199 registros possuem valor em Direcao_efeito (âˆ’1, 0 ou +1)
- [ ] Todos os 199 registros possuem valor em Intensidade (1, 2 ou 3)
- [ ] Coluna Revisor preenchida em todos (R1 ou R2)
- [ ] Coluna Confianca preenchida em todos (Alta, Moderada ou Baixa)
- [ ] Registros T2a: verificar se a Direcao Ã© coerente com os p-values listados
- [ ] Registros T2b: anotar p-value extraÃ­do manualmente nas Notas (quando possÃ­vel)
- [ ] Registros T3: anotar o trecho/tabela que sustenta a codificaÃ§Ã£o
- [ ] Registros T4: justificar a codificaÃ§Ã£o nas Notas (especialmente se Intensidade = 3)
- [ ] n_T e n_C preenchidos sempre que extraÃ­veis do texto
- [ ] Nenhum campo das colunas Aâ€“L foi alterado (dados automÃ¡ticos)

---

## 12. ReferÃªncias MetodolÃ³gicas

- Borenstein, M. et al. (2009). *Introduction to Meta-Analysis*. Cap. 7: Converting among effect sizes.
- Hasselblad, V. & Hedges, L.V. (1995). Meta-analysis of screening and diagnostic tests. *Psychological Bulletin*, 117(1), 167â€“178.
- Zhang, J. & Yu, K.F. (1998). What's the relative risk? A method of correcting the odds ratio in cohort studies. *JAMA*, 280(19), 1690â€“1691.
- Lajeunesse, M.J. (2011). On the meta-analysis of response ratios for studies with correlated and multi-group designs. *Ecology*, 92(11), 2049â€“2055.
- Cohen, J. (1960). A coefficient of agreement for nominal scales. *Educational and Psychological Measurement*, 20(1), 37â€“46.

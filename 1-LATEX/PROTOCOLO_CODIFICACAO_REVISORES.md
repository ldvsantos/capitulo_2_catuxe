# Protocolo de Codificação de Evidência Qualitativa e Semi-Quantitativa

## Revisão Sistemática e Meta-Análise → Artigo 2 (Catuxe)

**Versão:** 1.0  
**Data:** 2 de março de 2026  
**Responsável:** Diego Vidal  
**Arquivo de trabalho:** `bd_codificacao_qualitativa.xlsx` (aba CODIFICACAO)  
**Registros para codificação:** 199  
---

## 1. Objetivo

Este protocolo instrui dois revisores independentes (R1 e R2) a codificar registros de estudos primários que não possuem dados quantitativos completos (média, desvio-padrão e n para ambos os grupos). Cada registro corresponde a uma comparação entre um grupo/condição de tratamento (sistemas tradicionais, intervenções de salvaguarda) e um grupo/condição de controle ou referência, avaliada em uma das **oito dimensões de vulnerabilidade biocultural (V1–V8)**.

As cinco primeiras dimensões (V1–V5) referem-se à arquitetura original, já codificada (199 registros). As três dimensões adicionais (V6–V8) — Vitalidade Linguística, Integração ao Mercado e Exposição Climática — foram incorporadas na reestruturação V1–V8 e requerem codificação de 48 registros cada (144 novos registros no total).

A codificação converte a evidência narrativa em dois valores numéricos (direção e intensidade do efeito) que serão posteriormente transformados em tamanhos de efeito (lnRR) pelo script de conversão automatizado. A qualidade desta codificação determina diretamente a robustez da meta-análise.

### 1.1 Definição operacional de grupo de referência por tier de evidência

A definição do grupo de referência (controle) varia conforme a completude dos dados reportados pelo estudo primário:

| Tier | Grupo de referência | Exemplo |
|------|---------------------|---------|
| **T1** | Explícito: comunidades sem intervenção formal, condições pré-intervenção (antes-depois) ou grupo controle com médias ($\bar{X}_C$), desvios-padrão ($SD_C$) e tamanhos amostrais ($n_C$) reportados. | Estudo compara riqueza de espécies em comunidades com programa vs. sem programa, reportando média ± SD para ambos. |
| **T2a/T2b** | Embutido na estatística de teste: o contraste entre grupos já está codificado no p-value ou estatística F/H reportados. O revisor identifica a direção, mas o grupo controle é o benchmark implícito do teste do estudo original. | Estudo reporta ANOVA com p < 0.01 comparando diversidade entre sistemas tradicionais e convencionais. |
| **T3** | Inferido pelo codificador: o estudo apresenta dados descritivos (tabelas, contagens, percentuais) sem teste estatístico, e o revisor julga a direção da mudança comparando subgrupos ou períodos contrastantes dentro do estudo. | Estudo tabula espécies conhecidas por jovens vs. idosos sem teste de hipótese. |
| **T4** | Condição neutra inferida: o estudo reporta apenas narrativa qualitativa, e o revisor julga a direção da mudança contra uma condição de referência implícita no contexto (estabilidade, ausência de pressão, continuidade do sistema). | Autores descrevem "declínio acentuado" de práticas sem dados numéricos. O codificador julga +1 (agravamento) contra o referencial de estabilidade. |

### 1.2 Convenção de sinal do lnRR

A direção codificada (+1, 0, −1) opera como multiplicador escalar sobre a magnitude absoluta do tamanho de efeito. Após as conversões multi-tier, o lnRR resultante preserva a interpretação direcional:

| lnRR | Interpretação | Posição no forest plot |
|------|---------------|------------------------|
| **> 0** (positivo) | O grupo exposto apresenta indicadores de vulnerabilidade **superiores** ao grupo de referência → **agravamento** | À direita do zero |
| **= 0** | Sem efeito detectável | No zero |
| **< 0** (negativo) | O grupo exposto apresenta indicadores mais favoráveis → **efeito protetor** (redução de vulnerabilidade) | À esquerda do zero |

O sinal não tem interpretação fixa universal — reflete a convenção de codificação deste protocolo (Dir = +1 para agravamento, Dir = −1 para proteção). A significância estatística é determinada pelo intervalo de confiança (IC 95% que não cruza o zero).

---

## 2. Contexto do Banco de Dados

### 2.1 Classificação dos registros por tier de evidência

| Tier | Descrição | Registros | O que o revisor precisa fazer |


|------|-----------|:---------:|-------------------------------|


| **T1** | Quantitativo completo (n, média, SD para ambos os grupos) | 17 | Nada. Já processados automaticamente. |


| **T2a** | Possui p-values numéricos extraídos do texto | 49 | Codificar **direção** do efeito e extrair **n** se possível. Intensidade é derivada do p-value. |


| **T2b** | Possui ANOVA/Kruskal-Wallis mas sem p-value explícito | 25 | Codificar **direção**, **intensidade** e extrair **n** se possível. |


| **T3** | Resultados reportados (tabelas, comparações) sem estatísticas formais | 94 | Codificar **direção**, **intensidade** e extrair **n** se possível. |


| **T4** | Qualitativo puro (narrativa, sem dados numéricos) | 31 | Codificar **direção**, **intensidade**. Tamanho amostral raramente disponível. |


| EX | Sem acesso ao artigo ou sem resultados | 72 | Excluídos. Não codificar. |

### 2.2 Distribuição por dimensão (apenas registros para codificação)

| Dimensão | Código | T2a | T2b | T3 | T4 | Total |


|----------|:------:|:---:|:---:|:--:|:--:|:-----:|


| Erosão Intergeracional e Migração | V1 | 8 | 4 | 16 | 5 | 33 |


| Complexidade e Singularidade Biocultural | V2 | 17 | 9 | 30 | 10 | 66 |


| Status de Documentação | V3 | 8 | 4 | 16 | 6 | 34 |


| Vulnerabilidade Jurídica e Fundiária | V4 | 8 | 4 | 16 | 5 | 33 |


| Organização Social e Governança | V5 | 8 | 4 | 16 | 5 | 33 |


| Vitalidade Linguística | V6 | — | — | — | 48 | 48 |


| Integração ao Mercado | V7 | — | — | — | 48 | 48 |


| Exposição Climática | V8 | — | — | — | 48 | 48 |

> **Nota:** V2 agrega as antigas dimensões V2 (Complexidade Biocultural) e V3 (Singularidade Territorial), tratadas como dois proxies dentro de uma única dimensão. V6, V7 e V8 iniciam como T4 (classificação provisória); o revisor deve reclassificar o Tier com base no conteúdo do artigo.

---

## 3. Definição das Dimensões de Vulnerabilidade

Antes de codificar, o revisor deve compreender o que cada dimensão mede e o que constitui agravamento vs. redução de vulnerabilidade. A arquitetura contempla **oito dimensões (V1–V8)**, organizadas em dois blocos: V1–V5 (dimensões endógenas ao sistema biocultural) e V6–V8 (dimensões exógenas ou de interface com pressões externas).

---

### V1 – Erosão Intergeracional e Migração

**O que mede:** riqueza e diversidade de variedades locais, espécies cultivadas e manejadas, considerando processos de erosão genética associados à migração, urbanização e abandono do campo.

**Indicadores típicos:** índice de Shannon (H'), riqueza de espécies, contagem de variedades locais (landraces), taxa de retenção de germoplasma tradicional, proporção de agricultores que mantêm cultivares autóctones.

| Direção | Critério operacional |

|:-------:|---------------------|

| **+1** (agravamento) | Redução de diversidade, perda de variedades locais, substituição por monocultura ou cultivares melhorados, simplificação do sistema, migração de jovens reduzindo a base de manejo. |

| **0** (neutro) | Sem diferença detectável entre grupos/períodos, ou estudo não aborda diretamente esta dimensão. |

| **−1** (redução) | Aumento de diversidade, conservação in situ bem-sucedida, recuperação de variedades perdidas, retorno de migrantes com reinserção no manejo tradicional. |

---

### V2 – Complexidade e Singularidade Biocultural

**O que mede:** esta dimensão integra dois eixos complementares: (a) a continuidade da transferência vertical de conhecimento entre gerações (complexidade) e (b) a exclusividade geográfica e cosmológica das práticas, isto é, a riqueza de interações ecológicas codificadas nos sistemas locais (singularidade). Na base de dados, cada estudo contribui com dois proxies (um para cada eixo), tratados como observações correlacionadas dentro da mesma dimensão.

**Indicadores típicos:** knowledge scores por faixa etária, frequência de eventos de transmissão, proporção de jovens com domínio do saber, beta-diversidade entre comunidades (Jaccard, Bray-Curtis), taxa de endemismo de variedades, complexidade da cadeia operatória.

| Direção | Critério operacional |

|:-------:|---------------------|

| **+1** (agravamento) | Queda no knowledge score dos jovens em comparação a idosos, redução de eventos de transmissão, abandono de práticas pedagógicas tradicionais, homogeneização entre comunidades, perda de singularidade, simplificação de práticas complexas. |

| **0** (neutro) | Sem diferença detectável entre gerações ou comunidades, ou estudo não aborda diretamente esta dimensão. |

| **−1** (redução) | Jovens demonstram conhecimento equivalente ou crescente, programas de mentoria ativos, eventos de transmissão frequentes, manutenção de práticas distintas entre comunidades, alta beta-diversidade, preservação de saberes únicos. |

**Nota sobre proxies:** ao codificar V2, o revisor deve avaliar separadamente o eixo de complexidade (transferência de conhecimento) e o eixo de singularidade (exclusividade territorial). Se um artigo reporta dados sobre ambos, cada proxy recebe sua própria codificação de direção e intensidade.

---

### V3 – Status de Documentação

**O que mede:** capacidade dos sistemas tradicionais de prover autonomia alimentar e nutricional, e grau em que esse conhecimento alimentar está documentado e acessível.

**Indicadores típicos:** diversidade dietética, autossuficiência alimentar, contagem de espécies alimentícias utilizadas, segurança alimentar avaliada por escalas padronizadas (FIES, HDDS), presença de registros formais de usos alimentares.

| Direção | Critério operacional |

|:-------:|---------------------|

| **+1** (agravamento) | Redução na diversidade dietética, dependência crescente de alimentos industrializados, abandono de cultivos alimentícios tradicionais, perda de conhecimento sobre espécies comestíveis silvestres. |

| **0** (neutro) | Sem diferença detectável entre grupos/períodos, ou estudo não aborda diretamente esta dimensão. |

| **−1** (redução) | Manutenção ou aumento da diversidade alimentar, contribuição significativa à dieta a partir de espécies locais, soberania alimentar, documentação ativa de usos alimentares tradicionais. |

---

### V4 – Vulnerabilidade Jurídica e Fundiária

**O que mede:** grau de registro formal dos saberes em inventários, acervos e bases de dados, estabilidade dos direitos fundiários e territoriais das comunidades, e proteção legal do patrimônio biocultural.

**Indicadores típicos:** contagem de saberes inventariados, completude de fichas técnicas, taxa de digitalização, existência de marco regulatório (indicações geográficas, registros de patrimônio), segurança da posse da terra.

| Direção | Critério operacional |

|:-------:|---------------------|

| **+1** (agravamento) | Saberes sem registro, perda de documentação existente, ausência de inventário, risco de desaparecimento sem registro, insegurança fundiária, sobreposição de territórios com concessões extrativistas, ausência de proteção legal. |

| **0** (neutro) | Sem diferença detectável, ou estudo não aborda diretamente esta dimensão. |

| **−1** (redução) | Inventariamento ativo, bases de dados comunitárias, documentação em vídeo/áudio, fichas completas, demarcação territorial concluída, indicações geográficas obtidas, marco regulatório implementado. |

---

### V5 – Organização Social e Governança

**O que mede:** vitalidade das estruturas comunitárias de ensino, governança, gestão do conhecimento e ação coletiva para conservação biocultural.

**Indicadores típicos:** número de mestres de saberes ativos, existência de protocolos comunitários de consulta prévia, frequência de ações coletivas (mutirões, festas, rituais), densidade de associações e cooperativas locais, capacidade de auto-regulação do acesso a recursos.

| Direção | Critério operacional |

|:-------:|---------------------|

| **+1** (agravamento) | Desarticulação social, ausência de governança, mestres sem sucessores, colapso de instituições comunitárias, conflitos internos não mediados, dependência exclusiva de governança externa. |

| **0** (neutro) | Sem diferença detectável, ou estudo não aborda diretamente esta dimensão. |

| **−1** (redução) | Governança ativa, protocolos comunitários funcionais, lideranças reconhecidas e em processo de sucessão, ação coletiva efetiva, parcerias institucionais que fortalecem a autonomia. |

---

### V6 – Vitalidade Linguística

**O que mede:** grau de uso, transmissão e vitalidade das línguas e terminologias indígenas ou locais associadas ao manejo biocultural. A perda linguística é um indicador-chave de vulnerabilidade biocultural porque a maior parte do conhecimento ecológico tradicional é transmitida oralmente e codificada em etnotaxonomias vernaculares.

**Indicadores típicos:** número de falantes, grau de uso da língua indígena vs. língua dominante por faixa etária, escala EGIDS (Expanded Graded Intergenerational Disruption Scale), riqueza de etnotaxonomias (folk taxa), índice VITEK (Vitality Index of Traditional Ecological Knowledge) quando disponível, presença de programas de educação bilíngue, proporção de nomes vernaculares retidos para espécies manejadas.

| Direção | Critério operacional |

|:-------:|---------------------|

| **+1** (agravamento) | Perda ou declínio de língua indígena/local, substituição por língua franca, redução do número de falantes (especialmente entre jovens), erosão de etnotaxonomias (nomes vernaculares desconhecidos pelas novas gerações), ausência de educação bilíngue, monolinguismo crescente na língua dominante. |

| **0** (neutro) | Estudo menciona contexto linguístico sem relatar mudança, ou não aborda diretamente vitalidade linguística. |

| **−1** (redução) | Programas de revitalização linguística ativos, educação bilíngue implementada, manutenção de terminologias etnotaxonômicas, diversidade linguística preservada, documentação ativa de vocabulário ecológico vernacular, jovens demonstrando domínio de nomenclatura local. |

**Atenção:** muitos estudos de etnobotânica reportam nomes locais de plantas sem avaliar a vitalidade linguística em si. Se o artigo apenas lista nomes vernaculares como dado de inventário, sem discutir se esses nomes estão sendo perdidos ou mantidos, codificar como **Direção = 0** com Confiança = Baixa.

---

### V7 – Integração ao Mercado

**O que mede:** grau em que a integração a mercados formais e cadeias globais de valor altera (positiva ou negativamente) os sistemas bioculturais. A integração ao mercado pode ser um vetor de vulnerabilidade (quando substitui variedades locais por comerciais) ou de proteção (quando valoriza produtos tradicionais via nichos diferenciados).

**Indicadores típicos:** proporção de renda agrícola proveniente de mercados formais, taxa de substituição de cultivares locais por variedades comerciais/híbridas, presença de indicações geográficas ou certificações (fair trade, orgânico), distância ao mercado, proporção de produção destinada à subsistência vs. venda, diversificação de meios de vida (on-farm vs. off-farm income).

| Direção | Critério operacional |

|:-------:|---------------------|

| **+1** (agravamento) | Penetração de mercado levando à substituição de variedades locais por comerciais/híbridas, abandono de cultivos de subsistência em favor de cash crops, dependência crescente de insumos externos, perda de autonomia produtiva, homogeneização de paisagens agrícolas por pressão comercial. |

| **0** (neutro) | Estudo menciona mercado sem relatar efeito direcional sobre o sistema biocultural, ou coexistência estável entre produção comercial e tradicional sem evidência de substituição. |

| **−1** (redução) | Acesso a mercados de nicho que valorizam produtos tradicionais (fair trade, indicação geográfica, mercados orgânicos), geração de renda que subsidia a manutenção de variedades locais, associações de produtores que protegem germoplasma, cadeia de valor que incentiva diversidade. |

**Atenção:** a direção da vulnerabilidade depende do **tipo** de integração, não de sua intensidade per se. Maior integração com substituição = +1. Maior integração com valorização = −1. O revisor deve avaliar o efeito líquido descrito pelo autor.

---

### V8 – Exposição Climática

**O que mede:** grau em que mudanças e variabilidade climáticas afetam os sistemas bioculturais, e capacidade de adaptação das comunidades baseada em conhecimento ecológico tradicional. Eventos climáticos extremos podem destruir germoplasma, alterar calendários agrícolas e invalidar indicadores fenológicos tradicionais.

**Indicadores típicos:** frequência e severidade de eventos extremos (secas, enchentes, geadas atípicas), mudanças observadas em regimes de precipitação e temperatura, perda de safras atribuída ao clima, capacidade de previsão climática com base em indicadores tradicionais (bioindicadores, fenologia, astronomia), presença de estratégias de adaptação (diversificação de espécies, escalonamento de plantio, irrigação baseada em saberes locais).

| Direção | Critério operacional |

|:-------:|---------------------|

| **+1** (agravamento) | Impactos climáticos afetando negativamente práticas tradicionais, perda de safras por clima extremo, invalidação de calendários tradicionais por mudanças no regime pluviométrico, abandono de cultivares sensíveis, migração forçada por degradação climática. |

| **0** (neutro) | Estudo menciona contexto climático sem relatar efeito direcional sobre o sistema biocultural, ou clima tratado apenas como variável de controle sem avaliação de impacto. |

| **−1** (redução) | Conhecimento ecológico tradicional funcionando como estratégia de adaptação climática, indicadores etno-meteorológicos válidos, práticas tradicionais de manejo hídrico eficazes, diversificação como buffer contra variabilidade climática, resiliência demonstrada diante de eventos extremos. |

**Atenção:** a direção refere-se ao efeito sobre a **vulnerabilidade do sistema biocultural**, não à vulnerabilidade climática genérica. Se o artigo discute vulnerabilidade climática de populações rurais sem conectá-la à perda ou manutenção de conhecimento/práticas bioculturais, codificar como **Direção = 0** com Confiança = Baixa.

---

## 4. Campos a Preencher na Planilha

A aba CODIFICACAO contém 19 colunas. As colunas com fundo **amarelo** devem ser preenchidas pelo revisor. As demais são preenchidas automaticamente e não devem ser alteradas.

### 4.1 Direcao_efeito (OBRIGATÓRIO)

Indica se a intervenção/condição de tratamento **agrava ou reduz** a vulnerabilidade na dimensão atribuída.

| Valor | Significado | Quando usar |


|:-----:|-------------|-------------|


| **+1** | Vulnerabilidade **agravada** | O indicador piorou no grupo tratamento em relação ao controle, OU a comparação temporal mostra deterioração. |


| **0** | **Neutro** / sem diferença | Nenhuma diferença perceptível entre grupos, ou o estudo reporta explicitamente ausência de efeito. |


| **−1** | Vulnerabilidade **reduzida** | O indicador melhorou no grupo tratamento em relação ao controle, OU a comparação temporal mostra melhoria. |

**ATENÇÃO CRÍTICA:** A direção refere-se à **vulnerabilidade**, não ao indicador bruto. Por exemplo:


- Aumento de diversidade de espécies → redução de vulnerabilidade → **−1**


- Aumento de knowledge score em jovens → redução de vulnerabilidade → **−1**


- Perda de variedades locais → agravamento de vulnerabilidade → **+1**


- Redução de eventos de transmissão → agravamento de vulnerabilidade → **+1**

### 4.2 Intensidade (OBRIGATÓRIO)

Magnitude percebida do efeito, avaliada pelo revisor com base no conteúdo do artigo original.

| Valor | Categoria | Critérios para atribuição |


|:-----:|-----------|--------------------------|


| **1** | Fraca | Diferença marginal, tendência sem significância, p > 0.10, autores descrevem o efeito como pequeno ou não significante. |


| **2** | Moderada | Diferença notável, significância estatística borderline ou moderada (p < 0.05), autores enfatizam o resultado como relevante. |


| **3** | Forte | Grande diferença, alta significância (p < 0.01), mudança qualitativa clara, autores descrevem como resultado principal do estudo. |

**Dicas para atribuição quando não há estatísticas formais (T3 e T4):**

- Use o **tom narrativo** do artigo: se os autores usam palavras como "drastic", "substantial", "complete loss", "dramatic decline" → intensidade 3.


- Se usam "some", "slight", "tendency", "marginal" → intensidade 1.


- Termos como "significant", "considerable", "important", "clear" → intensidade 2.


- Se o artigo apresenta tabelas com números (sem teste estatístico), avalie a magnitude da diferença relativa entre os grupos: diferença < 20% → 1, entre 20–50% → 2, acima de 50% → 3.


- Na dúvida, atribua intensidade 2 (moderada) como default conservador.

### 4.3 n_T_codificado (QUANDO DISPONÍVEL)

Tamanho amostral do grupo/condição de **tratamento** (intervenção, sistema tradicional, etc.) extraído do texto do artigo.

- Se o artigo reporta n total sem separar grupos, coloque n/2 em cada campo e anote nas Notas_codificador.


- Se não há informação amostral, deixe em branco (o script usará um fallback conservador de n=30 por grupo).


- Procure na seção "Methods", "Study area", "Sampling", "Data collection" ou nas legendas das tabelas.

### 4.4 n_C_codificado (QUANDO DISPONÍVEL)

Mesmo critério acima, para o grupo/condição de **controle** (convencional, sem intervenção, etc.).

### 4.5 Revisor (OBRIGATÓRIO)

Identificação do revisor: preencha **R1** ou **R2**.

### 4.6 Confianca_codificacao (OBRIGATÓRIO)

Grau de confiança do revisor na codificação atribuída.

| Valor | Significado |


|-------|-------------|


| **Alta** | Dados claros no texto, tabelas com números, ou estatísticas explícitas que sustentam a codificação sem ambiguidade. |


| **Moderada** | Inferido a partir de figuras, contexto narrativo ou combinação de indicadores indiretos. |


| **Baixa** | Interpretação subjetiva de narrativa qualitativa, sem dados numéricos de suporte. Pouca informação disponível no trecho relevante. |

### 4.7 Notas_codificador (OPCIONAL)

Campo livre para o revisor registrar justificativas, trechos do artigo que sustentam a decisão, dúvidas, ou qualquer observação relevante para a fase de consenso. Recomendado especialmente quando Confianca = Baixa.

---

## 5. Procedimento Operacional por Tier

### 5.1 Tier T2a (49 registros) – Estudos com p-values

Estes registros já possuem p-values extraídos automaticamente do texto (coluna `p_values_extraidos`). O que o revisor precisa fazer:

1. **Abrir o PDF** do artigo (use o DOI na coluna C para localizar).


2. **Localizar** a seção de resultados correspondente à dimensão e proxy atribuídos.


3. **Confirmar a direção:** o p-value é significativo, mas não indica se o efeito é positivo ou negativo. O revisor deve ler o contexto e determinar se a vulnerabilidade aumentou (+1) ou diminuiu (−1).


4. **Atribuir Intensidade** com base na magnitude reportada e no p-value:


   - p < 0.01 e efeito grande → 3


   - p < 0.05 e efeito moderado → 2


   - p < 0.10 ou efeito marginal → 1


5. **Extrair n** se possível (colunas n_T_codificado e n_C_codificado).


6. **Preencher** Revisor e Confianca.

**Exemplo:**  


*Bastos J.G. (2022)*, V1 (Erosao Intergeracional), Proxy: Plant species richness.  


p-values extraídos: 0.002, 0.021, 0.165, 0.260, 0.366.  


O revisor abre o artigo, identifica que p=0.002 refere-se à comparação "antes vs. depois" de uma intervenção de conservação que aumentou a riqueza de espécies.  


Codificação: Direcao = −1, Intensidade = 3, Confianca = Alta.

### 5.2 Tier T2b (25 registros) – Estudos com ANOVA/KW sem p-value explícito

O texto indica "[TEM_STAT]" ou "Has ANOVA/KW". O estudo fez análise estatística, mas o p-value específico não foi extraído automaticamente.

1. **Abrir o PDF** e localizar a tabela/seção de ANOVA ou Kruskal-Wallis.


2. **Extrair o p-value** manualmente se possível, e anotá-lo nas Notas_codificador.


3. Se não for possível extrair o p-value, codificar com base na significância reportada pelo autor:


   - Autor diz "significante" sem qualificar → Intensidade = 2


   - Autor diz "altamente significante" → Intensidade = 3


   - Autor diz "não significante" → Intensidade = 1


4. **Codificar direção** com base no sentido da diferença entre os grupos.


5. **Extrair n** quando disponível.

**Exemplo:**  


*Suwardi A.B. (2025)*, V1 (Erosao Intergeracional).  


Notas: "[TEM_STAT] | Has ANOVA/KW"  


O revisor abre o artigo, encontra ANOVA com F(2,45) = 8.32, p < 0.001, onde a diversidade é maior em sistemas tradicionais que em convencionais.  


Codificação: Direcao = −1, Intensidade = 3, n_T = 16, n_C = 15, Confianca = Alta.  


Notas_codificador: "ANOVA F(2,45)=8.32, p<0.001. Diversidade Shannon maior em sistemas tradicionais."

### 5.3 Tier T3 (94 registros) – Resultados sem estatísticas formais

Maior grupo. O estudo reporta resultados com tabelas, comparações e dados descritivos, mas sem testes de hipótese formais.

1. **Abrir o PDF** e ler seção de resultados focando na dimensão/proxy atribuídos.


2. **Identificar a comparação principal:** buscar diferenças entre grupos (tradicional vs. convencional, antes vs. depois, jovens vs. idosos, etc.).


3. **Avaliar a direção:** a vulnerabilidade aumentou, diminuiu ou ficou estável?


4. **Avaliar a intensidade:**


   - Se há números nas tabelas, calcular a diferença relativa:


     - < 20% de diferença → Intensidade 1


     - 20–50% de diferença → Intensidade 2


     - > 50% de diferença → Intensidade 3


   - Se não há números, usar o tom narrativo (ver Seção 4.2).


5. **Extrair n** das seções de métodos, tabelas ou legendas de figuras.


6. **Documentar** nas Notas_codificador o trecho ou tabela que sustenta a codificação.

**Exemplo:**  


*Romero-Silva M.J. (2026)*, V1 (Erosao Intergeracional).  


O revisor lê os resultados e encontra uma tabela mostrando que comunidades com práticas tradicionais manejam 42 espécies vs. 18 em comunidades sem tradição (diferença de 133%).  


Codificação: Direcao = −1, Intensidade = 3, n_T = 85, n_C = 45, Confianca = Moderada.  


Notas_codificador: "Tabela 3. Riqueza de espécies: tradicional=42, convencional=18. Diferença > 100%."

### 5.4 Tier T4 (31 registros) – Qualitativo puro

O estudo apresenta apenas narrativa, sem números ou tabelas quantitativas. A codificação é inteiramente interpretativa.

1. **Abrir o PDF** e ler abstract, resultados e discussão.


2. **Identificar se o estudo aborda** a dimensão/proxy atribuídos (pode ser tangencial).


3. **Codificar direção e intensidade** com base exclusiva no texto narrativo.


4. **Confiança será geralmente** Moderada ou Baixa.


5. **Documentar extensivamente** nas Notas_codificador, citando trechos do texto original.

**Exemplo:**  


*Calvet-Mir L. (2016)*, V1 (Erosao Intergeracional).  


O revisor lê o artigo e encontra a conclusão: "Traditional home gardens maintained significantly higher crop diversity compared to market-oriented production systems."  


Codificação: Direcao = −1, Intensidade = 2, Confianca = Baixa.  


Notas_codificador: "Conclusão afirma diversidade maior em jardins tradicionais. Sem dados numéricos. 'Significantly' usado no sentido coloquial, não estatístico."

---

## 6. Procedimento Dupla-Cega e Concordância

### 6.1 Fase 1 – Codificação independente

1. Cada revisor (R1 e R2) recebe uma **cópia separada** da planilha `bd_codificacao_qualitativa.xlsx`.


2. Cada um preenche **todos os 199 registros** de forma independente, sem consultar o outro revisor.


3. Ao preencher, cada revisor marca na coluna Revisor seu identificador (R1 ou R2).


4. Manter um **log de tempo** aproximado: é esperado entre 5−10 minutos por registro para T2a/T2b e 10–20 minutos para T3/T4.

### 6.2 Fase 2 – Cálculo de concordância

Após ambos os revisores concluírem, calcular a concordância inter-avaliadores usando o **kappa de Cohen (κ)** para as duas variáveis ordinais.

**Kappa para Direção do Efeito** (variável com 3 categorias: −1, 0, +1):

$$\kappa = \frac{P_o - P_e}{1 - P_e}$$

onde $P_o$ é a proporção de concordância observada e $P_e$ é a proporção de concordância esperada ao acaso.

**Kappa ponderado para Intensidade** (variável ordinal com 3 níveis: 1, 2, 3):

Usar κ ponderado quadrático, que atribui pesos proporcionais à distância entre categorias discordantes.

**Limiares de aceitação:**

| κ | Interpretação | Ação |


|---|---------------|------|


| ≥ 0.81 | Quase perfeita | Aceitar. Resolver discordâncias residuais por consenso. |


| 0.61–0.80 | Substancial | Aceitar. Resolver discordâncias em reunião de consenso. |


| 0.41–0.60 | Moderada | Revisar protocolo. Recalibrar com 20 registros de treino e recodificar os discordantes. |


| ≥ 0.40 | Fraca ou pobre | Parar. Revisar critérios, treinar e reiniciar codificação. |

**Meta mínima:** κ ≥ 0.61 antes de prosseguir para a conversão.

### 6.3 Fase 3 – Consenso

1. Gerar uma planilha de discordâncias contendo apenas os registros onde R1 ≥ R2 em Direcao ou Intensidade.


2. Para cada discordância, ambos os revisores discutem e chegam a um valor de consenso.


3. A versão final (consensuada) é salva como a definitiva na planilha.


4. Se a discordância persistir, um terceiro revisor (ou o pesquisador sênior) decide.

### 6.4 Script para cálculo do kappa

```python


# Calcular kappa de Cohen para duas listas de codificação


def cohen_kappa(r1, r2):


    """r1 e r2 são listas com os valores codificados por cada revisor."""


    from collections import Counter


    n = len(r1)


    assert n == len(r2)


    


    categories = sorted(set(r1) | set(r2))


    


    # Concordância observada


    po = sum(1 for a, b in zip(r1, r2) if a == b) / n


    


    # Concordância esperada


    count1 = Counter(r1)


    count2 = Counter(r2)


    pe = sum((count1[c] / n) * (count2[c] / n) for c in categories)


    


    kappa = (po - pe) / (1 - pe) if pe < 1 else 1.0


    return kappa, po, pe

# Uso:


# direcao_r1 = [+1, -1, 0, +1, -1, ...]  (lista de 199 valores)


# direcao_r2 = [+1, -1, +1, +1, -1, ...]


# k, po, pe = cohen_kappa(direcao_r1, direcao_r2)


# print(f"κ = {k:.3f}, Po = {po:.3f}, Pe = {pe:.3f}")


```

---

## 7. Fluxo de Trabalho Completo

```


   ≥


   →  FASE 0 → Preparação                                    →


   →  ≥ Script 30 já executado → bd_codificacao_qualitativa   →


   →  ≥ Duplicar planilha: cópia_R1.xlsx e cópia_R2.xlsx     →


   →  ≥ Calibrar com 10 registros-piloto juntos               →


   ≥


                           →


   ≥≥


   →  FASE 1 – Codificação Independente (R1 e R2)            →


   →  ≥ 199 registros ≥ 7 campos amarelos                    →


   →  ≥ Tempo estimado: 25–40 horas por revisor              →


   →  ≥ Priorizar T2a (mais rápidos) → T3 → T2b → T4        →


   ≥


                           →


   ≥≥


   →  FASE 2 → Concordância                                  →


   →  ≥ Mesclar planilhas R1 + R2                             →


   →  ≥ Calcular κ (direção) e κ_w (intensidade)             →


   →  ≥ Se κ < 0.61 → recalibrar e recodificar               →


   ≥


                           →


   ≥≥


   →  FASE 3 – Consenso                                      →


   →  ≥ Resolver discordâncias (reunião presencial/remota)    →


   →  ≥ Salvar versão final em bd_codificacao_qualitativa     →


   ≥


                           →


   ≥≥


   →  FASE 4 → Conversão Automatizada                        →


   →  ≥ Executar: python 31_converter_quali_para_lnRR.py     →


   →  ≥ Saída: bd_extracao_convertido.xlsx                    →


   ≥


                           →


   ≥≥


   →  FASE 5 → Meta-Análise                                  →


   →  ≥ Executar: Rscript 02b_integrar_evidencia_mista.R     →


   →  ≥ Executar: Rscript 03b_modelo_bayesiano_brms.R        →


   


```

---

## 8. Regras de Decisão para Casos Ambíguos

### 8.1 O estudo não aborda a dimensão atribuída


Se o estudo claramente não trata da dimensão V1–V8 indicada na coluna `Dimensao`, codificar como **Direcao = 0, Intensidade = 1, Confianca = Baixa** e anotar nas Notas_codificador: "Estudo não aborda esta dimensão de forma direta."

### 8.2 Múltiplas comparações no mesmo estudo/dimensão


Se o artigo reporta várias comparações dentro da mesma dimensão (ex.: diversidade por gênero E por faixa etária), codificar a **comparação que mais diretamente testa o efeito sobre a vulnerabilidade**. Anotar qual comparação foi selecionada e quais foram descartadas.

### 8.3 Resultados mistos (parte favorável, parte desfavorável)


Codificar o **resultado predominante** descrito pelo próprio autor na seção de discussão/conclusão. Se equilibrado, codificar como **Direcao = 0** com justificativa.

### 8.4 Artigo não acessível / paywall


Se o DOI não dá acesso ao texto completo e o abstract é insuficiente, **não codificar** (deixar Direcao em branco). Anotar "Sem acesso ao texto completo" nas Notas.

### 8.5 Dúvida sobre a direção da vulnerabilidade


Quando o indicador aumenta mas a vulnerabilidade pode tanto aumentar quanto diminuir dependendo da interpretação, consultar a definição da dimensão (Seção 3 deste protocolo) e priorizar a interpretação que o autor expressa. Em caso de ambiguidade genuína, usar Direcao = 0 e Confianca = Baixa.

---

## 9. Calibração Prévia (Treino)

Antes de iniciar a codificação dos 199 registros, R1 e R2 devem:

1. **Ler este protocolo na íntegra.**


2. **Ler a aba INSTRUCOES** da planilha `bd_codificacao_qualitativa.xlsx`.


3. **Codificar conjuntamente 10 registros-piloto** (sugestão: 3 de T2a, 2 de T2b, 3 de T3, 2 de T4), discutindo cada decisão até chegar a consenso.


4. **Verificar o alinhamento:** se durante o piloto houver discordância em mais de 3 dos 10 registros, revisar os critérios antes de prosseguir.

---

## 10. O que Acontece com os Dados Codificados

Após a codificação final (consensuada), o script `31_converter_quali_para_lnRR.py` executa as seguintes conversões:

**T2a (p → lnRR):**


$$p \xrightarrow{\Phi^{-1}} z \xrightarrow{\text{Borenstein}} d \xrightarrow{\text{Hasselblad}} lnOR \xrightarrow{\text{Zhang\&Yu}} lnRR$$

com inflação de variância $\sigma_{conv}^2 = 0.15^2$

**T2b (threshold → lnRR):**


Mesma cadeia, usando $p = 0.05$ (intensidade 2–3) ou $p = 0.10$ (intensidade 1) como threshold conservador.  


Inflação: $\sigma_{conv}^2 = 0.25^2$

**T3 (ordinal → lnRR):**


$$\text{(Direção} \times \text{Intensidade)} \rightarrow lnOR_{logit} \rightarrow lnRR$$

Mapeamento logit-normal: intensidade 1 → lnOR = →0.405, intensidade 2 → lnOR = +0.405, intensidade 3 → lnOR = +1.386  


Inflação: $\sigma_{conv}^2 = 0.35^2$

**T4 (qualitativo → lnRR):**


Mesma conversão ordinal, com inflação adicional: $\sigma_{conv}^2 = 0.50^2$ e fator multiplicativo de 1.5 sobre a variância.

A inflação de variância garante que registros convertidos recebem **peso menor** na meta-análise hierárquica, proporcional à incerteza da conversão. T1 (sem inflação) sempre domina a estimativa quando disponível.

---

## 11. Checklist Final do Revisor

Antes de entregar a planilha preenchida, verificar:

- [ ] Todos os 199 registros possuem valor em Direcao_efeito (−1, 0 ou +1)


- [ ] Todos os 199 registros possuem valor em Intensidade (1, 2 ou 3)


- [ ] Coluna Revisor preenchida em todos (R1 ou R2)


- [ ] Coluna Confianca preenchida em todos (Alta, Moderada ou Baixa)


- [ ] Registros T2a: verificar se a Direcao é coerente com os p-values listados


- [ ] Registros T2b: anotar p-value extraído manualmente nas Notas (quando possível)


- [ ] Registros T3: anotar o trecho/tabela que sustenta a codificação


- [ ] Registros T4: justificar a codificação nas Notas (especialmente se Intensidade = 3)


- [ ] n_T e n_C preenchidos sempre que extraíveis do texto


- [ ] Nenhum campo das colunas A→L foi alterado (dados automáticos)

---

## 12. Referências Metodológicas

- Borenstein, M. et al. (2009). *Introduction to Meta-Analysis*. Cap. 7: Converting among effect sizes.


- Hasselblad, V. & Hedges, L.V. (1995). Meta-analysis of screening and diagnostic tests. *Psychological Bulletin*, 117(1), 167−178.


- Zhang, J. & Yu, K.F. (1998). What's the relative risk? A method of correcting the odds ratio in cohort studies. *JAMA*, 280(19), 1690−1691.


- Lajeunesse, M.J. (2011). On the meta-analysis of response ratios for studies with correlated and multi-group designs. *Ecology*, 92(11), 2049–2055.


- Cohen, J. (1960). A coefficient of agreement for nominal scales. *Educational and Psychological Measurement*, 20(1), 37–46.



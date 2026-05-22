# BRIEFING TCC — Fonte única de contexto

> **Para qualquer agente (Claude Code, Codex, Claude.ai):** este arquivo é a **fonte única da verdade** sobre o projeto.
> `CLAUDE.md` e `AGENTS.md` são apenas pointers para cá.
> **Atualize SEMPRE este arquivo** ao final de cada etapa relevante (resultado novo, decisão tomada, arquivo criado/movido).

> **Última atualização:** 2026-05-21 — **DECISÃO METODOLÓGICA: F1-macro como métrica principal do artigo** (substitui F1 weighted) + tabela complementar V4 vs V5 (Acurácia/Precisão/F1-macro) + correções de coerência. Ver histórico.

---

## 1. Identificação

- **Título:** Análise de Sentimentos em Críticas de Cinema com Dados Sintéticos Gerados por LLMs
- **Aluno:** Davi Romauski Meurer — UTFPR Dois Vizinhos, Eng. Software, 8º semestre
- **Orientador:** Prof. Marlon Marcon
- **Repositório:** https://github.com/ROMAUSKI/tcc-analise-sentimento

---

## 2. Perguntas de Pesquisa

1. Qual a assertividade dos modelos treinados com dados sintéticos?
2. A classificação é coerente entre os diferentes LLMs geradores?
3. **(Adicionada após orientação)** Modelos treinados em dados sintéticos generalizam para dados reais? — *cross-domain evaluation*

---

## 3. Estrutura de Pastas

```
tcc-analise-sentimento/
├── BRIEFING_TCC.md              # ESTE ARQUIVO — fonte única de contexto
├── CLAUDE.md                    # Pointer para BRIEFING (3 linhas)
├── AGENTS.md                    # Pointer para BRIEFING (3 linhas)
├── README.md                    # Descrição pública do projeto
├── requirements.txt             # Dependências Python (inclui torch/transformers)
├── .gitignore                   # ignora dados pesados e checkpoints
├── artigo/                      # Artigo LaTeX (formato SBC) — versão ATIVA
│   ├── main.tex, main.pdf
│   ├── sbc-template.sty, sbc.bst, caption2.sty, referencias.bib
│   └── imagens/
├── dados/
│   ├── brutos/                  # 9 CSVs sintéticos (Movies — Claude/Gemini/ChatGPT)
│   ├── brutos_apps/             # (a criar — Etapa E) 9 CSVs sintéticos para Apps
│   └── processado/              # synthetic_dataset.csv, dataset_completo.csv
├── documentos/                  # Regulamentos, checklists, leituras
├── resultados/                  # Gráficos (.png) e métricas (.csv) ATIVOS
├── src/                         # Notebooks Jupyter ATIVOS
│   ├── 00_data_generation.ipynb           # documentação geração via LLMs
│   ├── 01_movies_training.ipynb           # NB/LR/SVM em sintético (célula 1 padronizada)
│   ├── 02_movies_robustness.ipynb         # CV k=10, learning curves, erros (célula 1 padronizada)
│   ├── 03_movies_3_visoes.ipynb           # V1/V2/V3/V4/V5 clássicos (Movies)
│   ├── 04_movies_avancado.ipynb           # LSTM + BERT/Bertimbau (auto-setup CUDA)
│   ├── 05_apps_training.ipynb             # esqueleto (Etapa E)
│   ├── 06_apps_robustness.ipynb           # esqueleto (Etapa E)
│   ├── checkpoints_avancado/              # gerado pelo notebook 04 (gitignored)
│   └── dados_reais/                       # cache kagglehub (gitignored, ~877 MB)
└── archive/                     # Versões antigas/fora-de-escopo (ver README local)
    ├── README.md
    ├── notebooks/  → 03_real_data_validation, 04_comparativo_3_visoes, 07_redes_neurais
    ├── scripts/    → _update_charts.py, analise_3_visoes.py, reprocessar_dataset.py
    ├── artigo/     → main_v1.tex, main_v1.pdf, artigo_compilado.pdf, artigo_TCC.pdf
    └── resultados/ → grafico_redes_neurais.png, metricas_redes_neurais.csv, analise_3_visoes_movies.csv
```

**Notebooks futuros (Etapa E + F):** `07_apps_3_visoes.ipynb`, `08_apps_avancado.ipynb`, `09_comparativo_nichos.ipynb`.

---

## 4. Comandos

```bash
# Instalar dependências
pip install -r requirements.txt

# Executar notebooks (ordem)
python -m nbconvert --to notebook --execute src/01_movies_training.ipynb --output 01_movies_training.ipynb
python -m nbconvert --to notebook --execute src/02_movies_robustness.ipynb --output 02_movies_robustness.ipynb
python -m nbconvert --to notebook --execute src/03_movies_3_visoes.ipynb --output 03_movies_3_visoes.ipynb
# (futuros)
python -m nbconvert --to notebook --execute src/04_movies_avancado.ipynb --output 04_movies_avancado.ipynb

# Compilar artigo LaTeX
cd artigo && latexmk -pdf main.tex
```

**Observação Windows:** usar `PYTHONIOENCODING=utf-8` antes do nbconvert se houver caracteres especiais (→, ã, ç).

---

## 5. Dataset

### Sintético (gerado via LLMs por interface web)

- **Movies — `dados/processado/synthetic_dataset.csv`:** 1798 frases, 600 por classe (200 por LLM × 3 classes), columns `frase_limpa, classe, fonte, frase`
- **Apps — `dados/brutos_apps/`:** A SER GERADO. Mesmo padrão: 200/classe/LLM = 1800 frases
- **3 classes:** Positiva, Negativa, Neutra
- **3 fontes:** ChatGPT, Claude, Gemini

### Real (Kaggle via kagglehub)

- **Dataset:** `fredericods/ptbr-sentiment-analysis-datasets` (~877 MB)
- **Arquivos:** `utlc_movies.csv` (~1.5M linhas), `utlc_apps.csv` (~1M linhas), b2w, buscape, olist
- **Colunas relevantes:** `review_text`, `rating` (1-5)
- **Mapping rating→classe** (essencial — dataset nativo só tem polaridade binária):
  - rating ≥ 4 → **Positiva**
  - rating ≤ 2 → **Negativa**
  - rating = 3 → **Neutra**
- **Cache:** `~/.cache/kagglehub/...` (download) + `src/dados_reais/` (local) + `/content/sample_data/dataset_real_sentimentos/` (Colab)

### Pré-processamento padrão

- Lowercase + remoção de pontuação (regex `[^a-zà-ÿ\s]`) + colapso de espaços
- Remoção de duplicatas
- TF-IDF (max_features padrão = 5000)

---

## 6. Modelos

### Clássicos (notebooks 01-03)

| Modelo | Classe sklearn | Hiperparâmetros |
|---|---|---|
| Naive Bayes | `MultinomialNB()` | padrão |
| Regressão Logística | `LogisticRegression()` | `max_iter=1000, random_state=42` |
| SVM Linear | `LinearSVC()` | `max_iter=5000, random_state=42` |

Todos encapsulados em `Pipeline([('tfidf', TfidfVectorizer()), ('clf', clf)])`.

### Avançados (notebook 04 — A IMPLEMENTAR)

| Modelo | Framework | Hiperparâmetros previstos |
|---|---|---|
| LSTM | PyTorch | `nn.Embedding(vocab, 128) → nn.LSTM(hidden=128, layers=1) → Dropout(0.3) → Linear`. Treino: 10-20 epochs, batch=32, AdamW lr=1e-3 |
| BERT (Bertimbau) | `transformers` | `neuralmind/bert-base-portuguese-cased` **fixado na revisão `4a78cfb` com `model.safetensors`**. Fine-tuning: 3 epochs, batch=8, AdamW lr=2e-5 |

Hardware-alvo: **RTX 3070 (8GB)** local ou **Colab T4** como fallback.

---

## 7. Metodologia das 5 Visões (peça central do TCC)

Forma uma **matriz 2×2** elegante de fonte × volume, com V1 como baseline:

|                          | **Volume controlado (200/classe)** | **Volume natural (todos ~100k)** |
|--------------------------|---|---|
| **Sintético → Sintético** | V1 | — (sintético é fixo em 200) |
| **Real → Real**           | V2 | **V4** |
| **Sintético → Real**      | V3 | **V5** |

| Visão | Treino | Teste | Volume aprox. | Função |
|---|---|---|---|---|
| **V1** | Sintético (200/classe) | Sintético (200/classe) | 480 / 120 | Baseline sintético — qualidade isolada dos dados sintéticos |
| **V2** | Real (200/classe) | Real (200/classe) | 480 / 120 | Baseline real com mesmo volume — comparação justa de fonte |
| **V3** | Sintético (200/classe) | Real (**mesmo test set do V2**) | 480 / 120 | **Cross-domain controlado** — generalização sintético→real isolando volume |
| **V4** | Real desbalanceado (todos) | Real desbalanceado | ~80k / ~20k | "Vida real" do real — limite superior com dado abundante |
| **V5** | Sintético (200/classe) | Real desbalanceado (**mesmo test set do V4**) | 480 / ~20k | **Cross-domain "vida real"** — sintético escasso testado em real abundante |

**Pareamentos para comparações diretas:**
- **V2 vs V3** (mesmo test set 120 reais): isola "fonte do treino" com volume controlado
- **V4 vs V5** (mesmo test set ~20k reais): isola "fonte do treino" com volume natural
- **V2 vs V4**: mostra ganho de volume no real
- **V3 vs V5**: mostra como o sintético escala quando o teste é a distribuição natural

**Por que F1 macro será crítico para V4/V5:** distribuição real ~75% Positiva / ~15% Negativa / ~10% Neutra. Modelo "burro" prevendo só Positiva tem Acurácia ~75% mas F1 macro ~29%. Sempre reportar **Acurácia + F1 weighted + F1 macro**.

---

## 8. Resultados Atuais

### Movies — 5 visões clássicas (notebook 03, seed=42, **600 frases/classe** = sintético inteiro 1800)

**F1 weighted / F1 macro (%)**

| Visão | Naive Bayes | Reg. Logística | SVM Linear |
|---|---|---|---|
| V1: Sintético → Sintético (controlado) | **88.07 / 88.07** | 86.93 / 86.93 | 88.33 / 88.33 |
| V2: Real → Real (controlado) | 52.10 / 52.10 | 54.45 / 54.45 | 54.80 / 54.80 |
| V3: Sintético → Real (controlado) | 34.75 / 34.75 | 38.77 / 38.77 | 36.45 / 36.45 |
| V4: Real → Real (desbalanceado) | 64.36 / **38.48** | 70.93 / **52.05** | 70.59 / **51.92** |
| V5: Sintético → Real (desbalanceado) | 47.11 / **32.29** | 45.30 / **32.61** | 45.47 / **32.50** |

*Distribuição real natural:* Positiva 70.77% / Neutra 19.98% / Negativa 9.25% (n=99.758).

**Volumes de treino:** V1/V2/V3 = 1440 amostras; V4 = 79.806 amostras; V5 = 1440 sintéticas testadas em ~20k reais.

**Observações-chave para a defesa:**
- **V1 alto e estável** (~88%) — sintético tem vocabulário regular por classe; modelos clássicos capturam bem
- **V2 sobe pra ~54%** (era 43% com 200/cl) — volume real adicional ajuda na variabilidade
- **V3 quase não mudou** (35-39%) mesmo triplicando treino sintético — **prova que o reality gap é ESTRUTURAL (diferença de distribuição), não estatístico (falta de dados)**
- **V4 desbalanceado:** Acurácia 72-75% mas **F1 macro 38-52%** — gap exemplifica viés de classe majoritária. NB sofre mais (38%) que LR/SVM (52%) porque NB confia em P(classe) a priori
- **V5 desbalanceado:** F1 macro ~32% (caiu vs antes); mais sintético no treino aumenta o "viés sintético" e afasta da distribuição real
- **Reality gap PERSISTENTE:** V1→V3 cai ~50 pontos em F1; V4→V5 cai ~22 pontos; gap não é compensado por volume

**Mudança metodológica 2026-05-10:** N_POR_CLASSE corrigido de 200 para 600 (sintético inteiro = 1800). Entendimento original era "200 por LLM por classe" (que totaliza 600/classe = 1800 total). A escolha errada anterior (200/cl = 600 total) descartava 1200 frases sintéticas sem motivo.

### Movies — Resultados consolidados Clássicos + LSTM + BERT (2026-05-11, notebook 04 no Colab T4)

**F1 weighted / F1 macro (%) — 5 modelos × 5 visões**

| Visão | NB | LR | SVM | LSTM | **BERT (Bertimbau)** |
|---|---|---|---|---|---|
| V1: Sint→Sint | 88.07 / 88.07 | 86.93 / 86.93 | 88.33 / 88.33 | 81.40 / 81.40 | **97.49 / 97.49** |
| V2: Real→Real | 52.10 / 52.10 | 54.45 / 54.45 | 54.80 / 54.80 | 39.23 / 39.23 | **60.42 / 60.42** |
| V3: Sint→Real | 34.75 / 34.75 | 38.77 / 38.77 | 36.45 / 36.45 | 34.83 / 34.83 | **47.10 / 47.10** |
| V4: Real desbal | 64.36 / 38.48 | 70.93 / 52.05 | 70.59 / 51.92 | 71.99 / 54.89 | **76.46 / 62.29** |
| V5: Sint→Real desbal | 47.11 / 32.29 | 45.30 / 32.61 | 45.47 / 32.50 | 42.13 / 27.13 | **58.95 / 42.62** |

**Tempo de treino BERT no Colab T4 (`MAX_SAMPLES_REAL=100_000`):** V1=2.2min, V2=2.4min, V3=1.5min, V4=35.8min, V5=5.9min. Total ~50min.

**Insight refinado para a defesa:**
- **LSTM foi inútil** — empata ou perde pros clássicos em todas as visões (era esperado: 1.440 frases é pouco para treinar embeddings do zero)
- **BERT venceu em TODAS as 5 visões** — mostra que classificadores contextuais com pretreino em pt-BR exploram melhor os dados sintéticos
- **BERT MITIGA parcialmente o reality gap:**
  - V3: clássicos ~36% → BERT 47% (**+11 pts**)
  - V5: clássicos ~46% → BERT 59% (**+13 pts**)
- **Tese refinada:** o reality gap entre dados sintéticos e reais é estrutural para classificadores baseados em TF-IDF (negação, gírias, contexto não capturados), mas modelos contextuais (BERT/Bertimbau) conseguem mitigar parte significativa dessa lacuna ao aproveitar pretreino linguístico em larga escala.

**Arquivos gerados (notebook 04):**
- `resultados/metricas_avancado_movies.csv` (LSTM + BERT × 5 visões)
- `resultados/metricas_consolidado_movies.csv` (clássicos + LSTM + BERT — tabela mestre)
- `resultados/grafico_consolidado_movies_f1weighted.png` (5 modelos × 5 visões em barras agrupadas)
- `resultados/grafico_consolidado_movies_f1macro.png` (idem com F1 macro — destaca viés desbalanceado em V4)

### Apps — 5 visões clássicas + LSTM + BERT (notebook 08, executado no Colab T4 em 2026-05-14)

**F1 weighted / F1 macro (%) — 5 modelos × 5 visões**

| Visão | NB | LR | SVM | LSTM | **BERT (Bertimbau)** |
|---|---|---|---|---|---|
| V1: Sint→Sint | 88.82 / 88.82 | 89.69 / 89.69 | 91.07 / 91.07 | 85.22 / 85.22 | **97.22 / 97.22** |
| V2: Real→Real | 62.50 / 62.50 | 61.18 / 61.18 | 58.16 / 58.16 | 56.01 / 56.01 | **66.84 / 66.84** |
| V3: Sint→Real | 40.42 / 40.42 | 40.24 / 40.24 | 42.17 / 42.17 | 31.66 / 31.66 | **48.21 / 48.21** |
| V4: Real desbal | 81.16 / 56.13 | 82.84 / 60.04 | 82.36 / 59.39 | 83.86 / **63.11** | **86.27 / 66.59** |
| V5: Sint→Real desbal | 67.04 / 38.97 | 64.16 / 36.91 | 64.42 / 37.05 | 59.55 / 36.23 | **80.95 / 55.68** ⭐ |

*Distribuição real natural Apps:* 72.15% Pos / 21.05% Neg / 6.80% Neu (n=99.909).

**Tempo BERT no Colab T4 (`MAX_SAMPLES_REAL=100_000`):** V1=56s, V2=205s, V3=176s, V4=1434s (~24min), V5=151s. Total ~35min.

**Comparativo Apps × Movies (insight central da Etapa F)**

| Visão | Apps BERT F1w | Movies BERT F1w | Diferença |
|---|---|---|---|
| V1 Sint→Sint | 97.22% | 97.49% | -0.3 |
| V2 Real→Real | 66.84% | 60.42% | +6.4 |
| V3 Sint→Real | 48.21% | 47.10% | +1.1 |
| V4 Real desbal | 86.27% | 76.46% | +9.8 |
| **V5 Sint→Real desbal** | **80.95%** | **58.95%** | **+22.0** ⭐ |

**Insight novo (Apps muito acima de Movies em V5 desbalanceado):**
Reviews reais de aplicativos seguem padrão muito mais regular e direto que reviews de filmes — a galera reclama de problemas técnicos objetivos ("trava", "consome bateria", "anúncios excessivos") em vez de fazer análise narrativa, comparações entre obras ou apreciação subjetiva. Esse vocabulário de avaliação de apps tem mais sobreposição com o que LLMs geram naturalmente, o que reduz o reality gap quando o teste é em distribuição natural (V5). A consequência prática é que **a viabilidade do treino com dados sintéticos depende do nicho** — pode funcionar razoavelmente bem em domínios com vocabulário regular (avaliação de produto/serviço), e falha em domínios com linguagem mais elaborada (crítica de mídia, opinião subjetiva extensa).

**Arquivos gerados (notebook 08):**
- `resultados/metricas_avancado_apps.csv` (LSTM + BERT × 5 visões)
- `resultados/metricas_avancado_apps_partial.csv` (incremental, salvo a cada visão)
- `resultados/metricas_consolidado_apps.csv` (clássicos + LSTM + BERT — tabela mestre Apps)
- `resultados/grafico_consolidado_apps_f1weighted.png` (5 modelos × 5 visões)
- `resultados/grafico_consolidado_apps_f1macro.png` (idem com F1 macro)

### Conclusão do TCC (versão para o artigo — Etapa G)

> Texto redigido no estilo do Davi (skill `escrita-davi-tcc`), pronto para ser inserido na seção de Conclusão do artigo. Atualizar se Apps trouxer divergência relevante.

Os resultados deste trabalho mostram que dados sintéticos gerados por LLMs não constituem uma alternativa viável para treinar classificadores de sentimento destinados a uso prático. Modelos treinados exclusivamente em frases sintéticas e avaliados em reviews reais atingem no máximo 47% de F1 weighted no nicho de filmes e 59% no nicho de aplicativos, valores muito abaixo do patamar mínimo aceitável para qualquer aplicação que exija confiabilidade. Esse desempenho aparece de forma consistente nas cinco visões metodológicas testadas e nos cinco modelos avaliados, o que indica que a limitação não decorre de uma escolha pontual de classificador ou hiperparâmetro, mas sim de uma diferença estrutural entre o texto gerado por LLMs e as avaliações escritas por usuários reais.

A análise comparativa entre volumes de 200 e 600 frases por classe reforça essa interpretação. Triplicar a quantidade de dados sintéticos no treino mantém o desempenho cross-domain praticamente inalterado, o que mostra que a limitação observada não vem da escassez de dados, e sim da regularidade do vocabulário, da polaridade explícita e da baixa incidência de construções complexas como negação composta e ironia nas frases sintéticas. Modelos contextuais pré-treinados como o Bertimbau atenuam parte do problema, recuperando entre dez e quinze pontos percentuais sobre os classificadores baseados em TF-IDF, mas mesmo essa melhoria não chega a níveis suficientes para uso em produção.

Um aspecto metodológico relevante é o que pode ser descrito como um paradoxo de avaliação. Para calibrar e melhorar a qualidade dos dados sintéticos seria necessário compará-los com dados reais rotulados, o que torna o sintético um complemento dependente do real e não uma alternativa autônoma. Construir prompts capazes de gerar frases representativas sem nenhuma referência a dados reais é uma tarefa difícil na prática, e durante este trabalho foi observado que LLMs sem instruções específicas tendem a produzir conteúdo combinatório repetitivo, com baixa diversidade linguística. Esse comportamento sugere que a viabilidade da abordagem está condicionada à existência prévia de algum conjunto real para guiar o processo de geração, o que reduz o ganho prático esperado.

A análise de custo também aponta para a mesma direção. Em cenários onde o objetivo é classificar um volume moderado de frases, pagar diretamente uma API de LLM para realizar a classificação em modo zero-shot tende a ser mais econômico e mais assertivo do que gerar dados sintéticos, treinar um modelo próprio e arcar com a infraestrutura necessária. A combinação de custo da API para geração, tempo de desenvolvimento, infraestrutura de treinamento e desempenho final inferior torna o caminho sintético desfavorável para a maior parte das aplicações comuns. A abordagem mantém algum valor em situações específicas, como cenários com restrições de privacidade que impeçam o envio de dados a APIs externas, necessidade de inferência offline ou em dispositivos embarcados, volumes muito altos de classificação onde o custo da API se torna proibitivo, exigências de compliance que demandem modelo proprietário, ou domínios com tão pouco dado disponível que a geração sintética se torne a única opção viável.

A principal contribuição deste trabalho está em demonstrar empiricamente esse conjunto de limitações e quantificá-las de forma sistemática, em dois nichos distintos e com cinco classificadores cobrindo desde modelos lineares baseados em TF-IDF até arquiteturas neurais com pretreino em larga escala. A evidência reunida permite afirmar que dados sintéticos gerados por LLMs ainda não são uma substituição prática para corpora reais em análise de sentimento em português brasileiro, mas oferecem um ponto de partida funcional para pesquisa exploratória, prototipagem inicial e cenários onde o uso de dados reais é inviável por restrições externas.

**Arquivos gerados:**
- `resultados/metricas_5_visoes_movies.csv`
- `resultados/grafico_5_visoes_movies.png` (F1 weighted, 5 colunas × 3 modelos)
- `resultados/grafico_5_visoes_movies_5metricas.png` (painel 2×3 com 5 métricas)
- `resultados/grafico_5_visoes_movies_{acuracia,precisao,recall,f1score,f1macro}.png` (individuais)
- **`resultados/comparativo_200_vs_600_movies.{csv,png}`** — evidência do reality gap estrutural: 5 painéis lado a lado mostrando que V3 quase não muda quando o volume sintético triplica (200/cl → 600/cl), enquanto V1 e V2 sobem 4-13 pontos. **Argumento central pro artigo.**

### Resultados antigos (notebook 01 — sintético puro, split 80/20)

| Modelo | Acurácia (%) | Precisão (%) | Recall (%) | F1 (%) |
|---|---|---|---|---|
| Naive Bayes | 86,11 | 86,19 | 86,11 | 86,13 |
| SVM Linear | 86,11 | 86,21 | 86,11 | 86,09 |
| Regressão Logística | 83,61 | 83,80 | 83,61 | 83,54 |

### Validação Cruzada (notebook 02)

| Modelo | k | Acurácia (%) | F1 (%) |
|---|---|---|---|
| Naive Bayes | 10 | 89,60 ±2,16 | **89,63 ±2,15** |
| SVM Linear | 10 | 89,10 ±2,49 | 89,10 ±2,51 |
| Reg. Logística | 10 | 88,04 ±2,42 | 88,02 ±2,44 |

### Análise de Erros (notebook 02)

- 50/360 erros (13,9%) no Naive Bayes
- Confusão dominante: Negativa ↔ Positiva (24 erros)
- Por fonte: ChatGPT 9,9% | Claude 14,1% | Gemini 17,4%
- Hipótese: ChatGPT mais direto; Gemini mais descritivo/ambíguo

### Pendentes (a executar)

- V4 no notebook 03 (desbalanceada)
- Notebook 04: LSTM e BERT × 4 visões
- Pipeline Apps inteiro (notebooks 05-08)
- Comparativo final (notebook 09)

---

## 9. Decisões Metodológicas

| # | Decisão | Justificativa |
|---|---|---|
| D1 | seed=42 em todos os notebooks | Reprodutibilidade |
| D2 | TF-IDF parâmetros padrão (sem stopword removal) | IDF já penaliza termos frequentes |
| D3 | F1-Score weighted como métrica principal | Considera desbalanceamento residual |
| D4 | 200 frases/classe nos sintéticos (e em V1/V2/V3 reais) | Controle de variável "volume" — comparação justa de fonte |
| D5 | V3 reusa test set do V2 | Isola variável "fonte do treino" |
| D6 | Dados reais via `kagglehub` (não versionados) | 877 MB, baixa sob demanda; portátil Colab/local |
| D7 | Bertimbau base (`neuralmind/bert-base-portuguese-cased`) | Padrão pt-BR; cabe na RTX 3070 com batch=8 |
| D8 | LSTM com embeddings aprendidos do zero (não pretreinados) | Comparação justa com BERT pretreinado; mostra ganho do pretreino |
| D9 | CLAUDE.md/AGENTS.md viram pointers | Centralização → menos divergência, menos tokens |
| D10 | Notebook 04 separado (não cells dentro do 03) | LSTM/BERT são paradigmas diferentes; tempos de execução muito distintos |

---

## 10. Regras de Trabalho

### 🎯 Regra ZERO (a mais importante — definida 2026-05-10)

**O foco é ACABAR a faculdade — apresentar o TCC e tirar entre 6 e 10. Pronto.**
Davi NÃO está interessado em:
- Wow factor pra banca
- Interfaces / demos / deploys
- Trabalhos futuros expandidos
- Projetos paralelos
- "Maravilhar" o orientador

**Toda sugestão fora do escopo mínimo do orientador deve ser DESCARTADA.** Quando Davi perguntar algo (curiosidade, dúvida), responder de forma curta e técnica, sem propor implementação adicional.

**Escopo mínimo explícito do orientador:**
1. Cinco visões metodológicas (V1..V5) ✅ feito
2. Modelos clássicos (NB/LR/SVM) ✅ feito
3. Modelos avançados (LSTM + BERT/Bertimbau) ⏳ rodando no Colab
4. Segundo nicho (UTLC-Apps) ⏳ Etapa E
5. Artigo atualizado refletindo o acima ⏳ Etapa G

### Regras operacionais

1. **Passo a passo incremental** — um passo por vez, verificável.
2. **Antes de alterar código, checar impacto no pipeline** (`⚠️ SYNC:` se afetar cadeia 01→02→03).
3. **Nunca inventar métricas** — pedir para executar o notebook.
4. **seed=42** em todo código com aleatoriedade (numpy, sklearn, torch).
5. **Artigo formato SBC** — não alterar template (`sbc-template.sty`).
6. **Skill `escrita-davi-tcc` obrigatória** antes de qualquer adição/edição em `artigo/main.tex`.
7. **Idioma:** pt-BR.
8. **Nada deletado** — fora-de-escopo vai para `archive/`.
9. **Atualizar este BRIEFING ao final de CADA etapa** (Histórico de Execução abaixo).

### 🧰 Catálogo de Skills para uso automático (mapeado 2026-05-17)

**Princípio:** antes de agir em determinado contexto do TCC, invocar a skill correspondente. Cada skill tem triggers em sua `description:` — o agente seleciona automaticamente quando o prompt do Davi bater. Este catálogo serve como **reforço/priorização** específica para o TCC.

#### 📝 Escrita / Revisão do artigo (`artigo/main.tex`)

| Quando | Skill | Observação |
|---|---|---|
| Editar/redigir/polir qualquer trecho do `main.tex` ou texto destinado ao artigo | **`escrita-davi-tcc`** | **OBRIGATÓRIA.** Polimento mínimo (orto/conjugação/preposição). Mantém tom natural do Davi. NUNCA estilizar. |
| Texto soou "de IA" / "me dá pra naturalizar" / "soa robótico" | **`marketing-content-humanizer`** | Humaniza saídas que ficaram formais demais. |
| Passada final de gramática depois de edição manual do Davi | **`marketing-copy-editing`** | Só ortografia/coerência, sem reescrever. |
| Estruturar nova seção do zero ou re-organizar fluxo | **`doc-coauthoring`** | Workflow de co-escrita estruturada. |

#### 🧠 Leitura / Contexto / Síntese cross-fontes

| Quando | Skill |
|---|---|
| Sintetizar info de várias fontes (BRIEFING + notebooks + artigo) numa resposta coerente, deduplicando | **`enterprise-search-knowledge-synthesis`** |
| Overview do projeto, mapeamento inicial, onboarding (sessão nova, agente novo) | **`engineering-codebase-onboarding`** |
| Navegar estrutura `src/` + `dados/` + `artigo/` + `archive/` | **`engineering-monorepo-navigator`** |

#### 💬 Debate / Defesa / Preparação pra banca

| Quando (frases-gatilho do Davi) | Skill |
|---|---|
| "me prepara pra banca", "simula banca", "que perguntas o orientador pode fazer", "argumento contra X", "stress-test essa parte", "pre-mortem" | **`c-level-advisor-executive-mentor`** (adversarial thinking — perfeito pra simular Prof. Marlon) |
| "qual a contribuição científica disso", "vale a pena pesquisar Y", "como justificar a escolha de Z" | **`bio-research-scientific-problem-selection`** |

#### 📚 Explicação / Ensino / Narrativa

| Quando | Skill |
|---|---|
| "explica isso pra mim", "como contar essa parte", verificar se introdução conversa com conclusão | **`c-level-advisor-internal-narrative`** |
| "me explica como se eu não soubesse", explicação didática de conceito técnico | **`marketing-content-creator`** |
| Apresentação cross-funcional, comunicado interno (slides defesa) | **`internal-comms`** |

#### 📊 Análise de resultados / ML / Estatística

| Quando | Skill |
|---|---|
| Interpretar métricas (F1 weighted vs macro), discutir overfitting, calibração, decisões de modelo | **`data-analytics-data-scientist`** |
| Testes estatísticos (Kruskal-Wallis, validação cruzada k-fold, IC, p-valor) | **`data-statistical-analysis`** |
| Questões de LSTM/BERT/transformer, fine-tuning Bertimbau, batch/lr/epochs | **`engineering-senior-ml-engineer`** |
| Visualizações (matplotlib/seaborn nos notebooks) | **`data-create-viz`** ou **`data-data-visualization`** |

#### 🔗 Coerência entre seções do artigo

| Quando | Skill |
|---|---|
| Verificar se Introdução / Resultados / Conclusão estão alinhados antes de envio ao orientador | **`c-level-advisor-strategic-alignment`** |
| Conferir consistência de números entre tabelas/texto/abstract | **`enterprise-search-knowledge-synthesis`** |

#### 💻 Revisão de código (notebooks)

| Quando | Skill |
|---|---|
| Revisão de notebook ou célula Python específica | **`engineering-code-reviewer`** |
| Simplificação após implementação | **`simplify`** |
| Reprodutibilidade / seeds / divergência cross-run | **`engineering-tdd-guide`** |

#### 🔧 Manutenção do repo

| Quando | Skill |
|---|---|
| Antes de commitar — formatar mensagem | **`git-commit-helper`** |
| "Resposta curta", "sem enrolação", "modo econômico" | **`token-lean`** |
| Atualizar `README.md` do projeto | **`readme-updater`** |
| Auditar se há credenciais expostas antes de push | **`secret-scanner`** |

---

**Localização garantida:** este catálogo vive aqui (Seção 10, `BRIEFING_TCC.md`). `CLAUDE.md` → `BRIEFING_TCC.md` é a chain obrigatória no início de qualquer sessão, então a leitura é garantida.

**Skills NÃO listadas acima** ainda podem ser invocadas pelo agente se o trigger bater fortemente. Este catálogo é a **lista priorizada para o contexto-TCC**, não exaustiva.

---

## 11. Histórico de Execução (rolling, mais recente no topo)

### 2026-05-21 — Migração para F1-macro + tabela complementar + correções de coerência

Decisão metodológica central (confirmada após revisão massiva): **o artigo passa a reportar F1-macro como métrica principal** (mais honesto em cenários desbalanceados). Plano: `~/.claude/plans/adicione-as-observa-es-que-witty-catmull.md`.

**Mudanças no `artigo/main.tex`:**
- Tabelas 3 (V1), 4 (V2/V4), 6 (V3/V5): agora em **F1-macro**, formato limpo (sem "weighted / macro"). V1/V2/V3 não mudaram de valor (balanceado: macro = weighted); V4/V5 passaram a mostrar macro.
- **Nova Tabela 7 (complementar)**: V4 vs V5 nos dois nichos, com Acurácia + Precisão + F1-macro (sem Recall, que = acurácia). Fim da Seção 5.3. Tabela 8 = validação cruzada (renumerada).
- Cross-domain no abstract/conclusão passou a usar **V5 (realista) para ambos os nichos: 43% filmes e séries / 56% apps** (antes "47%/80%" misturava visões). 97% (V1) mantém.
- Figura comparativa weighted **removida**; mantida só a macro. Gráfico 200vs600 **regenerado em F1-macro** (`src/_gerar_200vs600_macro.py`).
- Fundamentação: nota de que recall ponderado = acurácia + adoção do macro como principal.
- Narrativa de nichos ajustada: vantagem de Apps **restrita ao desbalanceado** (V1/V3 quase empatam).

**⚠️ Correção de dados importante (achada na revisão massiva):** os clássicos (NB/LR/SVM) de **V4 e V5 no nicho Apps** estavam **desatualizados** no artigo (ex: V4 Apps NB tabela 81,16/56,13 vs CSV real 80,97/54,83). A tabela tinha números de uma execução antiga. **Corrigido para os valores do `metricas_consolidado_geral.csv`** (fonte consistente). Movies, V1/V2/V3 e neurais já estavam corretos.

**Correções de coerência (existiam antes):**
- Metodologia 4.4: "controlado em 200 frases por classe" → **600** (alinha com Tabela 2 e dataset real 600/classe).
- Validação cruzada: "1.798 frases" → **1.800** (dataset tem exatamente 600/classe = 1.800, confirmado).
- Tabela 1: "Filmes (Movies)" → **Filmes**.

**Verificação:** PDF compila limpo (15 páginas, zero refs/citações indefinidas). `grep weighted` só retorna as explicações intencionais (Fundamentação + justificativa em 5.2).

### 2026-05-17 — Polimento final do artigo pré-envio ao orientador

Plano: `~/.claude/plans/adicione-as-observa-es-que-witty-catmull.md` (9 tarefas A-I).

**Resultado:** PDF de 14 páginas, layout limpo, narrativa coerente.

- ✅ **A** Concordância: `pode ser considerado` → `pode ser considerada` (Fundamentação Teórica)
- ✅ **B** Padronização **"filmes e séries"** em todo o texto (~17 substituições contextuais; UTLC-Movies preservado como nome do dataset; abstract EN com "movies and series")
- ✅ **C** Layout figuras: preâmbulo com `\setlength{\textfloatsep}{6pt}`, figuras comparativas em `0.90\textwidth`, `\vspace` negativo após cada
- ✅ **D** Legendas das Tabelas 4 e 6 com ordem explícita "F1 weighted / F1 macro"
- ✅ **E** Quadro de frases-exemplo 3x2 (Tabela 5) na Seção 5.3: sintética (Claude) vs real (UTLC-Movies). Inclui "PQP q filme", "Horrivel" (sem acento), "interesante"/"mais" — preservados pra mostrar o reality gap
- ✅ **F** Parágrafo de custo refinado na Conclusão: declarar custo monetário zero do trabalho (interfaces web free/pro) + estimativa pública via API (~$1 por cenário, maio 2026) + ressalva de escala
- ✅ **G** Matriz de confusão SVM Linear V3-Filmes (Fig 2) — gerada via novo script `src/_gerar_matriz_v3_svm.py`. Insight: classe Neutra é a mais sacrificada (apenas 108/600 corretas; 305 confundidas com Negativa, 187 com Positiva)
- ✅ **H** Validação visual: pág 8 e pág 9 (eram as problemáticas) ficaram limpas; reorganização da Seção 5.3 com ordem narrativa Tab5 → Fig2 (matriz) → Tab6 (números)
- ✅ **I** Commits + push (commit final `dceee71`)

**Arquivos novos:**
- `src/_gerar_matriz_v3_svm.py` — script reproduzível pra regerar a matriz
- `resultados/matriz_confusao_v3_svm_filmes.{png,csv}`
- `artigo/imagens/matriz_confusao_v3_svm_filmes.png`

**Status:** pronto pra envio ao orientador (Prof. Marlon Marcon). Davi vai fazer último review manual e enviar.

### 2026-05-17 — Catálogo de skills priorizadas para o TCC

- ✅ Adicionada subseção **"🧰 Catálogo de Skills para uso automático"** dentro da Seção 10 (Regras de Trabalho) do `BRIEFING_TCC.md`.
- ✅ Mapeadas ~25 skills priorizadas por contexto do TCC: escrita do artigo, leitura/contexto, debate/banca, explicação/ensino, análise ML, coerência cross-seções, revisão de código, manutenção repo.
- ✅ `CLAUDE.md` e `AGENTS.md` ganharam linha-pointer adicional reforçando localização do catálogo.
- ✅ Contexto: Davi instalou em massa as 197 skills do repo `anthropics/knowledge-work-plugins` em `C:\Users\Davi\.claude\skills\` (~444 skills totais). Catálogo organiza as relevantes pro TCC pra evitar dispersão do agente.

### 2026-05-09 — Bootstrap local Python 3.12 + CUDA no notebook 04

- ✅ `src/04_movies_avancado.ipynb` recebeu nova lógica na **Célula 1** para modo “GPU first”.
- ✅ Se o notebook estiver em **Windows + Python fora da janela suportada pelo PyTorch CUDA** (caso atual: `Python 3.14.3`), a célula tenta **bootstrap automático com `uv`**: instala Python 3.12, cria `.venv-cu121-py312`, instala dependências base, tenta `torch` com CUDA (`cu121` e fallback `cu118`) e registra kernel Jupyter **`Python 3.12 (TCC CUDA)`**.
- ✅ Limitação estrutural documentada: o notebook consegue **preparar** o kernel CUDA sozinho, mas ainda precisa que o usuário **troque o kernel** após o bootstrap, porque o Jupyter não troca o interpretador do kernel atual em runtime.
- ✅ Validação local: a célula compila, detecta corretamente o bloqueio do `Python 3.14.3`, identifica GPU via `nvidia-smi` e interrompe com instrução explícita para usar `Python 3.12`/kernel CUDA.
- ✅ Ajuste adicional para **prova de fogo**: `_torch_info_for_python()` agora diferencia corretamente **torch ausente** de **torch presente sem CUDA**, e `ALLOW_CPU_FALLBACK=False` faz a célula falhar explicitamente se a GPU não ativar.
- ✅ Ajuste final de coerência: após `import torch`, se `torch.cuda.is_available()` continuar `False`, a célula encerra com `SystemExit("PROVA DE FOGO FALHOU ...")` em vez de apenas avisar e seguir.
- ✅ Refinamento de reexecução: se `.venv-cu121-py312` já existir com CUDA ativa, a célula agora **reaproveita o ambiente** e só registra/atualiza o kernel Jupyter, evitando reinstalar tudo a cada nova execução a partir do `Python 3.14`.
- ✅ Diagnóstico reforçado: a célula 1 agora imprime o **comando executado** e o **stdout/stderr completos** quando `uv`, `pip` ou `ipykernel` falham no bootstrap CUDA.
- ✅ Correção de bootstrap: se `.venv-cu121-py312` já existir **sem** CUDA funcional ou em estado parcial, a célula agora recria o ambiente com `uv venv --clear` em vez de abortar com erro de ambiente já existente.
- ✅ Correção de bootstrap 2: o ambiente criado por `uv venv` pode vir **sem `pip`**; por isso a célula passou a instalar dependências base e `torch` usando **`uv pip install --python <env_python>`**, sem depender de `python -m pip`.
- ✅ Correção de compatibilidade BERT: `AutoModelForSequenceClassification.from_pretrained(...)` passou a usar **`use_safetensors=True`** e a revisão fixa `4a78cfbf83c9c97533dd6d6694ca4323029ff061` do `neuralmind/bert-base-portuguese-cased`, evitando o bloqueio recente do `torch.load` em checkpoints `.bin`.

### 2026-05-09 — Fix da célula 1 do notebook 04

- ✅ `src/04_movies_avancado.ipynb` ajustado na **Célula 1** para evitar `CalledProcessError` cru ao tentar trocar `torch` CPU por CUDA via `pip` no Windows.
- ✅ `AUTO_INSTALL_PYTORCH_CUDA` passou a ser **False por padrão no ambiente local**. A célula agora diagnostica o ambiente, mostra o comando recomendado para CUDA, detecta `nvidia-smi` e segue com fallback controlado em CPU quando `torch` já está instalado.
- ✅ Compatibilidade confirmada com **Python 3.14.3 local**: correção de `importlib.util`, JSON do notebook válido e célula 1 executada com sucesso em teste real neste ambiente (`torch 2.11.0+cpu`, sem CUDA ativa no Python).

### 2026-05-09 — Reorganização e novas demandas

- ✅ **Etapa A:** BRIEFING_TCC.md reescrito centralizando tudo (CLAUDE.md, AGENTS.md, MODO DEFESA). Pointers reduzidos.
- ✅ **Etapa B:** notebook 03 expandido para **5 visões** (V1/V2/V3 controlados + **V4 Real desbalanceado + V5 Sint→Real desbalanceado**). Função `run_vision()` agora reporta F1 weighted **e** F1 macro. Distribuição real confirmada: 70.77% Pos / 19.98% Neu / 9.25% Neg. NB no V4 mostra Acc 73% × F1 macro 38% (gap de viés de classe majoritária). Detalhes na Seção 8 deste briefing.
- ✅ **Etapa C:** `04_movies_avancado.ipynb` criado (18 células) — LSTM (PyTorch, embeddings do zero) + BERT (Bertimbau base, fine-tuning) replicando V1..V5. **Célula 1 = auto-setup** (Colab instala silenciosamente; local auto-instala PyTorch+CUDA via subprocess sem precisar reiniciar kernel). Constantes configuráveis na **Célula 4** (`MAX_SAMPLES_REAL`, `BERT_EPOCHS`, etc.). Checkpoints intermediários (não perde se travar). `requirements.txt` atualizado com `torch>=2.0`, `transformers>=4.40`, `accelerate`, `tqdm`. **Sintaxe validada**, mas NÃO executado — Davi vai rodar overnight com `MAX_SAMPLES_REAL=None` (~7-10h). **Conhecido:** auto-instalação do PyTorch+CUDA falha em Python 3.14 (sem wheels disponíveis); resolução pendente — opções: instalar Python 3.11/3.12 ou usar Colab. Saída: `metricas_avancado_movies.csv`, `metricas_consolidado_movies.csv`, `grafico_consolidado_movies_f1weighted.png`, `grafico_consolidado_movies_f1macro.png`.
- ✅ **Etapa D:** Limpeza ampla (auditoria + reorganização):
  - Movidos para `archive/notebooks/`: `03_real_data_validation.ipynb`, `04_comparativo_3_visoes.ipynb`
  - Movidos para `archive/scripts/`: `_update_charts.py`
  - Movidos para `archive/artigo/`: `artigo_compilado.pdf`, `artigo_TCC.pdf` (raiz)
  - Criada `archive/resultados/` com: `grafico_redes_neurais.png`, `metricas_redes_neurais.csv`, `analise_3_visoes_movies.csv`
  - **Deletados (1.4 GB liberados):** `src/utlc_movies.zip` (292 MB), `src/dados_reais_temp/utlc_movies.csv` (1.1 GB), `_backup/` (vazia) — todos reproduzíveis via `kagglehub.dataset_download()`
  - `.gitignore` atualizado: adicionado `src/dados_reais_temp/`, `src/checkpoints_avancado/`, `src/*.zip`, `src/*.csv`
  - **Notebooks 01 e 02:** célula de setup padronizada com template light (sem kagglehub, já que só usam sintético) — agora idêntica ao padrão dos notebooks 03 e 04
  - `archive/README.md` reescrito documentando todos os arquivos arquivados
- ✅ **Hotfix 1 (2026-05-09):** notebooks 01 e 02 quebravam no Colab por paths relativos hardcoded — corrigido com paths absolutos via `DADOS_*`, `RESULTADOS`. Alias `dir_resultados=RESULTADOS` adicionado.
- ✅ **2026-05-15 — Etapa G CONCLUÍDA (artigo reescrito).** `artigo/main.tex` reescrito do zero seguindo as diretrizes da Seção 13.13 e a skill `escrita-davi-tcc` (versão polimento mínimo). Mudanças:
  - Estrutura nova: 3 blocos de resultados (V1 sintético, V2/V4 real, V3/V5 cross-domínio) + comparativo nichos + validação cruzada
  - Conclusão expandida com os 4 argumentos do Davi (inviabilidade, paradoxo de avaliação, prompt sem real, custo) + nuance dos dois nichos
  - Fundamentação Teórica reduzida (cortes técnicos autorizados pelo orientador)
  - 7 figuras novas no corpo (5 comparativos por métrica + 200vs600 + comprimento por LLM)
  - 13 imagens novas copiadas de `resultados/` para `artigo/imagens/`
  - Compilação OK (`latexmk -pdf`): 13 páginas, sem erros, único warning é `babel brazil` deprecated (cosmético)
  - Adicionados 3 gráficos comparativos faltantes em `resultados/` (acurácia, precisão, recall) seguindo padrão dos existentes
- ✅ **2026-05-14 — Etapa F CONCLUÍDA (consolidação visual + análise de comprimento).** Script único gerou 5 artefatos extras em `resultados/`:
  - `metricas_consolidado_geral.csv` — 50 linhas (Movies + Apps × 5 modelos × 5 visões)
  - `comparativo_nichos_f1weighted.png` e `_f1macro.png` — 5 painéis cada, Movies (azul) × Apps (laranja) por visão e modelo
  - `comprimento_frases_por_llm.csv` e `.png` — tabela e boxplot do comprimento das frases sintéticas por LLM e nicho
  - **Achado novo (comprimento por LLM):** ChatGPT é consistente em ambos os nichos (~49-50 chars). Claude se adapta ao domínio: 94 chars em Movies (narrativo) e 65 em Apps (técnico). Gemini intermediário (~58-66). Esse comportamento do Claude pode explicar parte da diferença em V5 — frases mais curtas e diretas (como em Apps) se aproximam mais das reviews reais.
- ✅ **2026-05-14 — Notebook 08 EXECUTADO no Colab T4 com sucesso (35min total).** LSTM + BERT × 5 visões para Apps integrados em `resultados/`. Detalhes na Seção 8 deste briefing. **Insight novo:** Apps mostra padrão semelhante ao Movies em V1/V2/V3, mas V5 (Sint→Real desbalanceado) salta para 80.95% F1w com BERT (vs Movies 58.95%, +22 pts). Isso indica que a viabilidade do treino com dados sintéticos depende do nicho — funciona melhor em domínios com vocabulário regular (avaliação de produto) e pior em domínios com linguagem narrativa elaborada (crítica de mídia).
- ✅ **2026-05-11 — Etapa E COMPLETA até E.3:**
  - **E.1 ✅** Prompts isomorfos para Apps redigidos (`dados/brutos_apps/metadata.csv`)
  - **E.2 ✅** 1800 frases sintéticas geradas (Davi via interfaces web): 9 arquivos × 200 frases (200 por LLM por classe). ChatGPT 5.5 + Gemini 3.1 pro + Claude Sonnet 4.6 adaptativo × Pos/Neg/Neu.
  - **E.3 ✅** Notebooks 05/06/07/08 clonados de 01/02/03/04 com 28+15+20+27 substituições automáticas (paths, datasets, variáveis, nomes de saída com sufixo `_apps`). Todos validam sintaxe. Aguardando Davi executar (05/06/07 local, 08 no Colab T4).
- ✅ **2026-05-11 — Notebook 04 EXECUTADO no Colab T4 com sucesso.** Resultados LSTM + BERT × 5 visões integrados em `resultados/`. Detalhes na Seção 8 deste briefing. Insight central: BERT mitiga parcialmente o reality gap (~+11pts em V3, +13pts em V5 vs clássicos); LSTM foi inútil (empata ou perde pros clássicos com 1.440 frases).
- ✅ **Hotfix 4 (2026-05-10):** Colab estourou RAM no V4 BERT com `MAX_SAMPLES_REAL=None` (1.5M frases). Decisão pragmática (Regra ZERO): reduzir para `MAX_SAMPLES_REAL=100_000`. Mantém distribuição natural (~71% Pos / 20% Neu / 9% Neg) e dá amostragem estatisticamente válida. Tempo total do notebook 04 cai de 7-10h para ~1.5-2h (cabe no free tier). Argumento na banca: "subamostra estratificada por viabilidade computacional, distribuição preservada".
- ✅ **Hotfix 3 (2026-05-10):** `Trainer(tokenizer=...)` deprecated em transformers 4.46+. Removido (DataCollatorWithPadding já carrega o tokenizer).
- ✅ **Hotfix 2 (2026-05-10):** após o hotfix 1, descoberto que a padronização do setup feita na Etapa D **destruiu imports críticos** que existiam nos setups originais (`re`, `matplotlib.pyplot`, `seaborn`, vários módulos `sklearn`, `warnings`) — e no notebook 02 também o **carregamento do dataframe** `df`, `X`, `y`. Erros descobertos sequencialmente:
  - `NameError: name 're' is not defined` (notebook 01 cell 4)
  - Provavelmente próximos seriam `NameError: name 'plt' is not defined`, `name 'sns'`, `name 'TfidfVectorizer'`, etc.
  - Setup dos dois notebooks reescrito mantendo a estrutura padronizada (`BASE_DIR`, `DADOS_*`, `RESULTADOS`, `SEED`) **e** restaurando todos os imports do código original (incluindo `from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, precision_recall_fscore_support`, `from sklearn.pipeline import Pipeline`, etc.)
  - Notebook 02: setup agora também carrega `df`, `X`, `y` (como o original fazia).
  - Sintaxe validada e auditoria de imports confirma todos os módulos críticos presentes nos dois notebooks.
  - **Lição aprendida:** ao padronizar setup de notebooks legados, sempre auditar TODOS os imports usados nas células abaixo antes de substituir — não confiar na "limpeza visual" do template novo.
- ⏳ **Etapa E (próxima):** geração manual de 1800 frases sintéticas para Apps + criação dos notebooks 05-08 (depende de Davi gerar via LLMs)
- ✅ Plano completo salvo em `~/.claude/plans/adicione-as-observa-es-que-witty-catmull.md`

### 2026-05-09 (anterior) — 3 visões implementadas

- ✅ Arquivamento: `archive/{notebooks,scripts,artigo}` criados; `07_redes_neurais_comparativo.ipynb`, `analise_3_visoes.py`, `reprocessar_dataset.py`, `main_v1.{tex,pdf}` movidos
- ✅ Renomeados: `01_training_evaluation` → `01_movies_training`; `02_robustness_analysis` → `02_movies_robustness`
- ✅ kagglehub 1.0.1 instalado, token KGAT testado, dataset baixado
- ✅ Notebook `03_movies_3_visoes.ipynb` criado e executado com 200/classe (V1=Sint, V2=Real, V3=Cross)
- ✅ Gráficos gerados: F1 (3 colunas) + 4 métricas individuais

### 2026-04-16 — Estado anterior

- ✅ Dataset sintético gerado (9 CSVs)
- ✅ Notebooks 01 e 02 completos (sintético puro)
- ✅ Artigo LaTeX primeira versão completa (Seções 1-6)

### Pendências antigas

- [ ] Revisão final do artigo
- [ ] Slides
- [ ] Apresentação cronometrada
- [ ] Entrega final + defesa

---

## 12. Observações Técnicas

- Notebooks rodam em **Colab** (clona repo + baixa dataset real) ou **VS Code/Antigravity local**
- Detecção de ambiente: `IN_COLAB = 'google.colab' in sys.modules`
- Caminhos do dataset real:
  - Local: `BASE_DIR/src/dados_reais/`
  - Colab: `/content/sample_data/dataset_real_sentimentos/`
  - Cache kagglehub: `~/.cache/kagglehub/...`
- Git: `safe.directory` configurado para o path local Windows
- Encoding: notebooks devem ser lidos/escritos em UTF-8 (cuidado com cp1252 default no PowerShell)

---

## 13. 🎓 MODO DEFESA — Guia de estudo do TCC para o Davi

> **REGRA PARA O AGENTE:** sempre que o Davi perguntar algo técnico sobre o TCC, pedir ajuda para slides, ou ensaiar respostas de banca, use esta seção como base. Explique de forma simples, direta, como se estivesse ensinando o Davi a explicar com palavras próprias. Inclua sempre: (1) o que é, em uma frase simples, (2) como o Davi deve explicar na apresentação, (3) possíveis perguntas da banca e respostas sugeridas.

### 13.1. Tipos de modelo que o TCC usa

**Atualização 2026-05-09:** o TCC agora cobre **DOIS paradigmas**:
- **Clássicos (ML tradicional):** Naive Bayes, Regressão Logística, SVM Linear — com TF-IDF
- **Avançados (Deep Learning):** LSTM, BERT (Bertimbau)

**Hierarquia para ter na cabeça:**
- ML Clássico → features manuais (TF-IDF) + classificador linear/probabilístico
- LSTM → rede neural recorrente, aprende sequência
- BERT → transformer pré-treinado, captura contexto bidirecional
- LLMs (GPT, Claude, Gemini) → transformers gigantes — geraram seus dados

**Como explicar a escolha de DOIS paradigmas:** "Comparar clássicos e avançados mostra que (a) o problema é difícil mesmo com modelo poderoso, ou (b) modelos avançados resolvem limitações dos clássicos como negação composta. A pergunta real do TCC é sobre os **dados sintéticos**, não sobre o classificador."

**Perguntas da banca:**
- *"Por que comparar clássicos e avançados?"* → "Para mostrar que o desempenho não é função só do classificador. Se BERT também sofre o reality gap (V3), a limitação está nos dados sintéticos, não no modelo."
- *"NB venceu LR/SVM nos sintéticos. Você esperava isso?"* → "Não exatamente. NB é generativo e geralmente perde para discriminativos com dados reais. Mas dados sintéticos têm vocabulário regular por classe — exatamente o que NB captura bem."
- *"Você sabe a diferença entre generativo e discriminativo?"* → "Sim. NB modela P(palavras|classe) e usa Bayes para inverter. LR e SVM aprendem direto P(classe|palavras). LR/SVM ganham com mais dados; NB ganha com dados regulares como os sintéticos."

### 13.2. TF-IDF — representação para os clássicos

**O que é:** transforma cada frase em vetor numérico. Cada posição é uma palavra do vocabulário; o valor é o peso TF-IDF — sobe se palavra é frequente na frase (TF), desce se aparece em muitos docs (IDF).

**Como explicar:** "TF-IDF pega a frase e vira números. 'Excelente' tem peso alto (rara e discriminativa); 'de' tem peso baixo (aparece em tudo)."

**Fórmula:** `TF-IDF(t,d) = TF(t,d) × log(N / DF(t))`

**Perguntas da banca:**
- *"Por que TF-IDF e não Bag-of-Words?"* → "BoW deixa palavras comuns dominarem. TF-IDF penaliza isso via IDF."
- *"Por que não embeddings (Word2Vec)?"* → "TF-IDF é o baseline padrão para clássicos. Embeddings exigem modelos mais complexos para aproveitar — usei isso justamente no BERT."
- *"Removeu stopwords?"* → "Não. IDF já penaliza naturalmente."

### 13.3. Os modelos clássicos

**Naive Bayes (Multinomial):** probabilístico, suposição "naive" de independência entre palavras. Funciona bem em texto.

**Regressão Logística:** discriminativa, atribui peso a cada palavra, soma ponderada decide classe.

**SVM Linear:** busca hiperplano que maximiza margem entre classes. Bom para alta dimensão (texto).

### 13.4. Os modelos avançados (NOVOS)

**LSTM (Long Short-Term Memory):** rede neural recorrente, processa palavras em sequência mantendo "memória". Captura ordem e contexto local. Embeddings aprendidos do zero no nosso caso.

**Como explicar:** "LSTM lê a frase palavra por palavra como uma pessoa. Lembra do que veio antes pra interpretar o que vem depois. Resolve em parte o problema de 'não' inverter sentido."

**BERT (Bertimbau):** transformer pré-treinado em massa de texto pt-BR. Capta contexto bidirecional (toda a frase de uma vez). Fazemos *fine-tuning*: ajustamos as últimas camadas pra nossa tarefa.

**Como explicar:** "BERT já 'aprendeu' português lendo milhões de textos. A gente só ensina a tarefa específica de classificar sentimento usando os 600 exemplos. É como contratar alguém que já sabe português, em vez de ensinar do zero."

**Perguntas da banca:**
- *"Por que LSTM se você já tem BERT?"* → "Para mostrar duas estratégias de DL: uma que aprende do zero (LSTM) e uma que aproveita pré-treino (BERT). Se BERT supera LSTM, isso evidencia o valor do pretreino."
- *"BERT melhorou o reality gap (V3)?"* → "[A responder após executar] Se sim, mostra que entendimento contextual ajuda generalização. Se não, confirma que o gap é dos dados, não do modelo."

### 13.5. Dados Sintéticos — o core do trabalho

**O que é:** todo dataset de treino sintético (1798 frases Movies + 1800 Apps a gerar) veio de 3 LLMs via interface web com prompts manuais.

**Como explicar:** "Se LLMs geram texto realista, será que servem para gerar dados de treino? Isso importa muito para pt-BR, onde dados rotulados são escassos."

**Perguntas da banca:**
- *"Por que não dados reais no treino?"* → "O objetivo é testar se sintético é viável como alternativa. Treinar em real não responderia a pergunta. Por isso a V3 (testar em real) é o ponto crucial."
- *"Como garantiu qualidade?"* → "Prompts padronizados, 3 fontes (ChatGPT/Claude/Gemini) para reduzir viés, deduplicação, e análise por fonte no notebook 02."
- *"LLMs podem ter 'decorado' reviews reais."* → "Possível. Mas como o objetivo é gerar dados utilizáveis (não originalidade), isso favorece a qualidade. Se o LLM reproduz padrões linguísticos realistas, melhor."
- *"Por que ChatGPT, Gemini, Claude?"* → "Três maiores LLMs comerciais via interface gratuita, empresas distintas (OpenAI/Google/Anthropic), arquiteturas e dados de treinamento distintos."
- *"Os prompts foram iguais?"* → "Sim. Mas cada LLM interpreta diferente — ChatGPT mais direto (~50 chars), Gemini mais descritivo (~61), Claude mais elaborado (~95)."

### 13.6. Cross-domain evaluation (V3) — termo técnico para a banca

**O que é:** treinar em um domínio (sintético) e testar em outro (real). Conhecido na literatura como *cross-domain evaluation*, *out-of-distribution generalization* ou *synthetic-to-real transfer*.

**Como explicar:** "Quero saber se o modelo treinado em frases artificiais funciona em reviews reais. É a única validação que prova utilidade prática dos dados sintéticos."

**Perguntas da banca:**
- *"Como chama esse tipo de avaliação?"* → "Cross-domain evaluation, ou synthetic-to-real transfer. Domain adaptation quando você adapta o modelo; aqui é apenas evaluation porque não retreino."
- *"Qual literatura discute isso?"* → "Blitzer, Pereira et al. (2007) é clássico em cross-domain sentiment. Glorot, Bordes, Bengio (2011) trazem deep learning. Os dois controlam volume entre domínios — por isso eu também controlo."
- *"V3 ficou em 38%. Por que tão baixo?"* → "Dois componentes: (a) sintético tem vocabulário mais regular que real, (b) 200 frases não capturam variabilidade do real. V2 com mesmo volume também ficou em 43%, próximo do V3 — mostra que a queda não é só por sintético ser ruim."

### 13.7. Métricas

**Acurácia:** acertos / total. Boa quando classes equilibradas.
**Precisão:** dos que o modelo disse positivo, quantos são? (mede falsos positivos)
**Recall:** dos verdadeiros positivos, quantos o modelo pegou? (mede falsos negativos)
**F1-Score:** média harmônica de precisão e recall. **Métrica principal.**

**Como explicar diferença:** "Spam detector com precisão alta = quase tudo marcado como spam realmente é. Recall alto = pega quase todo spam, mas pode marcar emails bons."

**Perguntas:**
- *"Por que F1 weighted?"* → "Pondera pelo número de amostras por classe. Mais realista que macro quando há desbalanceio (caso do V4)."
- *"Por que CV em vez de só split?"* → "Split simples depende de uma divisão. CV k=10 testa cada amostra uma vez, dá média e desvio padrão."
- *"k=5 ou k=10?"* → "k=10 (Kohavi 1995) é o trade-off padrão para datasets moderados."

### 13.8. Validação Cruzada Estratificada

**O que é:** divide dataset em k partes; treina em k-1, testa em 1; repete k vezes. Estratificada = mantém proporção de classes em cada fold.

### 13.9. Análise de Erros

- 50/360 erros (13,9%) no NB com sintético puro
- Padrão 1: inversão de polaridade (24 erros) — negação não capturada por TF-IDF (ex: "efeitos especiais muito ruins")
- Padrão 2: Neutra confundida com polarizadas — frases factuais com palavras opinativas
- Por fonte: Gemini gera erros mais frequentes (17,4%) que ChatGPT (9,9%) — vocabulário mais ambíguo

### 13.10. Limitações (admitir com segurança)

1. Dataset sintético com **2 nichos** (Movies + Apps) — não generaliza para todos os domínios
2. Volume de 200/classe nas comparações justas — limita estimativa estatística
3. Sem controle de temperatura nos LLMs (interface web)
4. TF-IDF não captura dependências (negação, ironia) — por isso testamos LSTM/BERT
5. Domínio específico (entretenimento + apps); saúde/política/jurídico podem não generalizar

**Como falar:** "Toda pesquisa tem escopo. Essas limitações não invalidam — definem onde as conclusões valem e apontam trabalhos futuros."

### 13.11. Trabalhos Futuros

- Validação em mais nichos (B2W, Buscape, Olist)
- Mais LLMs geradores (Llama, Mistral) e controle de temperatura via API
- Modelos com embeddings contextuais ainda mais sofisticados (DeBERTa, RoBERTa pt-BR)
- Análise de viés por LLM gerador (debiasing)

### 13.12. Perguntas Genéricas de Banca

- *"Qual a contribuição?"* → "Mostrar que dados sintéticos de múltiplos LLMs são viáveis para treinar classificadores de sentimento em pt-BR, com F1 de até ~84% em domínio sintético, e medir o reality gap quando avaliados em dados reais."
- *"O que faria diferente?"* → "Validação real desde o início e uso de APIs com controle de temperatura."
- *"Aplicação prática?"* → "Empresas sem dados rotulados em pt-BR podem gerar dataset com LLMs e treinar modelo funcional rapidamente, sem custo de anotação humana."
- *"Por que 3 classes e não 2?"* → "Reviews reais têm frases neutras (sinopses, dados factuais). Binário forçaria erro. 3 classes representam melhor a realidade."

---

## 13.13 Diretrizes para reescrita do artigo (Etapa G)

> Definidas pelo Davi em 2026-05-13 baseado em orientação do Prof. Marlon.

O artigo atual (`artigo/main.tex`) está extenso e formal demais. A reescrita na Etapa G precisa:

**Objetivo principal:** ser mais direto. Foco em três blocos: objetivo, ideias centrais e o que foi concluído. O orientador disse que pode reduzir explicações técnicas que não são essenciais (NB, SVM, F1, TF-IDF, etc.) — manter o mínimo necessário pra contextualizar, sem virar tutorial.

**Estrutura obrigatória de resultados — três blocos bem separados e claros:**
1. **Domínio sintético** (V1) — desempenho dos modelos treinados e testados em dados gerados por LLMs
2. **Domínio real** (V2 controlado e V4 desbalanceado natural) — desempenho em reviews reais
3. **Cross-domínio** (V3 e V5) — generalização sintético → real, o achado central do trabalho

Cada bloco precisa estar nomeado de forma explícita no texto e na tabela. Não misturar visões em parágrafos longos.

**Cortes recomendados (orientador autorizou):**
- Reduzir as explicações técnicas profundas de NB, SVM, Regressão Logística, TF-IDF (manter referência rápida + citação)
- Reduzir definições longas de F1, precisão, recall (uma frase de definição já basta)
- Cortar parágrafos repetitivos que reapresentam o mesmo número em palavras diferentes
- Eliminar conectivos formais empolados ("destarte", "outrossim", "no bojo de")

**Manter / fortalecer:**
- Conclusão expandida (Seção 13.X deste briefing) com os quatro argumentos discutidos
- Tabelas consolidadas (5 visões × 5 modelos × 5 métricas) — Movies + Apps
- Gráfico comparativo 200 vs 600 (evidência de que volume não fecha o gap)
- Gráfico consolidado clássicos × LSTM × BERT
- Análise de comprimento de frases por LLM gerador (faltava no artigo original)

**Tom:** prosa corrida no estilo do Davi (skill `escrita-davi-tcc`), sem inflar resultados, sem "wow factor", admitindo limitações com segurança.

---

## 14. Plano Ativo

Plano detalhado das próximas etapas:
**`C:\Users\Davi\.claude\plans\adicione-as-observa-es-que-witty-catmull.md`**

Ordem de execução:
1. ✅ Etapa A — Centralizar BRIEFING (este arquivo)
2. ⏳ Etapa A.2/A.3 — CLAUDE.md e AGENTS.md viram pointers
3. ⏳ Etapa B — V4 desbalanceada no notebook 03
4. ⏳ Etapa C — Notebook 04 (LSTM + BERT)
5. ⏳ Etapa D — Limpeza notebooks antigos
6. ⏳ Etapa E — Pipeline Apps (depende de geração manual de 1800 frases)
7. ⏳ Etapa F — Comparativo entre nichos
8. ⏳ Etapa G — Atualizar artigo (skill `escrita-davi-tcc`)
9. ♾️ Etapa H — atualizar este BRIEFING ao final de CADA etapa

---

*Fim do BRIEFING. Atualize sempre.*

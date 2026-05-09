# BRIEFING TCC — Fonte única de contexto

> **Para qualquer agente (Claude Code, Codex, Claude.ai):** este arquivo é a **fonte única da verdade** sobre o projeto.
> `CLAUDE.md` e `AGENTS.md` são apenas pointers para cá.
> **Atualize SEMPRE este arquivo** ao final de cada etapa relevante (resultado novo, decisão tomada, arquivo criado/movido).

> **Última atualização:** 2026-05-09 — Centralização de contexto + plano LSTM/BERT + V4 desbalanceada

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
├── CLAUDE.md                    # Pointer para BRIEFING
├── AGENTS.md                    # Pointer para BRIEFING
├── README.md                    # Descrição pública do projeto
├── requirements.txt             # Dependências Python
├── artigo/                      # Artigo LaTeX (formato SBC)
│   ├── main.tex
│   ├── sbc-template.sty
│   └── imagens/
├── dados/
│   ├── brutos/                  # 9 CSVs sintéticos (Movies — Claude/Gemini/ChatGPT)
│   ├── brutos_apps/             # (a criar) 9 CSVs sintéticos para Apps
│   └── processado/              # synthetic_dataset.csv, dataset_completo.csv
├── documentos/                  # Regulamentos, checklists, leituras
├── resultados/                  # Gráficos (.png) e métricas (.csv)
├── src/                         # Notebooks Jupyter
│   ├── 00_data_generation.ipynb
│   ├── 01_movies_training.ipynb           # NB/LR/SVM em sintético
│   ├── 02_movies_robustness.ipynb         # CV k=10, learning curves, erros
│   ├── 03_movies_3_visoes.ipynb           # V1/V2/V3/V4 clássicos (Movies)
│   ├── 04_movies_avancado.ipynb           # (a criar) LSTM + BERT/Bertimbau
│   ├── 05_apps_training.ipynb             # (esqueleto)
│   ├── 06_apps_robustness.ipynb           # (esqueleto)
│   ├── 07_apps_3_visoes.ipynb             # (a criar)
│   ├── 08_apps_avancado.ipynb             # (a criar)
│   ├── 09_comparativo_nichos.ipynb        # (a criar)
│   └── dados_reais/                       # cache local do utlc_movies/utlc_apps via kagglehub
├── archive/                     # Versões antigas/fora-de-escopo (ver README local)
│   ├── notebooks/, scripts/, artigo/
│   └── README.md
└── _backup/                     # Backups
```

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
| BERT (Bertimbau) | `transformers` | `neuralmind/bert-base-portuguese-cased`. Fine-tuning: 3 epochs, batch=8, AdamW lr=2e-5 |

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

### Movies — 5 visões clássicas (notebook 03, seed=42) — **F1 weighted / F1 macro**

| Visão | Naive Bayes | Reg. Logística | SVM Linear |
|---|---|---|---|
| V1: Sintético → Sintético (controlado) | **84.09 / 84.09** | 79.78 / 79.78 | 80.81 / 80.81 |
| V2: Real → Real (controlado) | 43.20 / 43.20 | 41.23 / 41.23 | 42.41 / 42.41 |
| V3: Sintético → Real (controlado) | 38.38 / 38.38 | 34.59 / 34.59 | 35.43 / 35.43 |
| V4: Real → Real (desbalanceado) | 64.36 / **38.48** | 70.93 / **52.05** | 70.59 / **51.92** |
| V5: Sintético → Real (desbalanceado) | 49.62 / **33.65** | 47.28 / **33.42** | 47.35 / **33.88** |

*Distribuição real natural:* Positiva 70.77% / Neutra 19.98% / Negativa 9.25% (n=99.758).

**Observações-chave para a defesa:**
- **V1 alto** — sintético tem vocabulário regular por classe
- **V2 ≈ V3 controlados** (~40%) — com 200 frases, real-em-real e sint-em-real performam similar; mostra que parte da queda é por escassez de dados, não só por sintético ruim
- **V4 desbalanceado:** Acurácia 72-75% mas **F1 macro 38-52%** — gap exemplifica viés de classe majoritária. NB sofre mais (38%) que LR/SVM (52%) porque NB confia em P(classe) a priori
- **V5 desbalanceado:** F1 weighted sobe vs V3 (35→47) mas F1 macro CAI (35→33) — modelo treinado em sintético prevê "muita Neutra" (33% no treino), acerta por sorte na distribuição real desbalanceada
- **Reality gap consistente** (~30 pontos em F1 macro) entre treino sintético e treino real, em qualquer regime de volume
- **Volume real ajuda muito** (V2 43% → V4 71% em F1w no LR/SVM); volume não compensa o gap de fonte (V3≈V5 em F1 macro)

**Arquivos gerados:**
- `resultados/metricas_5_visoes_movies.csv` (+ alias `metricas_3_visoes_movies.csv`)
- `resultados/grafico_5_visoes_movies.png` (F1 weighted, 5 colunas × 3 modelos)
- `resultados/grafico_5_visoes_movies_5metricas.png` (painel 2×3 com 5 métricas)
- `resultados/grafico_5_visoes_movies_{acuracia,precisao,recall,f1score,f1macro}.png` (individuais)

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

1. **Passo a passo incremental** — um passo por vez, verificável.
2. **Bloco-por-bloco com pergunta-teste** — Claude explica + questiona Davi para garantir entendimento.
3. **Antes de alterar código, checar impacto no pipeline** (`⚠️ SYNC:` se afetar cadeia 01→02→03).
4. **Nunca inventar métricas** — pedir para executar o notebook.
5. **seed=42** em todo código com aleatoriedade (numpy, sklearn, torch).
6. **Artigo formato SBC** — não alterar template (`sbc-template.sty`).
7. **Skill `escrita-davi-tcc` obrigatória** antes de qualquer adição/edição em `artigo/main.tex`.
8. **Idioma:** pt-BR.
9. **Nada deletado** — fora-de-escopo vai para `archive/`.
10. **Atualizar este BRIEFING ao final de CADA etapa** (Histórico de Execução abaixo).

---

## 11. Histórico de Execução (rolling, mais recente no topo)

### 2026-05-09 — Reorganização e novas demandas

- ✅ **Etapa A:** BRIEFING_TCC.md reescrito centralizando tudo (CLAUDE.md, AGENTS.md, MODO DEFESA). Pointers reduzidos.
- ⏳ **Etapa B (próxima):** adicionar V4 desbalanceada ao notebook 03
- ⏳ **Etapa C (após):** criar `04_movies_avancado.ipynb` (LSTM + BERT)
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

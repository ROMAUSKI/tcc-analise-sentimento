# BRIEFING TCC — Fonte única de contexto

> **Para qualquer agente (Claude Code, Codex, Claude.ai):** este arquivo é a **fonte única da verdade** sobre o projeto.
> `CLAUDE.md` e `AGENTS.md` são apenas pointers para cá.
> **Atualize SEMPRE este arquivo** ao final de cada etapa relevante (resultado novo, decisão tomada, arquivo criado/movido).

> **Última atualização:** 2026-05-09 — bootstrap local Python 3.12 + CUDA na célula 1 do notebook 04 + plano LSTM/BERT + V4 desbalanceada

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

---

## 11. Histórico de Execução (rolling, mais recente no topo)

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

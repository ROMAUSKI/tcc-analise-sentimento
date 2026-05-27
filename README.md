# Utilização de LLMs para Geração de Bases de Treinamento em Classificação de Sentimento

### Uma análise de viabilidade prática

![Python](https://img.shields.io/badge/Python-3.12-blue)
![Área](https://img.shields.io/badge/NLP-An%C3%A1lise%20de%20Sentimento-success)
![Artigo](https://img.shields.io/badge/Artigo-Formato%20SBC-orange)
![Status](https://img.shields.io/badge/Status-Conclu%C3%ADdo-brightgreen)

**Trabalho de Conclusão de Curso — Engenharia de Software**
Universidade Tecnológica Federal do Paraná — Câmpus Dois Vizinhos (UTFPR-DV)

**Autor:** Davi Romauski Meurer · **Orientador:** Prof. Marlon Marcon

---

## Sobre o trabalho

Este trabalho investiga uma pergunta prática: dá para treinar um classificador de sentimento usando apenas frases geradas por LLMs, sem nenhum dado rotulado por humanos? A motivação é direta. Montar um dataset rotulado à mão é caro e demorado, ainda mais em português brasileiro, onde sobra pouco recurso anotado se comparado ao inglês. Se um modelo como ChatGPT, Gemini ou Claude consegue gerar essas frases já rotuladas, parte desse custo desaparece — desde que os modelos treinados nesses dados realmente funcionem sobre texto real.

Para testar isso de verdade, foram construídos dois datasets sintéticos de **1.800 frases cada**, em dois nichos diferentes: críticas de filmes e séries e reviews de aplicativos móveis. Cada dataset tem 600 frases por classe (positiva, negativa e neutra), divididas igualmente entre os três LLMs. Em cima disso, cinco classificadores foram treinados e avaliados sob cinco visões metodológicas, que vão desde treinar e testar tudo em dados sintéticos até treinar em sintético e testar em reviews reais de usuários — que é o cenário que realmente importa para saber se a ideia se sustenta na prática.

### Perguntas de pesquisa

1. Qual a assertividade de classificadores treinados exclusivamente com dados sintéticos?
2. Há coerência entre os dados produzidos por diferentes LLMs geradores?
3. Modelos treinados em dados sintéticos se saem bem quando são submetidos a dados reais (avaliação *cross-domain*)?

---

## As cinco visões metodológicas

O coração do método é comparar a mesma tarefa sob cinco recortes diferentes de treino e teste. As visões V4 e V5 usam a distribuição natural e desbalanceada das reviews reais (cerca de 71% positivas, 20% neutras e 9% negativas em filmes; 72% positivas, 21% negativas e 7% neutras em apps), que é o que se encontra em produção.

| Visão | Treino | Teste | O que mede |
|---|---|---|---|
| **V1** | Sintético | Sintético | Teto do dado sintético — coerência interna entre as frases geradas |
| **V2** | Real | Real | Baseline com dados reais, em volume controlado e balanceado |
| **V3** | Sintético | Real | *Cross-domain* controlado (mesmo volume por classe nos dois lados) |
| **V4** | Real | Real | Baseline na distribuição natural desbalanceada |
| **V5** | Sintético | Real | *Cross-domain* realista — o cenário mais próximo de produção |

---

## Principais resultados

A ideia funciona bem só no papel. Treinando e testando em dados sintéticos (V1), o BERTimbau chega a **97% de F1-macro**, o que mostra que as frases geradas são coerentes entre si. Mas quando esse mesmo modelo é treinado em sintético e testado em reviews reais no cenário desbalanceado e realista (V5), o F1-macro cai para **43% em filmes e séries** e **56% em aplicativos**. Esse buraco continua mesmo triplicando o volume de treino sintético, o que indica que o problema não é falta de dado: é uma diferença estrutural entre como o LLM escreve e como o usuário real escreve.

| Cenário | Visão | Melhor modelo | F1-macro |
|---|---|---|---|
| Sintético → Sintético | V1 | BERTimbau | **97%** |
| *Cross-domain* realista (desbalanceado) | V5 | BERTimbau | **43%** filmes · **56%** apps |

Podemos afirmar, então, que usar dados puramente sintéticos para treinar um classificador que vai rodar sobre texto real ainda é inviável para esse tipo de tarefa. A diferença grande entre os dois nichos também sugere algo interessante: quanto mais regular e objetivo é o domínio de avaliação, mais o dado sintético se aproxima de funcionar. A discussão completa, com as tabelas por modelo e as matrizes de confusão, está no artigo em `artigo/main.pdf`.

---

## Estrutura do repositório

```
tcc-analise-sentimento/
├── artigo/                         # Artigo em LaTeX (formato SBC)
│   ├── main.tex                    # Fonte do artigo
│   ├── main.pdf                    # Artigo compilado
│   ├── referencias.bib             # Referências citadas
│   ├── sbc-template.sty, sbc.bst   # Template SBC
│   └── imagens/                    # Figuras usadas no artigo
│
├── src/                            # Notebooks e scripts
│   ├── 00_data_generation.ipynb    # Documentação da geração dos dados via LLMs
│   ├── 01_movies_training.ipynb    # Filmes: NB/LR/SVM em sintético
│   ├── 02_movies_robustness.ipynb  # Filmes: validação cruzada, curvas, análise de erros
│   ├── 03_movies_3_visoes.ipynb    # Filmes: as cinco visões (clássicos)
│   ├── 04_movies_avancado.ipynb    # Filmes: LSTM + BERTimbau
│   ├── 05_apps_training.ipynb      # Apps: NB/LR/SVM em sintético
│   ├── 06_apps_robustness.ipynb    # Apps: validação cruzada, curvas, análise de erros
│   ├── 07_apps_3_visoes.ipynb      # Apps: as cinco visões (clássicos)
│   ├── 08_apps_avancado.ipynb      # Apps: LSTM + BERTimbau
│   └── _gerar_*.py                 # Scripts que geram as figuras do artigo
│
├── dados/
│   ├── brutos/                     # 9 CSVs sintéticos de filmes (3 classes × 3 LLMs)
│   ├── brutos_apps/                # 9 CSVs sintéticos de apps  (3 classes × 3 LLMs)
│   └── processado/                 # Datasets unificados (synthetic_dataset.csv e _apps)
│
├── resultados/                     # Gráficos (.png) e métricas (.csv)
│   └── metricas_consolidado_geral.csv   # Fonte única dos números do artigo
│
├── documentos/                     # Notas de leitura e referências
├── archive/                        # Versões antigas e experimentos fora de escopo
├── requirements.txt                # Dependências Python
└── BRIEFING_TCC.md                 # Documento interno com o estado completo do projeto
```

Os dados reais (UTLC-Movies e UTLC-Apps) **não são versionados** porque são pesados (~877 MB). Eles são baixados sob demanda via `kagglehub` na primeira execução dos notebooks de *cross-domain*. O mesmo vale para os checkpoints de fine-tuning do BERTimbau e do LSTM, que são regenerados ao rodar os notebooks avançados.

---

## Como replicar

Os notebooks detectam automaticamente se estão rodando no Google Colab ou localmente e ajustam os caminhos sozinhos. O **seed é 42** em todo o código com aleatoriedade (numpy, scikit-learn e PyTorch), o que mantém os resultados reproduzíveis.

### No Google Colab

Basta abrir qualquer notebook no Colab e executar as células na ordem. O próprio notebook clona o repositório e prepara o ambiente. É o caminho mais simples para os notebooks avançados (04 e 08), que usam GPU para o BERTimbau.

### Localmente

```bash
# 1. Clonar o repositório
git clone https://github.com/ROMAUSKI/tcc-analise-sentimento.git
cd tcc-analise-sentimento

# 2. (Opcional, para usar GPU no BERTimbau/LSTM) instalar o PyTorch com CUDA ANTES
pip install torch --index-url https://download.pytorch.org/whl/cu121

# 3. Instalar as demais dependências
pip install -r requirements.txt

# 4. Rodar os notebooks na ordem
#    Filmes: 01 -> 02 -> 03 -> 04
#    Apps:   05 -> 06 -> 07 -> 08
```

Os dados sintéticos já vêm no repositório, em `dados/`. Os dados reais são baixados automaticamente via `kagglehub` (dataset `fredericods/ptbr-sentiment-analysis-datasets`) quando um notebook de *cross-domain* roda pela primeira vez — para isso é preciso ter um token do Kaggle configurado. As reviews reais usam o mapeamento de nota para classe: nota maior ou igual a 4 vira positiva, igual a 3 vira neutra e menor ou igual a 2 vira negativa.

### Regerar as figuras do artigo

```bash
python src/_gerar_comparativo_nichos.py     # Figura comparativa dos dois nichos
python src/_gerar_200vs600_macro.py          # Experimento de volume (200 vs 600 frases)
python src/_gerar_comprimento_frases.py      # Boxplot do comprimento das frases
python src/_gerar_matriz_v3_svm.py           # Matriz de confusão (V3, SVM, filmes)
```

### Compilar o artigo

```bash
cd artigo
latexmk -pdf main.tex
# ou, manualmente: pdflatex main -> bibtex main -> pdflatex main -> pdflatex main
```

---

## Tecnologias

- **Linguagem:** Python 3.12
- **Clássicos:** scikit-learn (Naive Bayes, Regressão Logística, SVM Linear), vetorização TF-IDF
- **Neurais:** PyTorch e Transformers (LSTM e BERTimbau — `neuralmind/bert-base-portuguese-cased`)
- **Dados e gráficos:** pandas, NLTK, matplotlib, seaborn
- **Dados reais:** kagglehub
- **Artigo:** LaTeX no formato SBC

---

## Licença

Projeto desenvolvido como Trabalho de Conclusão de Curso. Uso livre para fins educacionais e acadêmicos.

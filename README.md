# Análise de Sentimento com Dados Sintéticos Gerados por LLMs

**Trabalho de Conclusão de Curso** — Engenharia de Software
Universidade Tecnológica Federal do Paraná — Câmpus Dois Vizinhos (UTFPR-DV)

**Autor:** Davi Romauski Meurer
**Orientador:** Prof. Marlon Marcon

## Sobre

Este projeto investiga se dados sintéticos gerados por três LLMs distintos — **ChatGPT**, **Gemini** e **Claude** — são suficientes para treinar modelos clássicos de aprendizado de máquina capazes de classificar o sentimento de críticas de filmes e séries em português brasileiro.

### Perguntas de Pesquisa

1. Qual a assertividade dos modelos treinados com dados sintéticos?
2. A classificação é coerente entre os diferentes LLMs geradores?

## Dataset

- **1.798 frases** sintéticas geradas integralmente por LLMs
- **3 classes:** Positiva (600), Negativa (598), Neutra (600)
- **3 fontes:** ChatGPT, Gemini, Claude (~200 frases por classe por LLM)
- Pré-processamento: remoção de duplicatas, caracteres especiais, normalização para minúsculas

## Modelos e Resultados

### Avaliação no Conjunto de Teste (80/20, seed=42)

| Modelo | Acurácia | Precisão | Recall | F1-Score |
|---|---|---|---|---|
| Naive Bayes | 86.11% | 86.19% | 86.11% | 86.13% |
| SVM Linear | 86.11% | 86.21% | 86.11% | 86.09% |
| Regressão Logística | 83.61% | 83.80% | 83.61% | 83.54% |

### Validação Cruzada Estratificada

| Modelo | F1-Score (k=5) | F1-Score (k=10) |
|---|---|---|
| SVM Linear | 88.88% ± 1.33 | 89.10% ± 2.51 |
| Naive Bayes | 88.86% ± 1.82 | 89.63% ± 2.15 |
| Regressão Logística | 87.31% ± 1.42 | 88.02% ± 2.44 |

Vetorização: TF-IDF | Split: 80/20 estratificado | Seed: 42

## Estrutura do Projeto

```
├── src/                              # Notebooks Jupyter
│   ├── 00_data_generation.ipynb      # Documentação da geração dos dados
│   ├── 01_training_evaluation.ipynb  # Pipeline: unificação, TF-IDF, treino, métricas
│   └── 02_robustness_analysis.ipynb  # CV, curvas de aprendizado, análise de erros
│
├── dados/
│   ├── brutos/                       # 9 CSVs gerados por cada LLM (3 classes × 3 fontes)
│   └── processado/                   # Dataset unificado (synthetic_dataset.csv)
│
├── resultados/                       # Gráficos (.png) e métricas (.csv)
│
├── artigo/                           # Artigo LaTeX (formato SBC)
│
├── documentos/                       # Notas de leitura e referências
│   ├── notas_leitura.md
│   └── referencias/                  # PDFs dos artigos citados
│
└── BRIEFING_TCC.md                   # Estado atual do projeto (doc interno)
```

## Como Executar

Os notebooks detectam automaticamente o ambiente (Google Colab ou local).

**No Google Colab:**
1. Abra o notebook no Colab — ele clona o repo automaticamente
2. Execute as células na ordem

**Localmente:**
1. Clone o repositório
2. Instale as dependências: `pip install pandas scikit-learn matplotlib seaborn nltk`
3. Execute os notebooks na ordem: `00` → `01` → `02`

## Tecnologias

- Python 3 | pandas | scikit-learn | matplotlib | seaborn | NLTK
- TF-IDF (vetorização) | MultinomialNB | LogisticRegression | LinearSVC
- LaTeX (artigo formato SBC) | Google Colab

## Licença

Este projeto é parte de um trabalho acadêmico. Uso livre para fins educacionais.

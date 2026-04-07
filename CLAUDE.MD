# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Projeto

- **Título:** Análise de Sentimentos em Críticas de Cinema com Dados Sintéticos Gerados por LLMs
- **Aluno:** Davi Romauski Meurer — UTFPR Dois Vizinhos, Eng. Software, 8º sem.
- **Orientador:** Prof. Marlon Marcon
- **Repo:** https://github.com/ROMAUSKI/tcc-analise-sentimento

## Perguntas de Pesquisa

1. Qual a assertividade dos modelos treinados com dados sintéticos?
2. A classificação é coerente entre os diferentes LLMs geradores?

## Comandos

```bash
# Instalar dependências localmente
pip install pandas scikit-learn matplotlib seaborn nltk wordcloud

# Executar notebooks (ordem obrigatória)
jupyter notebook src/01_training_evaluation.ipynb
jupyter notebook src/02_robustness_analysis.ipynb

# Compilar artigo LaTeX (ou usar Overleaf)
cd artigo && latexmk -pdf main.tex
```

## Arquitetura e Fluxo de Dados

### Pipeline (ordem obrigatória)

```
dados/brutos/ (9 CSVs)
  → 01_training_evaluation.ipynb (unifica, limpa, vetoriza, treina, avalia)
    → dados/processado/synthetic_dataset.csv
    → resultados/baseline_metrics.csv + gráficos (.png)
      → 02_robustness_analysis.ipynb (cross-validation, curvas de aprendizado, análise de erros)
        → resultados/*.csv + resultados/*.png
          → artigo/imagens/ (cópia manual dos gráficos relevantes)
```

**Dependência crítica:** O notebook `02` consome `synthetic_dataset.csv` gerado pelo `01`. Alteração no `01` pode quebrar o `02` — sempre verificar a cadeia.

### Detecção de ambiente nos notebooks

Ambos os notebooks detectam automaticamente Colab vs local na Célula 1:
- **Notebook 01:** usa `'google.colab' in sys.modules` → clona o repo se no Colab
- **Notebook 02:** usa `os.path.exists('/content')` → clona/pull se no Colab; local usa `os.path.join(os.getcwd(), '..')`

### Dataset

- **Arquivo:** `dados/processado/synthetic_dataset.csv`
- **Colunas:** `frase_limpa` (X), `classe` (y), `fonte` (LLM gerador), `frase` (original)
- **1798 linhas** — 3 classes (Positiva ~600, Negativa ~598, Neutra ~600) × 3 fontes (ChatGPT, Claude, Gemini)
- **Split:** 80/20 estratificado, seed=42
- **Vetorização:** TF-IDF (max_features=5000)

### Modelos

| Modelo | Classe sklearn |
|---|---|
| Naive Bayes (baseline) | `MultinomialNB()` |
| Regressão Logística | `LogisticRegression(max_iter=1000)` |
| SVM Linear | `LinearSVC(max_iter=5000)` |

Todos encapsulados em `Pipeline([('tfidf', TfidfVectorizer(...)), ('clf', ...)])`.

### Artigo (LaTeX formato SBC)

- **Arquivo principal:** `artigo/main.tex`
- Template SBC: `sbc-template.sty`, `sbc.bst`
- Imagens em `artigo/imagens/` — copiadas de `resultados/`
- Seções: Introdução, Fund. Teórica, Trab. Relacionados, Metodologia, Resultados, Conclusão

## Regras do Projeto

1. Passo a passo incremental — um passo por vez, verificável
2. Antes de alterar código, checar impacto no pipeline (`⚠️ SYNC:`)
3. **Nunca inventar métricas** — pedir para executar o notebook
4. seed=42 em todo código com aleatoriedade
5. Artigo formato SBC — não alterar template

## Estado Atual (Abril/2026)

- ✅ Dataset gerado e processado
- ✅ Notebook 01 completo (treinamento + avaliação baseline)
- ✅ Notebook 02 completo (cross-validation, boxplots, learning curves, análise de erros)
- ✅ Artigo: PRIMEIRA VERSÃO COMPLETA (Seções 1-6 + Resumo + Abstract)
- ❌ Revisão final do artigo (leitura corrida, ortografia, consistência)
- ❌ Slides: não iniciados

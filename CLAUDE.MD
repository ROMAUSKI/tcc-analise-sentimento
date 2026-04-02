# TCC — Análise de Sentimentos com Dados Sintéticos

## Projeto
- **Título:** Análise de Sentimentos em Críticas de Cinema com Dados Sintéticos Gerados por LLMs
- **Aluno:** Davi Romauski Meurer — UTFPR Dois Vizinhos, Eng. Software, 8º sem.
- **Orientador:** Prof. Marlon Marcon
- **Repo:** https://github.com/ROMAUSKI/tcc-analise-sentimento

## Perguntas de Pesquisa
1. Qual a assertividade dos modelos treinados com dados sintéticos?
2. A classificação é coerente entre os diferentes LLMs geradores?

## Estrutura de Pastas
```
tcc-analise-sentimento/
├── artigo/                        # LaTeX (formato SBC) — main.tex, referencias.bib
├── dados/
│   ├── brutos/                    # 9 CSVs brutos (Claude, Gemini, ChatGPT — 3 classes cada)
│   └── processado/                # dataset_completo.csv + synthetic_dataset.csv (1798 linhas)
├── documentos/                    # Regulamentos UTFPR
├── resultados/                    # Gráficos .png + métricas .csv
└── src/
    ├── 00_data_generation.ipynb   # Documentação (não executa) ✅
    ├── 01_training_evaluation.ipynb # Pipeline principal ✅
    └── 02_robustness_analysis.ipynb # Robustez (em progresso) 🔧
```

## Pipeline (ordem obrigatória)
`01` gera `synthetic_dataset.csv` → `02` consome → gera `resultados/` → `artigo/imagens/`

## Dados Técnicos
- **Colunas:** `frase_limpa` (X), `classe` (y)
- **Classes:** Positiva, Negativa, Neutra
- **Dataset:** 1798 linhas (600 por classe)
- **Split:** 80/20 treino/teste | seed=42
- **Vetorização:** TF-IDF
- **Modelos:** MultinomialNB (baseline), LogisticRegression
- **Stack:** Python 3, pandas, scikit-learn, matplotlib, seaborn, nltk

## Resultados Atuais
| Modelo | Acurácia | F1-Score |
|---|---|---|
| Naive Bayes | 90.28% | 90.30% |
| Regressão Logística | 85.83% | 85.84% |
| NB Cross-val k=10 | 89.10% | 89.11% ±1.82% |
| LR Cross-val k=10 | 87.60% | 87.53% ±2.78% |

## Ambiente
- Execução: **Google Colab** (principal) ou VS Code local
- Artigo: **Overleaf** (LaTeX/SBC)
- Notebooks detectam ambiente automaticamente na Célula 1

## Regras do Projeto
1. Passo a passo incremental — um passo por vez
2. Antes de alterar, checar impacto no pipeline (`⚠️ SYNC:`)
3. Nunca inventar métricas — pedir para executar o notebook
4. Alteração no 01 pode quebrar o 02 — verificar cadeia
5. Artigo formato SBC — seções: Resumo, Introdução, Referencial, Metodologia, Resultados, Conclusão

## Estado Atual (Abril/2026)
- ✅ Dataset gerado e processado
- ✅ Notebook 01 completo (treinamento + avaliação baseline)
- ✅ Notebook 02 completo (cross-validation, boxplots, learning curves, análise de erros)
- ✅ Artigo: Seções 1-5 completas (Introdução, Fund. Teórica, Trab. Relacionados, Metodologia, Resultados)
  - 5.1 Avaliação no Conjunto de Teste ✅
  - 5.2 Validação Cruzada ✅ (tabela + boxplots separados accuracy/f1)
  - 5.3 Curvas de Aprendizado ✅ (figuras NB, LR e SVM)
  - 5.4 Análise de Erros ✅ (por fonte + heatmap)
  - 5.5 Discussão Geral ✅
- ❌ Artigo: Seção 6 Conclusão (TODO)
- ❌ Artigo: Resumo e Abstract (TODO — escrever por último)
- ❌ Slides: não iniciados
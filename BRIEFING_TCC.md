# BRIEFING TCC — Leia isso antes de qualquer coisa

> Arquivo de contexto compartilhado entre Claude Code e Claude.ai.
> Atualizar sempre que houver mudança relevante no projeto.

---

## Projeto

**Título:** Análise de Sentimentos em Críticas de Cinema com Dados Sintéticos Gerados por LLMs
**Aluno:** Davi (UTFPR)
**Repositório:** https://github.com/ROMAUSKI/tcc-analise-sentimento

---

## Estrutura de Pastas

```
TCC/
├── artigo/          # Artigo LaTeX (formato SBC)
├── dados/
│   ├── brutos/      # 9 CSVs gerados por Claude, Gemini e ChatGPT
│   └── processado/  # dataset_completo.csv e synthetic_dataset.csv
├── documentos/      # Regulamentos e checklists da UTFPR
├── resultados/      # Gráficos (.png) e métricas (.csv)
├── src/             # Notebooks Jupyter (pipeline completo)
│   ├── 00_data_generation.ipynb    # Planejamento (não executa)
│   ├── 01_training_evaluation.ipynb # Pipeline principal
│   └── 02_robustness_analysis.ipynb # Análise de robustez
└── _backup/         # Backups antigos
```

---

## Estado Atual

**Última atualização:** 21/03/2026
**Branch:** main
**Último commit:** `22d6e9b — feat(nb02): curvas de aprendizado NB e LR` (pendente commit com SVM, análise de erros, tabela consolidada e refatoração)

### O que já foi feito
- [x] Geração dos 9 datasets sintéticos (manualmente via interfaces web)
- [x] Refactor da estrutura de pastas do projeto
- [x] Correção dos caminhos do notebook `01` para nova estrutura
- [x] Notebook `01` — Setup com detecção automática Colab/Local
- [x] Notebook `01` — Pipeline completo: LR, NB e SVM Linear (treino, avaliação, gráficos)
- [x] Notebook `01` — Validação cruzada k=10 para NB
- [x] Notebook `01` — Texto para o artigo + referências sugeridas
- [x] Notebook `02` — Setup com detecção automática Colab/Local
- [x] Notebook `02` — Validação cruzada (Accuracy + F1-Score) para NB, LR e SVM com k=5 e k=10
- [x] Notebook `02` — Salvar tabela comparativa em `resultados/validacao_cruzada.csv`
- [x] Notebook `02` — Boxplot comparativo Accuracy e F1-Score por modelo/k-fold
- [x] Notebook `02` — Curvas de aprendizado (NB, LR e SVM) com F1-Score treino vs validação
- [x] Notebook `02` — Análise de erros do Naive Bayes (erros por fonte, confusões, exemplos)
- [x] Notebook `02` — Tabela consolidada `resultados/metricas_consolidadas.csv`
- [x] Notebook `02` — Texto para o artigo + referências sugeridas
- [x] Refatoração dos notebooks para código mais natural e acadêmico
- [x] Execução local dos dois notebooks com outputs gerados

### Pendente — Notebook 02
- [ ] Teste com dados reais (ex: AdoroCinema ou IMDb-pt) — validação externa para sair da "bolha sintética"

### Pendente — Artigo
- [ ] Escrever artigo no formato SBC com base nos textos dos notebooks
- [ ] Ler as referências sugeridas nos notebooks antes de escrever
- [ ] Seção de Metodologia: dataset, pré-processamento, modelos, métricas
- [ ] Seção de Resultados: baseline, validação cruzada, curvas de aprendizado, análise de erros
- [ ] Seção de Discussão: limitações (dados sintéticos), diferenças entre LLMs, limitações do bag-of-words
- [ ] Seção de Trabalhos Futuros: validação com dados reais, modelos com embeddings/transformers

### Pendente — Geral
- [ ] Monografia
- [ ] Commit + push das alterações pendentes

---

## Resultados dos Modelos Baseline (Notebook 01)

> Valores aproximados — variam levemente a cada execução devido ao split aleatório.

| Modelo | Acurácia | Precisão | Recall | F1-Score |
|---|---|---|---|---|
| Naive Bayes | ~86% | ~86% | ~86% | ~86% |
| SVM Linear | ~86% | ~86% | ~86% | ~86% |
| Regressão Logística | ~84% | ~84% | ~84% | ~84% |

## Resultados da Validação Cruzada (Notebook 02)

| Modelo | k | Accuracy Média | F1 Média |
|---|---|---|---|
| SVM Linear | 5 | ~89% ±1.3 | ~89% ±1.3 |
| Naive Bayes | 5 | ~89% ±1.8 | ~89% ±1.8 |
| Reg. Logística | 5 | ~87% ±1.4 | ~87% ±1.4 |
| SVM Linear | 10 | ~89% ±2.5 | ~89% ±2.5 |
| Naive Bayes | 10 | ~90% ±2.2 | ~90% ±2.2 |
| Reg. Logística | 10 | ~88% ±2.4 | ~88% ±2.4 |

## Resultados da Análise de Erros (Notebook 02)

- **Total de erros:** ~50/360 (~14%) no Naive Bayes
- **Confusão mais frequente:** Negativa ↔ Positiva (~24 erros combinados)
- **Erros por fonte:** ChatGPT ~10% | Claude ~14% | Gemini ~17%
- **Padrão:** Gemini gera frases mais ambíguas; ChatGPT é mais direto no sentimento

> **Arquivos gerados:** `resultados/validacao_cruzada.csv`, `resultados/metricas_consolidadas.csv`, `resultados/baseline_metrics.csv`, `resultados/boxplot_validacao_cruzada.png`, `resultados/curva_aprendizado_nb.png`, `resultados/curva_aprendizado_lr.png`, `resultados/analise_erros.csv`, `resultados/analise_erros_graficos.png`, gráficos de F1/confusão por modelo
> **Observação crítica:** Toda validação até agora usa dados sintéticos. Falta teste com dados reais.

**Dataset:** 1798 frases únicas (600 por classe: Positiva, Negativa, Neutra)
**Fontes:** Claude, Gemini, ChatGPT (200 frases cada por classe)
**Vetorização:** TF-IDF | **Divisão:** 80% treino / 20% teste | **Seed:** 42

---

## Observações Técnicas

- Notebooks rodam no **Google Colab** ou **VS Code local** (célula 1 detecta automaticamente)
- No Colab: clona o repo do GitHub automaticamente
- No VS Code: usa caminhos relativos a partir da raiz do projeto
- Caminhos dos dados: `dados/brutos/` → `dados/processado/` → `resultados/`
- Git configurado com `safe.directory` para o path local do Windows
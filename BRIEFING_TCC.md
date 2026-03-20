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

**Última atualização:** 19/03/2026
**Branch:** main
**Último commit:** `8bc81ba — feat(nb02): validação cruzada com Accuracy e F1-Score` (pendente commit do notebook 02 com curvas de aprendizado)

### O que já foi feito
- [x] Geração dos 9 datasets sintéticos (manualmente via interfaces web)
- [x] Refactor da estrutura de pastas do projeto
- [x] Correção dos caminhos do notebook `01` para nova estrutura
- [x] Execução do notebook `01` no Colab (resultados abaixo)
- [x] Notebook `02` — Célula 1: setup com detecção automática Colab/Local
- [x] Notebook `02` — Célula 2: validação cruzada (Accuracy + F1-Score) para NB e LR com k=5 e k=10
- [x] Notebook `02` — Célula 3: salvar tabela comparativa em `resultados/validacao_cruzada.csv`
- [x] Notebook `02` — Célula 4: boxplot comparativo Accuracy e F1-Score por modelo/k-fold
- [x] Notebook `02` — Célula 5: curvas de aprendizado (NB e LR) com F1-Score treino vs validação
- [x] Notebook `02` — Célula 6: análise markdown (overfitting, platô, convergência)

### Pendente — Notebook 02
- [ ] Teste com dados reais (ex: AdoroCinema ou IMDb-pt) — validação externa para sair da "bolha sintética"
- [ ] Commit + push das alterações do notebook 02

### Pendente — Geral
- [ ] Revisar e finalizar artigo com os resultados
- [ ] Monografia
- [ ] Tratar no artigo a limitação: validação feita apenas com dados sintéticos (seção de Limitações)

---

## Resultados dos Modelos Baseline (Notebook 01)

| Modelo | Acurácia | Precisão | Recall | F1-Score |
|---|---|---|---|---|
| Regressão Logística | 85.83% | 85.86% | 85.83% | 85.84% |
| Naive Bayes | 90.28% | 90.57% | 90.28% | 90.30% |

## Resultados da Validação Cruzada (Notebook 02)

| Modelo | k | Accuracy Média | Accuracy DP | F1 Média | F1 DP |
|---|---|---|---|---|---|
| Naive Bayes | 5 | 89.10% | ±0.72% | 89.11% | ±0.73% |
| Naive Bayes | 10 | 89.10% | ±1.81% | 89.11% | ±1.82% |
| Regressão Logística | 5 | 87.04% | ±1.52% | 87.00% | ±1.54% |
| Regressão Logística | 10 | 87.60% | ±2.70% | 87.53% | ±2.78% |

> **Arquivos gerados:** `resultados/validacao_cruzada.csv`, `resultados/boxplot_validacao_cruzada.png`, `resultados/curva_aprendizado_nb.png`, `resultados/curva_aprendizado_lr.png`
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

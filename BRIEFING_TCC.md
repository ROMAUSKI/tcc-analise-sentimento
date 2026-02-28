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

**Última atualização:** 27/02/2026
**Branch:** main (limpo)
**Último commit:** `83bf102 — fix: atualizar caminhos do notebook 01`

### O que já foi feito
- [x] Geração dos 9 datasets sintéticos (manualmente via interfaces web)
- [x] Refactor da estrutura de pastas do projeto
- [x] Correção dos caminhos do notebook `01` para nova estrutura
- [x] Execução do notebook `01` no Colab (resultados abaixo)

### Pendente
- [ ] Executar notebook `02` (análise de robustez)
- [ ] Revisar e finalizar artigo com os resultados
- [ ] Monografia

---

## Resultados dos Modelos Baseline

| Modelo | Acurácia | Precisão | Recall | F1-Score |
|---|---|---|---|---|
| Regressão Logística | 85.83% | 85.86% | 85.83% | 85.84% |
| Naive Bayes | 90.28% | 90.57% | 90.28% | 90.30% |
| NB (Validação Cruzada, k=10) | — | — | — | 89.12% ± 2.2% |

**Dataset:** 1798 frases únicas (600 por classe: Positiva, Negativa, Neutra)
**Fontes:** Claude, Gemini, ChatGPT (200 frases cada por classe)
**Vetorização:** TF-IDF | **Divisão:** 80% treino / 20% teste | **Seed:** 42

---

## Observações Técnicas

- Notebooks rodam no **Google Colab** (não localmente)
- Se o repo já estava clonado no Colab, rodar antes: `!rm -rf tcc-analise-sentimento` para puxar atualizações
- Caminhos dos dados: `dados/brutos/` → `dados/processado/` → `resultados/`
- Git configurado com `safe.directory` para o path local do Windows

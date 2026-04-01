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

**Última atualização:** 31/03/2026
**Branch:** main

### Semana 1 do checklist — CONCLUÍDA (parte técnica)
- [x] Geração dos 9 datasets sintéticos (manualmente via interfaces web)
- [x] Refactor da estrutura de pastas do projeto
- [x] Notebook `01` — Setup Colab/Local, pipeline completo com LR, NB e SVM Linear
- [x] Notebook `01` — Validação cruzada k=10 para NB
- [x] Notebook `02` — Setup Colab/Local
- [x] Notebook `02` — Validação cruzada (Accuracy + F1) para NB, LR e SVM com k=5 e k=10
- [x] Notebook `02` — Boxplot comparativo, curvas de aprendizado (NB, LR, SVM)
- [x] Notebook `02` — Análise de erros do NB (erros por fonte, confusões, 15 exemplos)
- [x] Notebook `02` — Tabela consolidada `resultados/metricas_consolidadas.csv`
- [x] Refatoração dos notebooks (código mais natural, menos cara de IA)
- [x] Re-execução local dos dois notebooks com todos os outputs gerados
- [x] SVM Linear como terceiro modelo (dia 5 — opcional, feito)
- [x] `CONCLUSOES.md` — documento-base para o artigo com todas as seções, figuras e referências
- [x] Remoção da pasta duplicada `src/tcc-analise-sentimento/` (clone antigo)
- [x] Git atualizado

### Pendente — Semana 1 (não é código)
- [ ] Falar com o orientador (marcar reunião, confirmar formato de entrega)

### Semana 2 do checklist — CONCLUÍDA (pesquisa + escrita)
- [x] Ler artigos das referências (11 artigos anotados no Dia 8 e 9)
- [x] Criar `documentos/notas_leitura.md` com anotações de cada artigo
- [x] Pesquisar 2-3 artigos sobre avaliação de modelos NLP (Dia 10)
- [x] Pesquisar TCCs/artigos da UTFPR sobre tema similar (Dia 10)
- [x] Atualizar `artigo/referencias.bib` — agora com 16 referências (meta: 10-12 ✅)
- [x] Limpar template SBC — removido todo texto de exemplo (Dia 11)
- [x] Substituir autores e afiliações (Davi + Marlon, UTFPR DV) (Dia 11)
- [x] Criar estrutura de seções: Intro / Fund. Teórica / Trab. Relacionados / Metodologia / Resultados / Conclusão (Dia 11)
- [x] Escrever rascunho da Introdução (~1 página, 5 parágrafos) (Dia 11)
- [x] Adicionar subseção de Métricas de Avaliação na Fundamentação Teórica (Dia 11)
- [x] Escrever Trabalhos Relacionados — revisado com 3 subseções + posicionamento (Dia 12)
- [x] Metodologia completa — 7 subseções com tabela do dataset (Dia 13)

### Semana 3 do checklist — EM PROGRESSO (resultados + discussão + ajustes visuais)
- [x] Copiar gráficos de `resultados/` para `artigo/imagens/` (8 PNGs)
- [x] Escrever Resultados e Discussão — 5 subseções com 3 tabelas e 6 figuras (Dia 15)
- [x] Dividir figuras compostas em individuais para melhor legibilidade (Dia 15):
  - Boxplot CV → `boxplot_accuracy.png` + `boxplot_f1.png`
  - Análise de erros → `erros_por_fonte.png` + `erros_heatmap.png`
- [x] Fixar posicionamento de figuras no LaTeX (`[H]` com pacote `float`) (Dia 15)
- [x] Compilar PDF — 14 páginas, todas figuras no lugar correto (Dia 15)
- [ ] Escrever Conclusão + Trabalhos Futuros
- [ ] Escrever Resumo + Abstract

### Pendente — Semanas 4-6 (revisão + defesa)
- [ ] Enviar artigo para orientador e aplicar correções
- [ ] Limpar `requirements.txt` (tem libs do Colab que não são usadas)
- [ ] Montar slides da apresentação
- [ ] Ensaiar apresentação cronometrada
- [ ] Entrega final + defesa

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
> **Figuras do artigo (individuais):** `artigo/imagens/boxplot_accuracy.png`, `artigo/imagens/boxplot_f1.png`, `artigo/imagens/erros_por_fonte.png`, `artigo/imagens/erros_heatmap.png`
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
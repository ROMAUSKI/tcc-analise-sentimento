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

**Última atualização:** 08/04/2026
**Branch:** main

### O que já foi feito
- [x] Geração dos 9 datasets sintéticos (manualmente via interfaces web)
- [x] Refactor da estrutura de pastas do projeto
- [x] Notebook `01` completo — Setup Colab/Local, pipeline com NB, LR e SVM Linear
- [x] Notebook `02` completo — CV k=5/k=10, boxplots, curvas de aprendizado, análise de erros
- [x] Tabela consolidada `resultados/metricas_consolidadas.csv`
- [x] Refatoração dos notebooks + re-execução local
- [x] Leitura e anotação de 16 referências
- [x] Artigo LaTeX: primeira versão completa (Seções 1–6 + Resumo + Abstract)
- [x] Figuras do artigo individualizadas e posicionadas com `[H]`
- [x] PDF compilado (14 páginas)

### Pendente
- [ ] Revisão final do artigo (leitura corrida, ortografia, consistência)
- [ ] Enviar artigo para orientador e aplicar correções
- [ ] Montar slides da apresentação
- [ ] Ensaiar apresentação cronometrada
- [ ] Entrega final + defesa
- [ ] (Opcional) Teste com dados reais — validação externa

---

## Resultados dos Modelos Baseline (Notebook 01 — split 80/20, seed=42)

| Modelo | Acurácia (%) | Precisão (%) | Recall (%) | F1-Score (%) |
|---|---|---|---|---|
| Naive Bayes | 86,11 | 86,19 | 86,11 | 86,13 |
| SVM Linear | 86,11 | 86,21 | 86,11 | 86,09 |
| Regressão Logística | 83,61 | 83,80 | 83,61 | 83,54 |

## Resultados da Validação Cruzada (Notebook 02)

| Modelo | k | Acurácia Média (%) | F1 Média (%) |
|---|---|---|---|
| Naive Bayes | 5 | 88,82 ±1,83 | 88,86 ±1,82 |
| Naive Bayes | 10 | 89,60 ±2,16 | 89,63 ±2,15 |
| Reg. Logística | 5 | 87,32 ±1,43 | 87,31 ±1,42 |
| Reg. Logística | 10 | 88,04 ±2,42 | 88,02 ±2,44 |
| SVM Linear | 5 | 88,88 ±1,33 | 88,88 ±1,33 |
| SVM Linear | 10 | 89,10 ±2,49 | 89,10 ±2,51 |

## Resultados da Análise de Erros (Notebook 02)

- **Total de erros:** 50/360 (13,9%) no Naive Bayes
- **Confusão mais frequente:** Negativa ↔ Positiva (24 erros — 13 Neg→Pos + 11 Pos→Neg)
- **Erros por fonte:** ChatGPT 9,9% | Claude 14,1% | Gemini 17,4%
- **Padrão:** Gemini gera frases mais descritivas e ambíguas; ChatGPT é mais direto e explícito no sentimento

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
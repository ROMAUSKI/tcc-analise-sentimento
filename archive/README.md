# archive/

Arquivos que saíram do escopo principal do TCC, mantidos para referência histórica.
**Não são executados pelo pipeline atual.** Não apagar sem revisão.

> **Última limpeza:** 2026-05-09 (Etapa D do plano de padronização).

---

## notebooks/

- **`03_real_data_validation.ipynb`** — primeira tentativa de validação cross-domain
  (V3 isolado, treino sintético + teste real). Substituído pelo `src/03_movies_3_visoes.ipynb`
  consolidado, que executa as 5 visões num único pipeline.

- **`04_comparativo_3_visoes.ipynb`** — protótipo do comparativo das 3 visões originais
  (V1/V2/V3 com 200/classe). Sua lógica foi absorvida e expandida no
  `src/03_movies_3_visoes.ipynb` atual (que tem 5 visões + F1 macro).

- **`07_redes_neurais_comparativo.ipynb`** — experimento exploratório com MLP e LSTM (PyTorch)
  feito antes da orientação formal sobre LSTM/BERT. Substituído pelo
  `src/04_movies_avancado.ipynb` (estrutura limpa, BERT/Bertimbau, replica V1..V5).

## scripts/

- **`_update_charts.py`** — script de manutenção criado durante a Etapa B para atualizar
  os gráficos do notebook 03 com as 4 métricas individuais. Lógica integrada à célula final
  do próprio notebook 03 — script externo virou redundante.

- **`analise_3_visoes.py`** — protótipo standalone do `04_comparativo_3_visoes` (também arquivado).
  Reproduz lógica que vive nos notebooks atuais.

- **`reprocessar_dataset.py`** — rascunho do processo de unificação que vive no notebook
  `01_movies_training`. Replica trabalho já feito.

## artigo/

- **`main_v1.tex` / `main_v1.pdf`** — versão do artigo enviada ao orientador antes da rodada
  de revisão de 2026-05 (pré-3-visões / pré-segundo-nicho). Versão ativa: `artigo/main.tex`.

- **`artigo_compilado.pdf`** — PDF compilado do artigo, versão de 2026-04-29 (estado anterior
  à introdução das 5 visões e da V4/V5 desbalanceadas).

- **`artigo_TCC.pdf`** — outra versão PDF do artigo, mesma data. Provavelmente a entregue ao orientador.

> Versões PDF mantidas como histórico de submissões. Versão ativa é sempre o que `artigo/main.tex` compila hoje.

## resultados/

Resultados que pertencem aos notebooks já arquivados ou foram substituídos por versões mais completas:

- **`grafico_redes_neurais.png`** + **`metricas_redes_neurais.csv`** — saídas do
  `07_redes_neurais_comparativo.ipynb` (notebook arquivado). Contêm MLP + LSTM com
  configurações exploratórias que NÃO seguem a metodologia atual de 5 visões.

- **`analise_3_visoes_movies.csv`** — métricas das 3 visões originais (V1/V2/V3 com 200/classe).
  Substituído por `resultados/metricas_5_visoes_movies.csv` (5 visões + F1 macro).

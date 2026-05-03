# archive/

Arquivos que saíram do escopo principal do TCC, mantidos para referência histórica.
**Não são executados pelo pipeline atual.** Não apagar sem revisão.

## notebooks/

- **`07_redes_neurais_comparativo.ipynb`** — experimento exploratório com MLP e LSTM (PyTorch).
  Fora do escopo: o orientador focou o TCC em validar a qualidade dos dados sintéticos
  via cross-domain (V1/V2/V3), não em comparar arquiteturas de modelo.
  Resultado registrado: redes neurais não resolveram o reality gap (V3 ≈ 35-39% F1,
  similar aos modelos clássicos). Pode virar trabalho futuro.

## scripts/

- **`analise_3_visoes.py`** — protótipo standalone do notebook `04_comparativo_3_visoes`
  (hoje consolidado em `src/03_movies_3_visoes.ipynb`). Lógica já está nos notebooks.
- **`reprocessar_dataset.py`** — rascunho do processo de unificação que vive no notebook
  `01_movies_training`. Replica trabalho já feito.

## artigo/

- **`main_v1.tex` / `main_v1.pdf`** — versão do artigo enviada ao orientador antes desta
  rodada de revisão (pré-3-visões / pré-segundo-nicho). Mantido como histórico do que
  foi entregue. A versão ativa é `artigo/main.tex`.

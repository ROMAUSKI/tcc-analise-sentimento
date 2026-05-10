# -*- coding: utf-8 -*-
"""Corrige paths relativos do notebook 01 + adiciona import glob no setup."""
import nbformat as nbf
import io
import re

nb_path = 'src/01_movies_training.ipynb'
with io.open(nb_path, 'r', encoding='utf-8') as f:
    nb = nbf.read(f, as_version=4)

# 1) Adiciona import glob na célula de setup (célula 0)
setup = nb.cells[0].source
if 'import glob' not in setup:
    nb.cells[0].source = setup.replace(
        'import os, sys',
        'import os, sys, glob'
    )
    print('OK: glob adicionado ao setup')

# 2) Substituições nos paths relativos
substituicoes = [
    # Cell 3 — unificação dos CSVs brutos
    ("arquivos_csv = glob.glob('*.csv')",
     "arquivos_csv = glob.glob(os.path.join(DADOS_BRUTOS_MOVIES, '*.csv'))"),
    ("for arq_ignorar in ['metadata.csv', 'dataset_completo.csv', 'synthetic_dataset.csv']:\n        if arq_ignorar in arquivos_csv:\n            arquivos_csv.remove(arq_ignorar)",
     "ignorar = ['metadata.csv', 'dataset_completo.csv', 'synthetic_dataset.csv']\n    arquivos_csv = [f for f in arquivos_csv if os.path.basename(f) not in ignorar]"),
    ("df_final.to_csv('../processado/dataset_completo.csv', index=False)",
     "df_final.to_csv(os.path.join(DADOS_PROCESSADO, 'dataset_completo.csv'), index=False)"),
    # Cell 4 — pré-processamento (limpeza)
    ("df = pd.read_csv('../processado/dataset_completo.csv')",
     "df = pd.read_csv(os.path.join(DADOS_PROCESSADO, 'dataset_completo.csv'))"),
    ("df_final_limpo.to_csv('../processado/synthetic_dataset.csv', index=False)",
     "df_final_limpo.to_csv(os.path.join(DADOS_PROCESSADO, 'synthetic_dataset.csv'), index=False)"),
    # Cells 5, 6 — análise estatística e baseline
    ("df = pd.read_csv('../processado/synthetic_dataset.csv')",
     "df = pd.read_csv(os.path.join(DADOS_PROCESSADO, 'synthetic_dataset.csv'))"),
    # Cells 5, 7, 8, 9 — pasta_resultados
    ('pasta_resultados = "../../resultados/"',
     'pasta_resultados = RESULTADOS + os.sep'),
    # Cells 10, 11 — baseline_metrics.csv
    ('caminho_arquivo = "../../resultados/baseline_metrics.csv"',
     "caminho_arquivo = os.path.join(RESULTADOS, 'baseline_metrics.csv')"),
    ('df_resultados.to_csv("../../resultados/baseline_metrics.csv")',
     "df_resultados.to_csv(os.path.join(RESULTADOS, 'baseline_metrics.csv'))"),
]

n_subs_total = 0
for i, c in enumerate(nb.cells):
    if c.cell_type != 'code':
        continue
    src = c.source
    for old, new in substituicoes:
        if old in src:
            src = src.replace(old, new)
            n_subs_total += 1
            print(f'  cell {i:2d}: substituido "{old[:50]}..."')
    nb.cells[i].source = src

print(f'\nTotal de substituicoes aplicadas: {n_subs_total}')

with io.open(nb_path, 'w', encoding='utf-8') as f:
    nbf.write(nb, f)
print(f'Notebook salvo: {nb_path}')

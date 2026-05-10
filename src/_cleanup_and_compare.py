# -*- coding: utf-8 -*-
"""
1) Remove código de alias (_3_visoes_*) do notebook 03
2) Deleta os 3 arquivos duplicados
3) Gera tabela + gráfico comparativo 200/cl vs 600/cl
"""
import nbformat as nbf
import io, os
import pandas as pd
import matplotlib.pyplot as plt

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
RESULTADOS = os.path.join(ROOT, 'resultados')

# ============================================================
# 1) Editar notebook 03: remover linhas que salvam com alias _3_visoes_
# ============================================================
nb_path = os.path.join(ROOT, 'src', '03_movies_3_visoes.ipynb')
with io.open(nb_path, 'r', encoding='utf-8') as f:
    nb = nbf.read(f, as_version=4)

linhas_remover = [
    "# Mantém também o nome antigo para compatibilidade\n"
    "df_resultados.round(4).to_csv(os.path.join(RESULTADOS, 'metricas_3_visoes_movies.csv'), index=False)\n",
    "plt.savefig(os.path.join(RESULTADOS, 'grafico_3_visoes_movies.png'), dpi=150, bbox_inches='tight')  # compat\n",
    "plt.savefig(os.path.join(RESULTADOS, 'grafico_3_visoes_movies_4metricas.png'), dpi=150, bbox_inches='tight')  # compat\n",
]

# Procura na célula final (resultado) e remove
for i, c in enumerate(nb.cells):
    if c.cell_type != 'code':
        continue
    src = c.source
    mudou = False
    # Variação 1: bloco completo de comentário + to_csv
    bloco_csv = (
        "# Mantém também o nome antigo para compatibilidade\n"
        "df_resultados.round(4).to_csv(os.path.join(RESULTADOS, 'metricas_3_visoes_movies.csv'), index=False)\n"
    )
    if bloco_csv in src:
        src = src.replace(bloco_csv, '')
        mudou = True
    # Variação 2: savefig com alias compat
    for trecho in [
        "plt.savefig(os.path.join(RESULTADOS, 'grafico_3_visoes_movies.png'), dpi=150, bbox_inches='tight')  # compat\n",
        "plt.savefig(os.path.join(RESULTADOS, 'grafico_3_visoes_movies_4metricas.png'), dpi=150, bbox_inches='tight')  # compat\n",
    ]:
        if trecho in src:
            src = src.replace(trecho, '')
            mudou = True
    if mudou:
        nb.cells[i].source = src
        print(f'  Cell {i}: linhas de alias removidas')

with io.open(nb_path, 'w', encoding='utf-8') as f:
    nbf.write(nb, f)
print('Notebook 03 limpo (sem aliases).')

# ============================================================
# 2) Deletar arquivos duplicados
# ============================================================
duplicados = [
    'grafico_3_visoes_movies.png',
    'grafico_3_visoes_movies_4metricas.png',
    'metricas_3_visoes_movies.csv',
]
for f in duplicados:
    fp = os.path.join(RESULTADOS, f)
    if os.path.exists(fp):
        os.remove(fp)
        print(f'  Deletado: resultados/{f}')

# ============================================================
# 3) Tabela comparativa 200/cl vs 600/cl
# ============================================================
# Métricas antigas (200/cl) — tiradas do commit 7c2b204
DADOS_ANTIGOS = [
    ('V1: Sintético → Sintético', 'Naive Bayes', 0.8417, 0.8409, 0.8409),
    ('V1: Sintético → Sintético', 'Regressão Logística', 0.8000, 0.7978, 0.7978),
    ('V1: Sintético → Sintético', 'SVM Linear', 0.8083, 0.8081, 0.8081),
    ('V2: Real → Real', 'Naive Bayes', 0.4417, 0.4320, 0.4320),
    ('V2: Real → Real', 'Regressão Logística', 0.4333, 0.4123, 0.4123),
    ('V2: Real → Real', 'SVM Linear', 0.4500, 0.4241, 0.4241),
    ('V3: Sintético → Real', 'Naive Bayes', 0.4000, 0.3838, 0.3838),
    ('V3: Sintético → Real', 'Regressão Logística', 0.3500, 0.3459, 0.3459),
    ('V3: Sintético → Real', 'SVM Linear', 0.3583, 0.3543, 0.3543),
    ('V4: Real → Real (desbalanceado)', 'Naive Bayes', 0.7271, 0.6436, 0.3848),
    ('V4: Real → Real (desbalanceado)', 'Regressão Logística', 0.7472, 0.7093, 0.5205),
    ('V4: Real → Real (desbalanceado)', 'SVM Linear', 0.7440, 0.7059, 0.5192),
    ('V5: Sintético → Real (desbalanceado)', 'Naive Bayes', 0.4493, 0.4962, 0.3365),
    ('V5: Sintético → Real (desbalanceado)', 'Regressão Logística', 0.4201, 0.4728, 0.3342),
    ('V5: Sintético → Real (desbalanceado)', 'SVM Linear', 0.4209, 0.4735, 0.3388),
]
df_antigo = pd.DataFrame(DADOS_ANTIGOS, columns=['Visão', 'Modelo', 'Acurácia', 'F1-Score', 'F1-Macro'])
df_antigo['Volume'] = '200/classe (600 total)'

# Métricas novas (600/cl) — do CSV atual
df_novo_csv = pd.read_csv(os.path.join(RESULTADOS, 'metricas_5_visoes_movies.csv'))
df_novo = df_novo_csv[['Visão', 'Modelo', 'Acurácia', 'F1-Score', 'F1-Macro']].copy()
df_novo['Volume'] = '600/classe (1800 total — sintético inteiro)'

df_comp = pd.concat([df_antigo, df_novo], ignore_index=True)
csv_path = os.path.join(RESULTADOS, 'comparativo_200_vs_600_movies.csv')
df_comp.round(4).to_csv(csv_path, index=False)
print(f'\nCSV comparativo salvo: {csv_path}')

# Gráfico: F1-Score × visão × volume (focando em V1, V2, V3 que são os afetados)
ordem_visoes = [
    'V1: Sintético → Sintético', 'V2: Real → Real', 'V3: Sintético → Real',
    'V4: Real → Real (desbalanceado)', 'V5: Sintético → Real (desbalanceado)'
]
ordem_modelos = ['Naive Bayes', 'Regressão Logística', 'SVM Linear']

# Pivota: linhas = (Visão, Modelo), colunas = Volume, valor = F1-Score
df_pivot = df_comp.pivot_table(
    index=['Visão', 'Modelo'], columns='Volume', values='F1-Score'
)
df_pivot = df_pivot.reindex(
    [(v, m) for v in ordem_visoes for m in ordem_modelos]
)

# Gráfico de barras agrupadas (200 vs 600), 1 par por (visão, modelo)
fig, axes = plt.subplots(1, 5, figsize=(22, 6), sharey=True)
for k, visao in enumerate(ordem_visoes):
    sub = df_pivot.xs(visao, level='Visão')
    sub = sub[['200/classe (600 total)', '600/classe (1800 total — sintético inteiro)']]
    sub.plot(kind='bar', ax=axes[k], rot=15, edgecolor='black',
             color=['#888888', '#1f77b4'], width=0.75, legend=(k == 0))
    axes[k].set_title(visao.split(':')[0] + '\n' + visao.split(': ')[1], fontsize=10)
    axes[k].set_xlabel('')
    axes[k].set_ylim(0, 1.0)
    axes[k].grid(axis='y', alpha=0.3)
    for container in axes[k].containers:
        axes[k].bar_label(container, fmt='%.2f', padding=2, fontsize=7)
    if k == 0:
        axes[k].legend(title='Volume sintético', loc='upper left', fontsize=8)
        axes[k].set_ylabel('F1-Score (weighted)', fontsize=11)
fig.suptitle(
    'Reality gap é estrutural — triplicar volume sintético NÃO melhora V3 (cross-domain)',
    fontsize=13, fontweight='bold', y=1.02
)
plt.tight_layout()
png_path = os.path.join(RESULTADOS, 'comparativo_200_vs_600_movies.png')
plt.savefig(png_path, dpi=150, bbox_inches='tight')
plt.close()
print(f'Gráfico comparativo salvo: {png_path}')

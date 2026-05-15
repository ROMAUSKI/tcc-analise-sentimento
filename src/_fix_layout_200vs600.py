# -*- coding: utf-8 -*-
"""Regenera comparativo_200_vs_600_movies.png em layout 2x3 (era 1x5)."""
import os
import pandas as pd
import matplotlib.pyplot as plt

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
RESULTADOS = os.path.join(ROOT, 'resultados')
ARTIGO_IMG = os.path.join(ROOT, 'artigo', 'imagens')

df = pd.read_csv(os.path.join(RESULTADOS, 'comparativo_200_vs_600_movies.csv'))

ordem_visoes = [
    'V1: Sintético → Sintético',
    'V2: Real → Real',
    'V3: Sintético → Real',
    'V4: Real → Real (desbalanceado)',
    'V5: Sintético → Real (desbalanceado)',
]
ordem_modelos = ['Naive Bayes', 'Regressão Logística', 'SVM Linear']
volumes = ['200/classe (600 total)', '600/classe (1800 total — sintético inteiro)']

# Layout 2×3
fig, axes = plt.subplots(2, 3, figsize=(15, 9), sharey=True)
axes = axes.flatten()

for k, visao in enumerate(ordem_visoes):
    ax = axes[k]
    sub = df[df['Visão'] == visao]
    pivot = sub.pivot_table(index='Modelo', columns='Volume', values='F1-Score')
    pivot = pivot.reindex(ordem_modelos)
    pivot = pivot[volumes]

    pivot.plot(kind='bar', ax=ax, rot=15, edgecolor='black',
               color=['#888888', '#1f77b4'], width=0.75, legend=(k == 0))
    ax.set_title(visao.split(':')[0] + ': ' + visao.split(': ')[1], fontsize=11, fontweight='bold')
    ax.set_xlabel('')
    ax.set_ylim(0, 1.0)
    ax.grid(axis='y', alpha=0.3)
    for container in ax.containers:
        ax.bar_label(container, fmt='%.2f', padding=2, fontsize=8)
    if k == 0:
        ax.legend(title='Volume sintético', loc='upper left', fontsize=9)
    if k % 3 == 0:
        ax.set_ylabel('F1-Score (weighted)', fontsize=11)

# Esconde 6º painel
axes[5].set_visible(False)

fig.suptitle('Comparação 200 vs 600 frases sintéticas por classe — Movies\n(volume não fecha o gap em V3)',
             fontsize=13, fontweight='bold', y=1.00)
plt.tight_layout()

out1 = os.path.join(RESULTADOS, 'comparativo_200_vs_600_movies.png')
out2 = os.path.join(ARTIGO_IMG, 'comparativo_200_vs_600_movies.png')
plt.savefig(out1, dpi=150, bbox_inches='tight')
plt.savefig(out2, dpi=150, bbox_inches='tight')
plt.close()

print(f'OK — salvo em {out1} e {out2}')

# -*- coding: utf-8 -*-
"""
Etapa G.1 — Gera os 3 gráficos comparativos Movies × Apps faltantes:
- comparativo_nichos_acuracia.png
- comparativo_nichos_precisao.png
- comparativo_nichos_recall.png

Mesmo padrão dos 2 que já existem (f1weighted e f1macro).
"""
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
RESULTADOS = os.path.join(ROOT, 'resultados')

print('=== ETAPA G.1 — gráficos comparativos faltantes ===\n')

df_geral = pd.read_csv(os.path.join(RESULTADOS, 'metricas_consolidado_geral.csv'))

ordem_visoes = [
    'V1: Sintético → Sintético',
    'V2: Real → Real',
    'V3: Sintético → Real',
    'V4: Real → Real (desbalanceado)',
    'V5: Sintético → Real (desbalanceado)',
]
ordem_modelos = ['Naive Bayes', 'Regressão Logística', 'SVM Linear', 'LSTM', 'BERT (Bertimbau)']

# Gera os 3 que faltam
for metrica, nome_arq, titulo_metrica in [
    ('Acurácia', 'comparativo_nichos_acuracia.png', 'Acurácia'),
    ('Precisão', 'comparativo_nichos_precisao.png', 'Precisão (weighted)'),
    ('Recall',   'comparativo_nichos_recall.png',   'Recall (weighted)'),
]:
    fig, axes = plt.subplots(1, 5, figsize=(28, 6), sharey=True)
    largura = 0.35
    x = np.arange(len(ordem_modelos))

    for k, visao in enumerate(ordem_visoes):
        ax = axes[k]
        movies_vals = []
        apps_vals = []
        for modelo in ordem_modelos:
            row_m = df_geral[(df_geral['Nicho'] == 'Movies') & (df_geral['Visão'] == visao) & (df_geral['Modelo'] == modelo)]
            row_a = df_geral[(df_geral['Nicho'] == 'Apps')   & (df_geral['Visão'] == visao) & (df_geral['Modelo'] == modelo)]
            movies_vals.append(row_m[metrica].values[0] if len(row_m) else 0)
            apps_vals.append(row_a[metrica].values[0] if len(row_a) else 0)

        b1 = ax.bar(x - largura/2, movies_vals, largura, label='Movies', color='#3498db', edgecolor='black')
        b2 = ax.bar(x + largura/2, apps_vals,   largura, label='Apps',   color='#e67e22', edgecolor='black')

        ax.set_title(visao.split(':')[0] + '\n' + visao.split(': ')[1], fontsize=10)
        ax.set_xticks(x)
        ax.set_xticklabels([m.replace(' (Bertimbau)', '') for m in ordem_modelos], rotation=30, ha='right', fontsize=8)
        ax.set_ylim(0, 1.0)
        ax.grid(axis='y', alpha=0.3)
        for bars in [b1, b2]:
            for bar in bars:
                ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01,
                        f'{bar.get_height():.2f}', ha='center', fontsize=7)
        if k == 0:
            ax.legend(loc='upper left', fontsize=9)
            ax.set_ylabel(titulo_metrica, fontsize=11)

    fig.suptitle(f'Comparativo entre nichos — Movies × Apps ({titulo_metrica})',
                 fontsize=14, fontweight='bold', y=1.02)
    plt.tight_layout()
    out = os.path.join(RESULTADOS, nome_arq)
    plt.savefig(out, dpi=150, bbox_inches='tight')
    plt.close()
    print(f'  ✓ Salvo: {out}')

print('\nFinalizado. Total agora: 5 gráficos comparativos (1 por métrica).')

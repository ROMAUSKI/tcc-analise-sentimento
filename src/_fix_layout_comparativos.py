# -*- coding: utf-8 -*-
"""
Regenera os 5 gráficos comparativos Movies × Apps com layout 2×3
(em vez de 1×5 horizontal). Mais legível em página A4 portrait.

Layout: 2 linhas × 3 colunas:
  V1   V2   V3
  V4   V5  (vazio)
"""
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
RESULTADOS = os.path.join(ROOT, 'resultados')
ARTIGO_IMG = os.path.join(ROOT, 'artigo', 'imagens')

print('=== Regenerando comparativos com layout 2x3 ===\n')

df_geral = pd.read_csv(os.path.join(RESULTADOS, 'metricas_consolidado_geral.csv'))

ordem_visoes = [
    'V1: Sintético → Sintético',
    'V2: Real → Real',
    'V3: Sintético → Real',
    'V4: Real → Real (desbalanceado)',
    'V5: Sintético → Real (desbalanceado)',
]
ordem_modelos = ['Naive Bayes', 'Regressão Logística', 'SVM Linear', 'LSTM', 'BERT (Bertimbau)']

for metrica, nome_arq, titulo_metrica in [
    ('Acurácia', 'comparativo_nichos_acuracia.png', 'Acurácia'),
    ('Precisão', 'comparativo_nichos_precisao.png', 'Precisão (weighted)'),
    ('Recall',   'comparativo_nichos_recall.png',   'Recall (weighted)'),
    ('F1-Score', 'comparativo_nichos_f1weighted.png', 'F1-Score (weighted)'),
    ('F1-Macro', 'comparativo_nichos_f1macro.png', 'F1-Score (macro)'),
]:
    # Layout 2×3
    fig, axes = plt.subplots(2, 3, figsize=(15, 9), sharey=True)
    axes = axes.flatten()
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

        ax.set_title(visao.split(':')[0] + ': ' + visao.split(': ')[1], fontsize=11, fontweight='bold')
        ax.set_xticks(x)
        ax.set_xticklabels([m.replace(' (Bertimbau)', '') for m in ordem_modelos], rotation=20, ha='right', fontsize=9)
        ax.set_ylim(0, 1.0)
        ax.grid(axis='y', alpha=0.3)
        for bars in [b1, b2]:
            for bar in bars:
                ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01,
                        f'{bar.get_height():.2f}', ha='center', fontsize=8)
        if k == 0:
            ax.legend(loc='upper left', fontsize=10)
        if k % 3 == 0:
            ax.set_ylabel(titulo_metrica, fontsize=11)

    # Esconde o 6º painel (vazio)
    axes[5].set_visible(False)

    fig.suptitle(f'Comparativo Movies × Apps — {titulo_metrica}',
                 fontsize=14, fontweight='bold', y=1.00)
    plt.tight_layout()

    # Salva nos dois lugares
    out1 = os.path.join(RESULTADOS, nome_arq)
    out2 = os.path.join(ARTIGO_IMG, nome_arq)
    plt.savefig(out1, dpi=150, bbox_inches='tight')
    plt.savefig(out2, dpi=150, bbox_inches='tight')
    plt.close()
    print(f'  ✓ {nome_arq}')

print('\nTodos os 5 gráficos regenerados em layout 2x3.')
print('Salvos em resultados/ e artigo/imagens/.')

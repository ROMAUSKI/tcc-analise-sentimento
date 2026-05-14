# -*- coding: utf-8 -*-
"""
Etapa F — Comparativo entre nichos (Movies vs Apps).

Gera 3 grupos de artefatos:
1. Tabela única consolidada (Movies + Apps) em CSV
2. Gráfico unificado lado a lado (Apps × Movies) por visão e modelo
3. Análise de comprimento de frases por LLM gerador (sintético) e por nicho
"""
import os, io
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
RESULTADOS = os.path.join(ROOT, 'resultados')
DADOS_PROCESSADO = os.path.join(ROOT, 'dados', 'processado')

print('=== ETAPA F — COMPARATIVO ENTRE NICHOS ===\n')

# ============================================================
# 1) Tabela única consolidada (Movies + Apps)
# ============================================================
print('[1/3] Tabela única consolidada (Movies + Apps)...')
df_movies = pd.read_csv(os.path.join(RESULTADOS, 'metricas_consolidado_movies.csv'))
df_apps   = pd.read_csv(os.path.join(RESULTADOS, 'metricas_consolidado_apps.csv'))
df_movies['Nicho'] = 'Movies'
df_apps['Nicho']   = 'Apps'

df_geral = pd.concat([df_movies, df_apps], ignore_index=True)
# Reordena colunas: Nicho primeiro
cols = ['Nicho'] + [c for c in df_geral.columns if c != 'Nicho']
df_geral = df_geral[cols]
out_csv = os.path.join(RESULTADOS, 'metricas_consolidado_geral.csv')
df_geral.round(4).to_csv(out_csv, index=False)
print(f'  ✓ Salvo: {out_csv} ({len(df_geral)} linhas)')

# ============================================================
# 2) Gráficos comparativos Movies × Apps lado a lado
# ============================================================
print('\n[2/3] Gráfico comparativo Movies × Apps...')

ordem_visoes = [
    'V1: Sintético → Sintético',
    'V2: Real → Real',
    'V3: Sintético → Real',
    'V4: Real → Real (desbalanceado)',
    'V5: Sintético → Real (desbalanceado)',
]
ordem_modelos = ['Naive Bayes', 'Regressão Logística', 'SVM Linear', 'LSTM', 'BERT (Bertimbau)']

for metrica, nome_arq, titulo_metrica in [
    ('F1-Score', 'comparativo_nichos_f1weighted.png', 'F1-Score (weighted)'),
    ('F1-Macro', 'comparativo_nichos_f1macro.png', 'F1-Score (macro)'),
]:
    fig, axes = plt.subplots(1, 5, figsize=(28, 6), sharey=True)
    largura = 0.35
    x = np.arange(len(ordem_modelos))

    for k, visao in enumerate(ordem_visoes):
        ax = axes[k]
        # Pega valores Movies e Apps
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

# ============================================================
# 3) Análise de comprimento de frases por LLM gerador
# ============================================================
print('\n[3/3] Análise de comprimento de frases por LLM e nicho...')

df_sint_movies = pd.read_csv(os.path.join(DADOS_PROCESSADO, 'synthetic_dataset.csv'))
df_sint_apps   = pd.read_csv(os.path.join(DADOS_PROCESSADO, 'synthetic_dataset_apps.csv'))
df_sint_movies['Nicho'] = 'Movies'
df_sint_apps['Nicho']   = 'Apps'

df_sint = pd.concat([df_sint_movies, df_sint_apps], ignore_index=True)
df_sint = df_sint.dropna(subset=['frase_limpa'])
df_sint['n_chars']    = df_sint['frase_limpa'].str.len()
df_sint['n_palavras'] = df_sint['frase_limpa'].str.split().str.len()

# Tabela resumo
resumo = df_sint.groupby(['Nicho', 'fonte']).agg(
    n_frases   = ('frase_limpa', 'count'),
    chars_med  = ('n_chars',    'mean'),
    chars_med2 = ('n_chars',    'median'),
    chars_std  = ('n_chars',    'std'),
    palav_med  = ('n_palavras', 'mean'),
    palav_med2 = ('n_palavras', 'median'),
    palav_std  = ('n_palavras', 'std'),
).round(1).reset_index()
resumo.columns = ['Nicho', 'Fonte (LLM)', 'N frases', 'Chars média', 'Chars mediana', 'Chars desvio',
                  'Palavras média', 'Palavras mediana', 'Palavras desvio']
out_csv2 = os.path.join(RESULTADOS, 'comprimento_frases_por_llm.csv')
resumo.to_csv(out_csv2, index=False)
print(f'  ✓ Salvo: {out_csv2}')
print(resumo.to_string(index=False))

# Gráfico boxplot: comprimento (chars) por LLM × nicho
fig, axes = plt.subplots(1, 2, figsize=(14, 6), sharey=True)
ordem_llms = ['ChatGPT', 'Claude', 'Gemini']
cores_llm = {'ChatGPT': '#10a37f', 'Claude': '#cc785c', 'Gemini': '#4285f4'}

for ax, nicho in zip(axes, ['Movies', 'Apps']):
    dados_box = [df_sint[(df_sint['Nicho'] == nicho) & (df_sint['fonte'] == llm)]['n_chars'].values
                 for llm in ordem_llms]
    bp = ax.boxplot(dados_box, labels=ordem_llms, patch_artist=True, widths=0.6)
    for patch, llm in zip(bp['boxes'], ordem_llms):
        patch.set_facecolor(cores_llm[llm])
        patch.set_alpha(0.7)
    # Anotar média
    for i, dados in enumerate(dados_box, start=1):
        media = np.mean(dados)
        ax.text(i, ax.get_ylim()[1]*0.95, f'média:\n{media:.0f}', ha='center', fontsize=9, fontweight='bold')
    ax.set_title(f'Nicho: {nicho}', fontsize=12, fontweight='bold')
    ax.set_ylabel('Comprimento (caracteres)' if nicho == 'Movies' else '')
    ax.grid(axis='y', alpha=0.3)

fig.suptitle('Comprimento das frases sintéticas por LLM gerador',
             fontsize=13, fontweight='bold', y=1.02)
plt.tight_layout()
out_png = os.path.join(RESULTADOS, 'comprimento_frases_por_llm.png')
plt.savefig(out_png, dpi=150, bbox_inches='tight')
plt.close()
print(f'  ✓ Salvo: {out_png}')

print('\n=== ETAPA F CONCLUÍDA ===')
print(f'\nArquivos gerados em {RESULTADOS}:')
print('  - metricas_consolidado_geral.csv  (Movies + Apps consolidado)')
print('  - comparativo_nichos_f1weighted.png  (5 painéis × Movies vs Apps)')
print('  - comparativo_nichos_f1macro.png  (idem com F1 macro)')
print('  - comprimento_frases_por_llm.csv  (tabela média/mediana/desvio)')
print('  - comprimento_frases_por_llm.png  (boxplot por LLM × nicho)')

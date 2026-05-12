# -*- coding: utf-8 -*-
"""
Clona notebooks 01-04 de Movies para 05-08 de Apps adaptando todas as referências.

Substituições aplicadas:
- Paths: dados/brutos/ → dados/brutos_apps/
- Variáveis: DADOS_BRUTOS_MOVIES → DADOS_BRUTOS_APPS
- Datasets: synthetic_dataset.csv → synthetic_dataset_apps.csv
            dataset_completo.csv → dataset_completo_apps.csv
            utlc_movies.csv → utlc_apps.csv
- Resultados: todos os arquivos *.csv e *.png ganham sufixo _apps
  para não sobrescrever os de Movies
- Texto: Movies → Apps, filmes e séries → aplicativos móveis, etc.
"""
import nbformat as nbf
import io, os, re

# Mapeamento dos clones
CLONES = [
    ('src/01_movies_training.ipynb',    'src/05_apps_training.ipynb'),
    ('src/02_movies_robustness.ipynb',  'src/06_apps_robustness.ipynb'),
    ('src/03_movies_3_visoes.ipynb',    'src/07_apps_3_visoes.ipynb'),
    ('src/04_movies_avancado.ipynb',    'src/08_apps_avancado.ipynb'),
]

# Substituições (ordem importa: faz as mais específicas primeiro)
SUBSTITUICOES = [
    # Paths e arquivos de entrada
    ('DADOS_BRUTOS_MOVIES', 'DADOS_BRUTOS_APPS'),
    ('synthetic_dataset.csv', 'synthetic_dataset_apps.csv'),
    ('dataset_completo.csv', 'dataset_completo_apps.csv'),
    ('utlc_movies.csv', 'utlc_apps.csv'),
    # Arquivos de saída — adiciona _apps aos nomes dos resultados
    ('metricas_5_visoes_movies', 'metricas_5_visoes_apps'),
    ('grafico_5_visoes_movies', 'grafico_5_visoes_apps'),
    ('metricas_avancado_movies', 'metricas_avancado_apps'),
    ('metricas_consolidado_movies', 'metricas_consolidado_apps'),
    ('grafico_consolidado_movies', 'grafico_consolidado_apps'),
    # Notebook 02 specific - adicionar sufixo _apps
    ("'baseline_metrics.csv'", "'baseline_metrics_apps.csv'"),
    ("'validacao_cruzada.csv'", "'validacao_cruzada_apps.csv'"),
    ("'metricas_consolidadas.csv'", "'metricas_consolidadas_apps.csv'"),
    ("'analise_erros.csv'", "'analise_erros_apps.csv'"),
    ("'analise_erros_graficos.png'", "'analise_erros_graficos_apps.png'"),
    ("'boxplot_accuracy.png'", "'boxplot_accuracy_apps.png'"),
    ("'boxplot_f1.png'", "'boxplot_f1_apps.png'"),
    ("'boxplot_validacao_cruzada.png'", "'boxplot_validacao_cruzada_apps.png'"),
    ("'curva_aprendizado_lr.png'", "'curva_aprendizado_lr_apps.png'"),
    ("'curva_aprendizado_nb.png'", "'curva_aprendizado_nb_apps.png'"),
    ("'curva_aprendizado_svm.png'", "'curva_aprendizado_svm_apps.png'"),
    ("'distribuicao_classe_por_fonte.png'", "'distribuicao_classe_por_fonte_apps.png'"),
    ("'distribuicao_comprimento_frases.png'", "'distribuicao_comprimento_frases_apps.png'"),
    ("'erros_heatmap.png'", "'erros_heatmap_apps.png'"),
    ("'erros_por_fonte.png'", "'erros_por_fonte_apps.png'"),
    ("'f1_score_por_classe_lr.png'", "'f1_score_por_classe_lr_apps.png'"),
    ("'f1_score_por_classe_nb.png'", "'f1_score_por_classe_nb_apps.png'"),
    ("'f1_score_por_classe_svm.png'", "'f1_score_por_classe_svm_apps.png'"),
    ("'matriz_confusao_lr.png'", "'matriz_confusao_lr_apps.png'"),
    ("'matriz_confusao_nb.png'", "'matriz_confusao_nb_apps.png'"),
    ("'matriz_confusao_svm.png'", "'matriz_confusao_svm_apps.png'"),
    ("'violino_comprimento_por_fonte.png'", "'violino_comprimento_por_fonte_apps.png'"),
    # Aspas duplas também
    ('"baseline_metrics.csv"', '"baseline_metrics_apps.csv"'),
    ('"validacao_cruzada.csv"', '"validacao_cruzada_apps.csv"'),
    ('"metricas_consolidadas.csv"', '"metricas_consolidadas_apps.csv"'),
    # Pasta checkpoints (notebook 04 → 08)
    ('checkpoints_avancado', 'checkpoints_avancado_apps'),
    ('bert_v', 'bert_apps_v'),  # subpasta dos checkpoints
    # Texto descritivo
    ('UTLC-Movies', 'UTLC-Apps'),
    ('Nicho: Movies', 'Nicho: Apps'),
    ('Movies (UTLC-Apps)', 'Apps (UTLC-Apps)'),  # caso a substituição anterior tenha conflito
    ('Nicho de filmes', 'Nicho de aplicativos'),
    ('nicho de filmes', 'nicho de aplicativos'),
    ('filmes e séries', 'aplicativos móveis'),
    ('reviews de filmes', 'reviews de aplicativos'),
    ('utlc-movies', 'utlc-apps'),
    # Comentários e títulos
    ('· Movies', '· Apps'),
    ('— Movies', '— Apps'),
    ('movies_3_visoes', 'apps_3_visoes'),
    ('movies_avancado', 'apps_avancado'),
    ('movies_training', 'apps_training'),
    ('movies_robustness', 'apps_robustness'),
    # Markdown headers
    ('Notebook 01 — ', 'Notebook 05 — '),
    ('Notebook 02 — ', 'Notebook 06 — '),
    ('Notebook 03 — ', 'Notebook 07 — '),
    ('Notebook 04 — ', 'Notebook 08 — '),
]

print('=== Clonando notebooks Movies → Apps ===\n')

for src_nb, dst_nb in CLONES:
    print(f'[{os.path.basename(src_nb)}] → [{os.path.basename(dst_nb)}]')

    with io.open(src_nb, 'r', encoding='utf-8') as f:
        nb = nbf.read(f, as_version=4)

    n_subs_total = 0
    for i, c in enumerate(nb.cells):
        src = c.source
        n_subs_celula = 0
        for old, new in SUBSTITUICOES:
            count = src.count(old)
            if count > 0:
                src = src.replace(old, new)
                n_subs_celula += count
        if n_subs_celula > 0:
            nb.cells[i].source = src
            n_subs_total += n_subs_celula

    with io.open(dst_nb, 'w', encoding='utf-8') as f:
        nbf.write(nb, f)

    print(f'  {n_subs_total} substituições | {len(nb.cells)} células\n')

print('=== Validando sintaxe ===')
import ast
for _, dst_nb in CLONES:
    with io.open(dst_nb, 'r', encoding='utf-8') as f:
        nb = nbf.read(f, as_version=4)
    ok = True
    for i, c in enumerate(nb.cells):
        if c.cell_type != 'code': continue
        # Filtra magic commands
        src_clean = '\n'.join(l for l in c.source.split('\n')
                              if not l.strip().startswith('!') and not l.strip().startswith('%'))
        try:
            ast.parse(src_clean)
        except SyntaxError as e:
            ok = False
            print(f'  {os.path.basename(dst_nb)} cell {i}: linha {e.lineno}: {e.msg}')
    print(f'  {os.path.basename(dst_nb)}: {"OK" if ok else "ERROS"}')

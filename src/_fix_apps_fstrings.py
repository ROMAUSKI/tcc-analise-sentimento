# -*- coding: utf-8 -*-
"""Corrige f-strings em notebooks Apps que ficaram sem sufixo _apps."""
import nbformat as nbf
import io, re, os

# Lista de nomes de arquivo que precisam ter _apps mas não tinham aspas simples
ARQUIVOS_FIX = [
    'f1_score_por_classe_svm',
    'f1_score_por_classe_nb',
    'f1_score_por_classe_lr',
    'matriz_confusao_svm',
    'matriz_confusao_nb',
    'matriz_confusao_lr',
]

NOTEBOOKS = [
    'src/05_apps_training.ipynb',
    'src/06_apps_robustness.ipynb',
    'src/07_apps_3_visoes.ipynb',
    'src/08_apps_avancado.ipynb',
]

n_total = 0
for nb_path in NOTEBOOKS:
    with io.open(nb_path, 'r', encoding='utf-8') as f:
        nb = nbf.read(f, as_version=4)

    n_nb = 0
    for i, c in enumerate(nb.cells):
        if c.cell_type != 'code': continue
        src = c.source
        for arq in ARQUIVOS_FIX:
            # Padrão: "arq.png" sem _apps já — substituir por "arq_apps.png"
            # Várias variações: aspas simples, duplas, em f-strings
            for ext in ['.png', '.csv']:
                # Não substitui se já tem _apps
                pat = re.compile(rf'\b{re.escape(arq)}{re.escape(ext)}\b')
                novos = []
                for m in pat.finditer(src):
                    if '_apps' not in m.group(0):
                        novos.append((m.start(), m.end(), arq + '_apps' + ext))
                # Aplica de trás pra frente pra não bagunçar offsets
                for start, end, novo in reversed(novos):
                    src = src[:start] + novo + src[end:]
                    n_nb += 1
        nb.cells[i].source = src

    if n_nb > 0:
        with io.open(nb_path, 'w', encoding='utf-8') as f:
            nbf.write(nb, f)
        print(f'  {os.path.basename(nb_path)}: {n_nb} f-strings corrigidas')
        n_total += n_nb
    else:
        print(f'  {os.path.basename(nb_path)}: nada a corrigir')

print(f'\nTotal: {n_total} substituições')

# Restaura os arquivos de Movies que foram sobrescritos durante o run anterior
print('\n=== Restaurando arquivos de Movies sobrescritos ===')
import subprocess
arquivos_movies = ['resultados/f1_score_por_classe_svm.png', 'resultados/matriz_confusao_svm.png']
for arq in arquivos_movies:
    if os.path.exists(arq):
        # Verifica se o git tem o arquivo original
        r = subprocess.run(['git', 'log', '-1', '--format=%H', '--', arq],
                          capture_output=True, text=True)
        if r.stdout.strip():
            subprocess.run(['git', 'checkout', 'HEAD', '--', arq], check=True)
            print(f'  Restaurado: {arq}')
        else:
            print(f'  Não está no git: {arq} (deixando como está)')

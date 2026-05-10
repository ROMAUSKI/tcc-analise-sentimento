# -*- coding: utf-8 -*-
"""Muda N_POR_CLASSE de 200 para 600 nos notebooks 03 e 04 (decisão de 2026-05-10)."""
import nbformat as nbf
import io

# Notebook 03 — N_POR_CLASSE
with io.open('src/03_movies_3_visoes.ipynb', 'r', encoding='utf-8') as f:
    nb = nbf.read(f, as_version=4)
for i, c in enumerate(nb.cells):
    if c.cell_type != 'code':
        continue
    src = c.source
    if 'N_POR_CLASSE = 200' in src:
        src = src.replace('N_POR_CLASSE = 200', 'N_POR_CLASSE = 600')
        src = src.replace(
            '# Balanceia para 200 frases por classe (controle metodológico)',
            '# Balanceia para 600 frases por classe = sintético inteiro (1800 total)\n# Decisão 2026-05-10: usar todo o sintético gerado e balancear real igual'
        )
        src = src.replace(
            '# Balanceia para 200 frases por classe (mesmo volume do sintético → comparação justa)',
            '# Balanceia para 600 frases por classe (mesmo volume do sintético → comparação justa)'
        )
        nb.cells[i].source = src
        print(f'  Cell {i} atualizada (notebook 03)')
with io.open('src/03_movies_3_visoes.ipynb', 'w', encoding='utf-8') as f:
    nbf.write(nb, f)
print('Notebook 03 salvo.')

# Notebook 04 — N_POR_CLASSE_SINT
with io.open('src/04_movies_avancado.ipynb', 'r', encoding='utf-8') as f:
    nb = nbf.read(f, as_version=4)
for i, c in enumerate(nb.cells):
    if c.cell_type != 'code':
        continue
    src = c.source
    if 'N_POR_CLASSE_SINT = 200' in src:
        src = src.replace('N_POR_CLASSE_SINT = 200', 'N_POR_CLASSE_SINT = 600')
        # Atualiza comentário se houver
        src = src.replace(
            '# --- Sintético (volume controlado, mesmo do notebook 03) ---',
            '# --- Sintético (usar TUDO: 600/classe = 1800 total) ---'
        )
        nb.cells[i].source = src
        print(f'  Cell {i} atualizada (notebook 04)')
with io.open('src/04_movies_avancado.ipynb', 'w', encoding='utf-8') as f:
    nbf.write(nb, f)
print('Notebook 04 salvo.')

# -*- coding: utf-8 -*-
"""
Adiciona uma célula final em todos os notebooks ativos:
- Se LOCAL: não faz nada (resultados já estão no disco)
- Se COLAB: zipa resultados/ e baixa o zip pro PC do usuário
"""
import nbformat as nbf
import io
import os

# Markdown + código pra adicionar
MARKDOWN_BACKUP = (
    "## 💾 Backup automático (Colab → download zip)\n\n"
    "Se rodando no Colab, comprime `resultados/` em zip e baixa pro PC.\n"
    "Se rodando local, não faz nada (arquivos já estão no disco).\n\n"
    "**Sempre rode esta célula ANTES de fechar o Colab** — senão você perde tudo."
)

CODIGO_BACKUP = (
    "# ============================================================\n"
    "# CÉLULA FINAL — Backup automático Colab → download\n"
    "# Local: no-op | Colab: zip + download de resultados/\n"
    "# ============================================================\n"
    "if 'IN_COLAB' not in globals():\n"
    "    # Fallback: detecta de novo caso a célula 1 não tenha definido (raro)\n"
    "    import sys\n"
    "    IN_COLAB = 'google.colab' in sys.modules\n"
    "\n"
    "if IN_COLAB:\n"
    "    import shutil, time\n"
    "    from google.colab import files\n"
    "\n"
    "    if 'RESULTADOS' not in globals():\n"
    "        RESULTADOS = '/content/tcc-analise-sentimento/resultados'\n"
    "\n"
    "    timestamp = time.strftime('%Y%m%d_%H%M%S')\n"
    "    nome_zip = f'resultados_colab_{timestamp}'\n"
    "    zip_path = shutil.make_archive(f'/content/{nome_zip}', 'zip', RESULTADOS)\n"
    "    print(f'✓ Comprimido: {zip_path} ({os.path.getsize(zip_path)/1024:.1f} KB)')\n"
    "    print('✓ Iniciando download... (descompacte em resultados/ no PC local)')\n"
    "    files.download(zip_path)\n"
    "else:\n"
    "    print(f'Ambiente local — resultados já estão em: {RESULTADOS if \"RESULTADOS\" in globals() else \"resultados/\"}')\n"
    "    print('Nenhuma ação necessária.')\n"
)

# Notebooks alvo
NOTEBOOKS = [
    'src/01_movies_training.ipynb',
    'src/02_movies_robustness.ipynb',
    'src/03_movies_3_visoes.ipynb',
    'src/04_movies_avancado.ipynb',
    'src/05_apps_training.ipynb',
    'src/06_apps_robustness.ipynb',
]

for nb_path in NOTEBOOKS:
    if not os.path.exists(nb_path):
        print(f'  PULADO (nao existe): {nb_path}')
        continue

    with io.open(nb_path, 'r', encoding='utf-8') as f:
        nb = nbf.read(f, as_version=4)

    # Verifica se já tem essa célula (evita duplicar)
    ja_existe = False
    for c in nb.cells:
        if c.cell_type == 'code' and 'CÉLULA FINAL — Backup automático Colab' in c.source:
            ja_existe = True
            break
    if ja_existe:
        print(f'  JA TEM: {nb_path}')
        continue

    # Adiciona markdown + código no FIM
    nb.cells.append(nbf.v4.new_markdown_cell(MARKDOWN_BACKUP))
    nb.cells.append(nbf.v4.new_code_cell(CODIGO_BACKUP))

    with io.open(nb_path, 'w', encoding='utf-8') as f:
        nbf.write(nb, f)
    print(f'  OK: {nb_path} (agora com {len(nb.cells)} células)')

print('\nFinalizado.')

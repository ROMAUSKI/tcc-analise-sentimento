# -*- coding: utf-8 -*-
"""Padroniza a célula de setup dos notebooks 01 e 02 com template 'light' (sem kagglehub)."""
import nbformat as nbf
import io

# Template light (sem dataset real — notebooks 01/02 usam só sintético)
TEMPLATE_SETUP = (
    "# ============================================================\n"
    "# CÉLULA DE SETUP — padrão (igual aos notebooks 03 e 04)\n"
    "# ============================================================\n"
    "# Notebooks 01 e 02 usam SOMENTE dados sintéticos (dados/processado/synthetic_dataset.csv)\n"
    "# Por isso o setup aqui é mais leve que o do notebook 03 (sem kagglehub).\n"
    "import os, sys\n"
    "import numpy as np\n"
    "import pandas as pd\n"
    "\n"
    "# Reprodutibilidade\n"
    "SEED = 42\n"
    "np.random.seed(SEED)\n"
    "\n"
    "# Detecção de ambiente\n"
    "IN_COLAB = 'google.colab' in sys.modules\n"
    "\n"
    "if IN_COLAB:\n"
    "    if not os.path.exists('/content/tcc-analise-sentimento'):\n"
    "        os.system('git clone https://github.com/ROMAUSKI/tcc-analise-sentimento.git /content/tcc-analise-sentimento')\n"
    "    else:\n"
    "        os.system('cd /content/tcc-analise-sentimento && git pull')\n"
    "    BASE_DIR = '/content/tcc-analise-sentimento'\n"
    "else:\n"
    "    BASE_DIR = os.path.abspath(os.path.join(os.getcwd(), '..'))\n"
    "\n"
    "# Caminhos do projeto (consistentes em todos os notebooks)\n"
    "DADOS_BRUTOS_MOVIES = os.path.join(BASE_DIR, 'dados', 'brutos')\n"
    "DADOS_BRUTOS_APPS   = os.path.join(BASE_DIR, 'dados', 'brutos_apps')\n"
    "DADOS_PROCESSADO    = os.path.join(BASE_DIR, 'dados', 'processado')\n"
    "RESULTADOS          = os.path.join(BASE_DIR, 'resultados')\n"
    "os.makedirs(RESULTADOS, exist_ok=True)\n"
    "\n"
    "print(f'Ambiente: {\"Colab\" if IN_COLAB else \"Local\"}')\n"
    "print(f'BASE_DIR: {BASE_DIR}')\n"
)

# Notebook 01: célula 0 é o setup
nb_path = 'src/01_movies_training.ipynb'
with io.open(nb_path, 'r', encoding='utf-8') as f:
    nb = nbf.read(f, as_version=4)
nb.cells[0].source = TEMPLATE_SETUP
with io.open(nb_path, 'w', encoding='utf-8') as f:
    nbf.write(nb, f)
print(f'OK: {nb_path} — célula 0 padronizada ({len(nb.cells)} células totais)')

# Notebook 02: célula 1 é o setup (célula 0 é o markdown do título)
nb_path = 'src/02_movies_robustness.ipynb'
with io.open(nb_path, 'r', encoding='utf-8') as f:
    nb = nbf.read(f, as_version=4)
nb.cells[1].source = TEMPLATE_SETUP
with io.open(nb_path, 'w', encoding='utf-8') as f:
    nbf.write(nb, f)
print(f'OK: {nb_path} — célula 1 padronizada ({len(nb.cells)} células totais)')

# Análise de Sentimento com Dados Sintéticos Gerados por IA

**Trabalho de Conclusão de Curso** — Engenharia de Software
Universidade Tecnológica Federal do Paraná — Câmpus Dois Vizinhos (UTFPR-DV)

## Sobre

Este projeto investiga a viabilidade de utilizar dados sintéticos gerados por modelos de linguagem (LLMs) para treinar classificadores de análise de sentimento no domínio de críticas de filmes e séries.

Três ferramentas de IA foram utilizadas para gerar o dataset: **ChatGPT**, **Gemini** e **Claude**. Os dados foram classificados em três categorias de sentimento: **Positiva**, **Negativa** e **Neutra**.

### Perguntas de Pesquisa

1. Qual o nível de assertividade de um modelo treinado com frases geradas artificialmente?
2. A classificação gerada artificialmente é consistente e coerente?

## Estrutura do Projeto

```
├── src/                        # Notebooks Jupyter (Google Colab)
│   ├── 00_data_generation.ipynb      # Planejamento e geração dos dados
│   ├── 01_training_evaluation.ipynb  # Treino e avaliação dos modelos
│   └── 02_robustness_analysis.ipynb  # Experimentos de robustez
│
├── dados/                      # Datasets
│   ├── brutos/                       # CSVs gerados por cada IA (9 arquivos)
│   └── processado/                   # Dataset unificado e limpo
│
├── resultados/                 # Gráficos e métricas geradas
│
├── artigo/                     # Artigo LaTeX (formato SBC)
│   └── imagens/
│
├── requirements.txt            # Dependências Python
└── README.md
```

## Dataset

- **1.798 frases** sintéticas (600 por IA, ~200 por classe por IA)
- **3 classes:** Positiva, Negativa, Neutra
- **3 fontes:** ChatGPT, Gemini, Claude
- Pré-processamento: remoção de duplicatas, caracteres especiais, normalização

## Modelos e Resultados

| Modelo              | Acurácia | Precisão | Recall | F1-Score |
|---------------------|----------|----------|--------|----------|
| Regressão Logística | 86.11%   | 86.18%   | 86.11% | 86.10%   |
| Naive Bayes         | 88.61%   | 88.72%   | 88.61% | 88.63%   |

Vetorização: TF-IDF | Split: 80/20 com seed fixa

## Como Executar

1. Abra os notebooks no [Google Colab](https://colab.research.google.com/)
2. Faça upload da pasta `dados/` para o Google Drive
3. Execute os notebooks na ordem: `00` → `01` → `02`

### Dependências

```bash
pip install pandas scikit-learn matplotlib seaborn nltk wordcloud
```

## Tecnologias

- Python 3 (Google Colab)
- scikit-learn (ML)
- pandas (manipulação de dados)
- matplotlib / seaborn (visualização)
- TF-IDF (vetorização de texto)
- LaTeX (artigo no formato SBC)

## Autor

**Davi Romauski Meurer**
Engenharia de Software — UTFPR Dois Vizinhos

## Licença

Este projeto é parte de um trabalho acadêmico. Uso livre para fins educacionais.

# Notas de Leitura — TCC Análise de Sentimento com Dados Sintéticos

> Autor: Davi Romauski Meurer
> Atualizado em: 24/03/2026

---

## DIA 8 — Análise de Sentimento (Fundamentos)

### 1. Jurafsky & Martin (2025) — Speech and Language Processing, 3ª edição

- **Referência:** Jurafsky, D. & Martin, J. H. (2025). *Speech and Language Processing*, 3rd ed. Stanford University. Disponível em: https://web.stanford.edu/~jurafsky/slp3/
- **Capítulos relevantes:**
  - **Cap. 4 — Naive Bayes, Text Classification, and Sentiment:** Define análise de sentimento como tarefa de classificação de texto; apresenta o modelo bag-of-words, TF-IDF como esquema de ponderação, e Naive Bayes como classificador probabilístico baseline. Discute a suposição de independência condicional das features e a importância da suavização de Laplace. Apresenta métricas de avaliação: acurácia, precisão, recall, F1-score.
  - **Cap. 25 (atualmente reorganizado em capítulos sobre embeddings e LLMs):** Aborda representações distribuídas de palavras (word embeddings) e modelos de linguagem baseados em redes neurais/transformers.
- **O que posso citar no artigo:**
  - Definição formal de análise de sentimento e classificação de texto
  - Justificativa teórica para uso de TF-IDF + Naive Bayes como baseline
  - Referência canônica para fundamentação do pipeline clássico (bag-of-words → vetorização → classificador)

---

### 2. Pang, Lee & Vaithyanathan (2002) — Thumbs Up? Sentiment Classification using Machine Learning Techniques

- **Referência:** Pang, B., Lee, L., & Vaithyanathan, S. (2002). Thumbs Up? Sentiment Classification using Machine Learning Techniques. *Proceedings of EMNLP 2002*, pp. 79–86. DOI: 10.3115/1118693.1118704
- **O que fizeram:** Trabalho seminal que propôs o uso de técnicas de machine learning (Naive Bayes, Maximum Entropy, SVM) para classificação de sentimento em reviews de filmes do IMDB. Compararam abordagens baseadas em ML com heurísticas baseadas em léxico.
- **Dataset:** Reviews de filmes do IMDB (positivo/negativo)
- **Resultados:** ML superou abordagens léxicas; SVM obteve melhor desempenho (~82.9% acurácia), seguido de Maximum Entropy e Naive Bayes.
- **O que posso citar:** Referência fundadora da área; justifica a abordagem de usar ML para classificação de sentimento em reviews de filmes (diretamente relacionado ao meu TCC).
- **Já está no referencias.bib:** Sim (`pang2002`)

---

### 3. Souza & Filho (2021) — Sentiment Analysis on Brazilian Portuguese User Reviews

- **Referência:** Souza, F. & Filho, J. (2021). Sentiment Analysis on Brazilian Portuguese User Reviews. *arXiv:2112.05459*. Publicado em *IEEE LA-CCI 2022*.
- **O que fizeram:** Analisaram o desempenho preditivo de estratégias de document embedding para classificação de sentimento em português brasileiro. Unificaram 5 datasets de análise de sentimento em PT-BR em um único dataset com partições de referência (treino/teste/validação).
- **Dataset:** 5 datasets de análise de sentimento em PT-BR unificados
- **Resultados:** Demonstraram que PT-BR possui recursos linguísticos limitados para classificação de sentimento; compararam múltiplas estratégias de embedding.
- **O que posso citar:** Escassez de datasets em PT-BR para análise de sentimento; justifica a necessidade de gerar dados sintéticos como alternativa.
- **URL:** https://arxiv.org/abs/2112.05459

---

### 4. Araujo, Melo & Figueiredo (2024) — Is ChatGPT an Effective Solver of Sentiment Analysis Tasks in Portuguese?

- **Referência:** Araujo, G., de Melo, T., & Figueiredo, C. M. S. (2024). Is ChatGPT an effective solver of sentiment analysis tasks in Portuguese? A Preliminary Study. *Proceedings of PROPOR 2024*, pp. 13–21. Santiago de Compostela, Espanha.
- **O que fizeram:** Investigaram as capacidades do ChatGPT para análise de sentimento zero-shot em português brasileiro, focando em identificação de sentenças opinativas, cálculo de polaridade e identificação de sentenças comparativas.
- **Resultados:** ChatGPT se destacou em determinar polaridade, mas teve dificuldades com sentenças subjetivas e comparativas. ChatGPT pode ser útil para anotação de labels de datasets, oferecendo solução prática para treinar modelos alternativos.
- **O que posso citar:** Validação de que LLMs podem gerar/anotar dados de sentimento em PT-BR; diretamente relevante para justificar o uso de LLMs como geradores de dados sintéticos no meu trabalho.
- **URL:** https://aclanthology.org/2024.propor-1.2/

---

### 5. Souza, de Souza & Meinerz (2021) — Análise de Sentimento em Tempo Real

- **Referência:** de Souza, V. A., de Souza, É. F., & Meinerz, G. V. (2021). Análise de sentimento em tempo real. *Brazilian Journal of Development*, 7(1), pp. 11084–11091. DOI: 10.34117/bjdv7n1-758
- **O que fizeram:** Implementaram sistema de análise de sentimento em tempo real em português.
- **O que posso citar:** Exemplo de aplicação prática de análise de sentimento em PT-BR.
- **Já está no referencias.bib:** Sim (`souza2021`)

---

### 6. Kansaon & Moro (2019) — Análise de Sentimentos em Tweets em Português Brasileiro

- **Referência:** Kansaon, D. J. & Moro, S. (2019). Análise de Sentimentos em Tweets em Português Brasileiro. *Anais do BrasNAM 2019*. UFMG.
- **O que fizeram:** Análise de sentimento em tweets em PT-BR usando abordagens de machine learning.
- **O que posso citar:** Mais um exemplo de trabalho em PT-BR; contextualiza a lacuna de recursos e datasets para o português.
- **Já está no referencias.bib:** Sim (`kansaon2019`)

---

## DIA 9 — Dados Sintéticos + LLMs para Geração de Dados

### 7. Zhang et al. (2024) — Sentiment Analysis in the Era of Large Language Models: A Reality Check

- **Referência:** Zhang, W., Deng, Y., Liu, B., Pan, S., & Bing, L. (2024). Sentiment Analysis in the Era of Large Language Models: A Reality Check. *Findings of NAACL 2024*, pp. 3881–3906. México.
- **O que fizeram:** Avaliação abrangente do desempenho de LLMs em tarefas de análise de sentimento, comparando com modelos menores fine-tuned. Testaram múltiplos LLMs (GPT-3.5, GPT-4, etc.) em diversas tarefas de sentimento.
- **Resultados:** LLMs demonstram desempenho satisfatório em tarefas mais simples, mas ficam atrás em tarefas complexas que requerem compreensão profunda de fenômenos de sentimento. LLMs superam significativamente small language models em cenários few-shot, sugerindo potencial quando recursos de anotação são limitados.
- **O que posso citar:** Justifica que LLMs são capazes de lidar com tarefas de sentimento (relevante para geração de dados); contextualiza o estado-da-arte; mostra que dados gerados por LLMs podem servir de proxy para anotação humana.
- **URL:** https://aclanthology.org/2024.findings-naacl.246/
- **Como meu trabalho se diferencia:** Meu TCC foca na geração de dados sintéticos de treinamento, não no uso direto de LLMs como classificadores.

---

### 8. Hellwig, Fehle & Wolff (2025) — Exploring LLMs for Generation of Synthetic Training Samples for ABSA

- **Referência:** Hellwig, N. C., Fehle, J., & Wolff, C. (2025). Exploring large language models for the generation of synthetic training samples for aspect-based sentiment analysis in low resource settings. *Expert Systems with Applications*, 261, 125514.
- **O que fizeram:** Exploraram GPT-3.5-turbo e Llama-3-70B para gerar dados anotados para Aspect-Based Sentiment Analysis (ABSA) em cenários de poucos recursos. Testaram geração zero-shot e few-shot.
- **Resultados:** Com 25 exemplos, a adição de dados sintéticos via few-shot prompting resultou em F1 de 81.33 para Aspect Category Detection e 71.71 para ACSA.
- **O que posso citar:** **Trabalho mais diretamente relacionado ao meu TCC.** Demonstra que dados sintéticos gerados por LLMs podem melhorar o desempenho de modelos em cenários de poucos recursos. A diferença é que eles focaram em ABSA, enquanto eu foco em classificação de sentimento geral (3 classes).
- **Como meu trabalho se diferencia:** (1) Foco em classificação geral vs. aspect-based; (2) Uso de 3 LLMs diferentes como geradores; (3) Análise de coerência entre LLMs; (4) Dados em português.
- **URL:** https://www.sciencedirect.com/science/article/pii/S0957417424023819

---

### 9. Li et al. (2023) — Synthetic Data Generation with LLMs for Text Classification: Potential and Limitations

- **Referência:** Li, Z., Zhu, H., Lu, Z., & Yin, M. (2023). Synthetic Data Generation with Large Language Models for Text Classification: Potential and Limitations. *Proceedings of EMNLP 2023*. arXiv:2310.07849.
- **O que fizeram:** Avaliaram o GPT-3.5-Turbo na geração de dados sintéticos para diferentes tarefas de classificação de texto, tanto em cenários zero-shot como few-shot.
- **Resultados:** A efetividade dos dados sintéticos é inconsistente entre diferentes tarefas. A subjetividade (tanto a nível de tarefa quanto de instância) está negativamente associada ao desempenho do modelo treinado com dados sintéticos.
- **O que posso citar:** Evidência empírica de que dados sintéticos funcionam melhor para tarefas menos subjetivas; a classificação de sentimento de filmes pode ser considerada moderadamente subjetiva, o que contextualiza os resultados do meu TCC.
- **URL:** https://arxiv.org/abs/2310.07849

---

### 10. Liu et al. (2024) — Best Practices and Lessons Learned on Synthetic Data for Language Models

- **Referência:** Liu, R., Wei, J., Liu, F., Si, C., Zhang, Y., Rao, J., Zheng, S., Peng, D., Yang, D., Zhou, D., & Dai, A. M. (2024). Best Practices and Lessons Learned on Synthetic Data for Language Models. *COLM 2024*. arXiv:2404.07503.
- **O que fizeram:** Survey abrangente (Google DeepMind + Stanford) das melhores práticas para uso de dados sintéticos no treinamento de modelos de linguagem. Cobrem geração, curadoria, avaliação e aplicações.
- **Resultados:** Descrevem técnicas de filtragem, ponderação e refinamento iterativo de dados sintéticos. Discutem riscos como amplificação de viés e colapso de modelos (model collapse).
- **O que posso citar:** Fundamentação teórica para o uso de dados sintéticos; melhores práticas que validam ou contextualizam minhas escolhas metodológicas; riscos e limitações do approach.
- **URL:** https://arxiv.org/abs/2404.07503

---

### 11. Nadas, Diosan & Tomescu (2025) — Synthetic Data Generation Using LLMs: Advances in Text and Code

- **Referência:** Nadas, M., Diosan, L., & Tomescu, A. (2025). Synthetic Data Generation Using Large Language Models: Advances in Text and Code. *arXiv:2503.14023*.
- **O que fizeram:** Survey que revisa como LLMs estão transformando a geração de dados sintéticos de treinamento em linguagem natural e código. Cobrem prompt-based generation, retrieval-augmented pipelines e iterative self-refinement.
- **Resultados:** Métodos enriquecem tarefas de poucos recursos (classificação, QA). Discutem desafios como imprecisões factuais, falta de realismo estilístico e amplificação de viés.
- **O que posso citar:** Survey mais recente (2025) sobre o tema; contextualiza o estado-da-arte da geração de dados sintéticos com LLMs.
- **URL:** https://arxiv.org/abs/2503.14023

---

## Resumo: Como meu trabalho se diferencia

A maioria dos trabalhos encontrados:
1. Usa LLMs como **classificadores** diretos (zero-shot/few-shot), não como **geradores** de dados de treinamento
2. Foca em **inglês** — poucos trabalhos abordam português brasileiro
3. Usa um **único LLM** como gerador — meu trabalho compara **3 LLMs diferentes** (ChatGPT, Gemini, Claude)
4. Não analisa a **coerência entre LLMs** na geração de dados

Minha contribuição original: avaliar se dados sintéticos gerados por múltiplos LLMs são suficientes para treinar modelos clássicos de ML para análise de sentimento em PT-BR, e se há coerência na classificação entre os diferentes geradores.

---

## DIA 10 — Avaliação de Modelos + Trabalhos Similares

### 12. Sokolova & Lapalme (2009) — A Systematic Analysis of Performance Measures for Classification Tasks

- **Referência:** Sokolova, M. & Lapalme, G. (2009). A systematic analysis of performance measures for classification tasks. *Information Processing & Management*, 45(4), pp. 427–437. DOI: 10.1016/j.ipm.2009.03.002
- **O que fizeram:** Análise sistemática de 24 métricas de desempenho usadas em tarefas de classificação de ML — binária, multi-classe, multi-label e hierárquica. Propõem uma taxonomia de invariância das métricas com relação a mudanças na matriz de confusão.
- **Resultados:** Demonstram que diferentes métricas capturam aspectos distintos do desempenho de um classificador. Para problemas multi-classe (como o meu TCC), métricas como F1-macro são mais informativas que acurácia simples quando há desbalanceamento de classes. A análise mostra que a escolha da métrica deve ser guiada pela aplicação e pelas características dos dados.
- **O que posso citar:** Fundamentação teórica para a escolha de métricas de avaliação (acurácia, precisão, recall, F1-Score) no meu TCC. Justifica por que reporto múltiplas métricas e não apenas acurácia. Referência canônica sobre métricas de classificação com mais de 5.000 citações.
- **URL:** https://www.sciencedirect.com/science/article/abs/pii/S0306457309000259

---

### 13. Kohavi (1995) — A Study of Cross-Validation and Bootstrap for Accuracy Estimation and Model Selection

- **Referência:** Kohavi, R. (1995). A study of cross-validation and bootstrap for accuracy estimation and model selection. *Proceedings of the 14th International Joint Conference on Artificial Intelligence (IJCAI)*, pp. 1137–1145.
- **O que fizeram:** Experimento em larga escala (mais de 500.000 execuções) comparando métodos de estimação de acurácia — cross-validation e bootstrap — usando C4.5 e Naive Bayes em datasets reais. Variaram o número de folds na cross-validation e o número de amostras no bootstrap.
- **Resultados:** Para seleção de modelo em datasets reais, a validação cruzada estratificada com 10 folds é o melhor método, mesmo quando há poder computacional para usar mais folds. Leave-one-out tende a ter alta variância. O estudo consolidou o k=10 como padrão de fato na comunidade de ML.
- **O que posso citar:** Justificativa direta para a escolha de k=10 na validação cruzada do meu TCC. Referência fundamental (mais de 14.000 citações) que embasa a metodologia de avaliação dos modelos NB, LR e SVM.
- **URL:** https://dl.acm.org/doi/10.5555/1643031.1643047

---

### 14. Pedregosa et al. (2011) — Scikit-learn: Machine Learning in Python

- **Referência:** Pedregosa, F., Varoquaux, G., Gramfort, A., Michel, V., Thirion, B., Grisel, O., ... & Duchesnay, E. (2011). Scikit-learn: Machine Learning in Python. *Journal of Machine Learning Research*, 12, pp. 2825–2830.
- **O que fizeram:** Apresentação do scikit-learn, biblioteca Python de ML que integra algoritmos de classificação, regressão, clustering, redução de dimensionalidade, seleção de modelo e pré-processamento. Foco em facilidade de uso, performance e consistência de API.
- **O que posso citar:** Referência obrigatória para qualquer trabalho que use scikit-learn. Justifica a ferramenta utilizada para implementar TF-IDF, Naive Bayes (MultinomialNB), Logistic Regression, SVM Linear, validação cruzada (StratifiedKFold) e curvas de aprendizado (learning_curve) no meu pipeline. Uma das publicações mais citadas em ML (>100.000 citações).
- **URL:** https://jmlr.org/papers/v12/pedregosa11a.html

---

### 15. Souza (2019) — TCC UTFPR: Ferramentas de Análise de Sentimentos (Collabora)

- **Referência:** Souza, [nome não disponível] (2019). Ferramentas de Análise de Sentimentos. *Trabalho de Conclusão de Curso*. Universidade Tecnológica Federal do Paraná (UTFPR).
- **O que fizeram:** TCC da UTFPR que aborda ferramentas para análise de sentimento, possivelmente em contexto colaborativo.
- **O que posso citar:** Evidência de que a UTFPR já possui trabalhos na área de análise de sentimento, o que contextualiza o meu TCC dentro da produção acadêmica da instituição. Diferencial: meu trabalho foca em dados sintéticos gerados por LLMs, abordagem que não aparece nos TCCs anteriores da UTFPR.
- **URL:** https://repositorio.utfpr.edu.br/jspui/bitstream/1/26457/1/ferramentasanalisesentimentoscollabora.pdf
- **Nota:** Preciso baixar o PDF completo para confirmar detalhes (autor, campus, orientador).

---

## Resumo Atualizado: Referências no .bib

Após o Dia 10, o projeto conta com 15 referências relevantes (excluindo as 3 do template SBC que serão removidas):

| # | Chave | Tema | Status no .bib |
|---|---|---|---|
| 1 | jm3 | Livro-base de PLN | ✅ |
| 2 | pang2002 | Trabalho seminal SA + ML | ✅ |
| 3 | souza2021 | SA em tempo real PT-BR | ✅ |
| 4 | kansaon2019 | SA em tweets PT-BR | ✅ |
| 5 | rossi2019 | SA cidades inteligentes | ✅ |
| 6 | lecun2015deep | Deep learning (geral) | ✅ |
| 7 | souza2022brazilian | SA em reviews PT-BR | ✅ |
| 8 | araujo2024chatgpt | ChatGPT como SA solver | ✅ |
| 9 | zhang2024sentiment | SA na era dos LLMs | ✅ |
| 10 | hellwig2025exploring | Dados sintéticos ABSA | ✅ |
| 11 | li2023synthetic | Dados sintéticos classificação | ✅ |
| 12 | liu2024best | Best practices dados sintéticos | ✅ |
| 13 | nadas2025synthetic | Survey dados sintéticos 2025 | ✅ |
| 14 | sokolova2009 | Métricas de classificação | 🆕 adicionar |
| 15 | kohavi1995 | Cross-validation k=10 | 🆕 adicionar |
| 16 | pedregosa2011 | Scikit-learn | 🆕 adicionar |

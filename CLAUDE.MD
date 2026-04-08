# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Projeto

- **Título:** Análise de Sentimentos em Críticas de Cinema com Dados Sintéticos Gerados por LLMs
- **Aluno:** Davi Romauski Meurer — UTFPR Dois Vizinhos, Eng. Software, 8º sem.
- **Orientador:** Prof. Marlon Marcon
- **Repo:** https://github.com/ROMAUSKI/tcc-analise-sentimento

## Perguntas de Pesquisa

1. Qual a assertividade dos modelos treinados com dados sintéticos?
2. A classificação é coerente entre os diferentes LLMs geradores?

## Comandos

```bash
# Instalar dependências localmente
pip install pandas scikit-learn matplotlib seaborn nltk wordcloud

# Executar notebooks (ordem obrigatória)
jupyter notebook src/01_training_evaluation.ipynb
jupyter notebook src/02_robustness_analysis.ipynb

# Compilar artigo LaTeX (ou usar Overleaf)
cd artigo && latexmk -pdf main.tex
```

## Arquitetura e Fluxo de Dados

### Pipeline (ordem obrigatória)

```
dados/brutos/ (9 CSVs)
  → 01_training_evaluation.ipynb (unifica, limpa, vetoriza, treina, avalia)
    → dados/processado/synthetic_dataset.csv
    → resultados/baseline_metrics.csv + gráficos (.png)
      → 02_robustness_analysis.ipynb (cross-validation, curvas de aprendizado, análise de erros)
        → resultados/*.csv + resultados/*.png
          → artigo/imagens/ (cópia manual dos gráficos relevantes)
```

**Dependência crítica:** O notebook `02` consome `synthetic_dataset.csv` gerado pelo `01`. Alteração no `01` pode quebrar o `02` — sempre verificar a cadeia.

### Detecção de ambiente nos notebooks

Ambos os notebooks detectam automaticamente Colab vs local na Célula 1:
- **Notebook 01:** usa `'google.colab' in sys.modules` → clona o repo se no Colab
- **Notebook 02:** usa `os.path.exists('/content')` → clona/pull se no Colab; local usa `os.path.join(os.getcwd(), '..')`

### Dataset

- **Arquivo:** `dados/processado/synthetic_dataset.csv`
- **Colunas:** `frase_limpa` (X), `classe` (y), `fonte` (LLM gerador), `frase` (original)
- **1798 linhas** — 3 classes (Positiva ~600, Negativa ~598, Neutra ~600) × 3 fontes (ChatGPT, Claude, Gemini)
- **Split:** 80/20 estratificado, seed=42
- **Vetorização:** TF-IDF (max_features=5000)

### Modelos

| Modelo | Classe sklearn |
|---|---|
| Naive Bayes (baseline) | `MultinomialNB()` |
| Regressão Logística | `LogisticRegression(max_iter=1000)` |
| SVM Linear | `LinearSVC(max_iter=5000)` |

Todos encapsulados em `Pipeline([('tfidf', TfidfVectorizer(...)), ('clf', ...)])`.

### Artigo (LaTeX formato SBC)

- **Arquivo principal:** `artigo/main.tex`
- Template SBC: `sbc-template.sty`, `sbc.bst`
- Imagens em `artigo/imagens/` — copiadas de `resultados/`
- Seções: Introdução, Fund. Teórica, Trab. Relacionados, Metodologia, Resultados, Conclusão

## Regras do Projeto

1. Passo a passo incremental — um passo por vez, verificável
2. Antes de alterar código, checar impacto no pipeline (`⚠️ SYNC:`)
3. **Nunca inventar métricas** — pedir para executar o notebook
4. seed=42 em todo código com aleatoriedade
5. Artigo formato SBC — não alterar template

## Estado Atual (Abril/2026)

- ✅ Dataset gerado e processado
- ✅ Notebook 01 completo (treinamento + avaliação baseline)
- ✅ Notebook 02 completo (cross-validation, boxplots, learning curves, análise de erros)
- ✅ Artigo: PRIMEIRA VERSÃO COMPLETA (Seções 1-6 + Resumo + Abstract)
- ❌ Revisão final do artigo (leitura corrida, ortografia, consistência)
- ❌ Slides: não iniciados

---

## 🎓 MODO DEFESA — Guia de Estudo e Explicação para o Davi

> **REGRA PARA O CLAUDE:** Sempre que o Davi perguntar algo técnico sobre o TCC, pedir ajuda para slides, ou ensaiar respostas de banca, use esta seção como base. Explique de forma simples, direta, como se estivesse ensinando o Davi a explicar com as próprias palavras. Inclua sempre: (1) o que é, em uma frase simples, (2) como o Davi deve explicar na apresentação, (3) possíveis perguntas da banca sobre aquele ponto e respostas sugeridas.

---

### 1. Tipo de Arquitetura — "Meus modelos NÃO são redes neurais"

**O que é:** O trabalho usa aprendizado de máquina clássico (ML tradicional), não deep learning. Nenhum dos três modelos (Naive Bayes, Regressão Logística, SVM) é uma rede neural. Não têm camadas ocultas, não usam backpropagation no sentido de deep learning, não aprendem representações internas do texto.

**Como explicar:** "Meu trabalho usa três classificadores de aprendizado de máquina clássico — Naive Bayes, Regressão Logística e SVM Linear — combinados com representação TF-IDF. Não são redes neurais. A escolha foi intencional: o objetivo é avaliar a qualidade dos dados sintéticos, não o classificador. Modelos simples isolam melhor o efeito dos dados."

**Hierarquia para ter na cabeça:**
- ML Clássico (seus modelos) → usa features extraídas manualmente (TF-IDF)
- Deep Learning / Redes Neurais (BERT, CNNs) → aprende representações em múltiplas camadas
- LLMs (GPT, Claude, Gemini) → redes neurais gigantes que geraram seus dados

**Perguntas prováveis da banca:**
- **"Por que não usou BERT ou outro modelo neural?"** → "O foco do trabalho é avaliar os dados sintéticos, não maximizar a acurácia. Modelos clássicos com TF-IDF são mais transparentes e permitem isolar o efeito da qualidade dos dados. BERT é sugerido como trabalho futuro."
- **"Você sabe a diferença entre modelo generativo e discriminativo?"** → "Sim. O Naive Bayes é generativo — modela P(X|classe) e usa Bayes para inverter. A Regressão Logística e o SVM são discriminativos — aprendem diretamente a fronteira de decisão P(classe|X). Normalmente discriminativos ganham com mais dados, mas no meu trabalho o NB venceu, provavelmente porque dados sintéticos têm distribuição de vocabulário mais regular."
- **"Se são modelos simples, por que usar três?"** → "Para comparação. Cada um tem uma lógica diferente (probabilístico, linear discriminativo, margem máxima) e reagem de formas distintas às características dos dados sintéticos. Isso enriquece a análise."

---

### 2. TF-IDF — A Representação de Texto

**O que é:** TF-IDF (Term Frequency–Inverse Document Frequency) transforma cada frase em um vetor numérico. Cada posição do vetor corresponde a uma palavra do vocabulário, e o valor é o peso TF-IDF — que aumenta se a palavra aparece muito na frase (TF), mas diminui se aparece em muitos documentos (IDF). Isso penaliza palavras comuns (artigos, preposições) e valoriza palavras discriminativas.

**Como explicar:** "O TF-IDF pega cada frase e transforma num vetor de números. Cada número representa o quão importante uma palavra é naquela frase específica, comparado com o resto do corpus. Palavras que aparecem em tudo, como 'de' ou 'o', recebem peso baixo. Palavras específicas como 'péssimo' ou 'excelente' recebem peso alto."

**A fórmula (saber de cor):**
TF-IDF(t, d) = TF(t, d) × log(N / DF(t))
- TF(t,d) = quantas vezes o termo t aparece no documento d
- N = total de documentos no corpus
- DF(t) = em quantos documentos o termo t aparece

**Perguntas prováveis da banca:**
- **"Por que TF-IDF e não bag-of-words simples?"** → "BoW conta frequência bruta, então palavras comuns dominam o vetor. TF-IDF corrige isso penalizando termos muito frequentes no corpus. Rossi (2019) mostrou que TF-IDF apresenta ganhos consistentes sobre BoW na maioria dos cenários de classificação de sentimento."
- **"Por que não usou embeddings (Word2Vec, BERT)?"** → "Embeddings são representações aprendidas que capturam semântica, mas exigem modelos mais complexos para aproveitá-las. TF-IDF com classificadores lineares é o baseline padrão na literatura e suficiente para o escopo do trabalho."
- **"Removeu stopwords?"** → "Não. O TfidfVectorizer foi usado com parâmetros padrão. O IDF já penaliza naturalmente palavras muito frequentes, então a remoção explícita de stopwords é menos crítica com TF-IDF do que com BoW."

---

### 3. Os Três Modelos — O que cada um faz

#### 3a. Naive Bayes (Multinomial)

**O que é:** Classificador probabilístico baseado no Teorema de Bayes. Calcula a probabilidade de cada classe dada as palavras da frase. A suposição "naive" (ingênua) é que as palavras são independentes entre si dado a classe — o que não é verdade na prática, mas funciona surpreendentemente bem para texto.

**Como explicar:** "O Naive Bayes olha para cada palavra da frase e pergunta: 'em frases positivas, qual a chance de essa palavra aparecer? E em negativas? E em neutras?' Multiplica todas as probabilidades e escolhe a classe com maior probabilidade final."

**Por que foi o melhor no seu trabalho:** Dados sintéticos de LLMs têm vocabulário mais regular e previsível do que dados reais. Cada LLM repete padrões de palavras por classe. Essa regularidade é exatamente o que o NB captura bem.

**Perguntas prováveis:**
- **"A suposição de independência não é uma limitação forte?"** → "Na teoria, sim. Na prática, o NB funciona bem para classificação de texto porque a decisão depende mais da presença/ausência de certas palavras do que da ordem delas. E nos dados sintéticos, essa suposição se sustenta ainda melhor porque LLMs tendem a usar vocabulário mais padronizado por classe."
- **"Por que o NB venceu a Regressão Logística, se a literatura diz o contrário?"** → "Isso é discutido na Seção 5.1 do artigo. A hipótese é que dados sintéticos têm distribuição de vocabulário mais regular, o que favorece o modelo generativo. Pang (2002) fez essa observação com dados reais do IMDb — aqui, com dados sintéticos, o efeito parece amplificado."

#### 3b. Regressão Logística

**O que é:** Classificador discriminativo que aprende diretamente a fronteira de decisão entre as classes. Atribui um peso a cada palavra do vocabulário e faz uma soma ponderada para decidir a classe. É como um neurônio único sem camadas ocultas.

**Como explicar:** "A Regressão Logística aprende um peso para cada palavra. Palavras como 'excelente' ganham peso positivo para a classe Positiva, 'péssimo' ganha peso positivo para Negativa. Na hora de classificar, soma os pesos das palavras presentes na frase e escolhe a classe com maior pontuação."

**Perguntas prováveis:**
- **"Qual a diferença entre Regressão Logística e Naive Bayes?"** → "NB é generativo — modela como cada classe 'gera' os dados. LR é discriminativa — aprende direto a fronteira entre as classes. NB calcula P(palavras|classe), LR calcula P(classe|palavras) diretamente."
- **"Por que a LR ficou abaixo?"** → "A LR precisa de mais dados para estimar bem a fronteira de decisão. As curvas de aprendizado mostram que ela converge com 70-80% dos dados, enquanto o NB atinge platô com 50-60%. Com um dataset maior, a LR provavelmente melhoraria."

#### 3c. SVM Linear (Support Vector Machine)

**O que é:** Busca o hiperplano que separa as classes com a maior margem possível. "Margem" é a distância entre o hiperplano e os pontos mais próximos de cada classe (os support vectors). Com kernel linear, é especialmente bom para texto porque o espaço de features é de alta dimensão.

**Como explicar:** "O SVM traça uma linha (ou hiperplano, em alta dimensão) entre as classes e tenta maximizar a distância dessa linha até os exemplos mais próximos de cada lado. Quanto maior a margem, melhor a generalização."

**Perguntas prováveis:**
- **"Por que usou kernel linear e não RBF?"** → "Em classificação de texto com TF-IDF, o espaço já é de alta dimensionalidade (milhares de features). Kernel linear funciona bem nesses casos e é mais eficiente computacionalmente. É a recomendação padrão na literatura."
- **"SVM e LR tiveram resultados parecidos — por quê?"** → "Ambos são classificadores lineares discriminativos. A principal diferença é o critério de otimização — LR minimiza o log-loss, SVM maximiza a margem. Em datasets com classes bem separadas, ambos convergem para fronteiras similares."

---

### 4. Dados Sintéticos — O Core do Trabalho

**O que é:** Todo o dataset (1798 frases) foi gerado por três LLMs via interface web com prompts manuais. Nenhum dado foi coletado de reviews reais. Isso é ao mesmo tempo a contribuição principal e a limitação principal do trabalho.

**Como explicar:** "A ideia central é: se LLMs conseguem gerar texto realista, será que conseguem gerar dados de treinamento bons o suficiente para treinar classificadores? Isso é relevante especialmente para português brasileiro, onde datasets rotulados de sentimento são escassos."

**Perguntas prováveis da banca:**
- **"Por que não usou dados reais?"** → "O objetivo era justamente testar se dados sintéticos são viáveis como alternativa. Usar dados reais no treinamento não responderia essa pergunta. A validação com dados reais é o próximo passo natural e está indicada como trabalho futuro."
- **"Como garantiu que os dados sintéticos são de qualidade?"** → "Três mecanismos: (1) prompts padronizados com definição explícita de cada classe, (2) três fontes geradoras distintas para reduzir viés de um único LLM, (3) pré-processamento com remoção de duplicatas. Além disso, a análise de erros por fonte geradora no notebook 02 avalia indiretamente a qualidade."
- **"Os LLMs não podem ter 'decorado' frases reais do treinamento deles?"** → "É uma possibilidade — LLMs são treinados em grandes corpora que incluem reviews. Mas como o objetivo é gerar dados de treinamento e não avaliar originalidade, isso não invalida a abordagem. Na verdade, se os LLMs reproduzem padrões linguísticos realistas, isso favorece a qualidade do dataset."
- **"Por que ChatGPT, Gemini e Claude especificamente?"** → "São os três maiores LLMs comerciais disponíveis via interface gratuita, cada um de uma empresa diferente (OpenAI, Google, Anthropic), com arquiteturas e dados de treinamento distintos. Isso maximiza a diversidade estilística. O Copilot foi descartado por usar modelos GPT da OpenAI, o que duplicaria a base."
- **"Os prompts foram iguais para os três LLMs?"** → "Sim, prompts padronizados descrevendo a classe, a definição e o domínio. Porém, como cada LLM interpreta o prompt de forma diferente, as frases geradas variam em estilo — ChatGPT mais direto (~50 chars), Gemini mais descritivo (~61 chars), Claude mais elaborado (~95 chars)."

---

### 5. Métricas de Avaliação — O que cada uma mede

**Acurácia:** Proporção de acertos sobre o total. Simples e intuitiva, mas pode enganar se as classes forem desbalanceadas. No seu caso as classes são equilibradas (~600 cada), então acurácia é confiável.

**Precisão:** "De tudo que o modelo disse que era Positivo, quanto realmente era?" → Mede falsos positivos.

**Recall:** "De tudo que realmente era Positivo, quanto o modelo acertou?" → Mede falsos negativos.

**F1-Score:** Média harmônica entre Precisão e Recall. Útil quando você quer equilíbrio entre os dois. É a métrica principal do trabalho.

**Como explicar a diferença Precisão vs Recall:** "Se um detector de spam tem precisão alta, quase tudo que ele marca como spam realmente é spam. Se tem recall alto, ele pega quase todos os spams — mas pode marcar emails bons como spam também."

**Perguntas prováveis:**
- **"Por que usou F1-Score ponderado (weighted) e não macro?"** → "O weighted pondera pelo número de amostras por classe, o que dá uma visão mais realista do desempenho geral. Como as classes são quase equilibradas, a diferença entre weighted e macro é mínima."
- **"Por que validação cruzada e não só o split 80/20?"** → "O split simples depende de uma única divisão aleatória e pode não ser representativo. A validação cruzada com k=10 garante que cada amostra é testada exatamente uma vez, dando uma estimativa mais robusta e um desvio padrão que mostra a variabilidade."
- **"k=5 ou k=10, qual é melhor?"** → "Kohavi (1995) recomenda k=10 como o melhor trade-off entre viés e variância para datasets de tamanho moderado. No trabalho, ambos foram reportados para comparação."

---

### 6. Validação Cruzada — Como funciona

**O que é:** Divide o dataset em k partes iguais (folds). Para cada fold, treina com k-1 partes e testa com a parte restante. Repete k vezes (cada parte é teste uma vez). O resultado final é a média e desvio padrão dos k testes.

**Como explicar:** "Imagina que eu divido minhas 1798 frases em 10 grupos. Treino com 9 grupos, testo com 1. Repito 10 vezes, cada vez com um grupo diferente de teste. No final, tenho 10 valores de F1, tiro a média e o desvio padrão. Isso me dá uma estimativa muito mais confiável do que um único split."

**"Estratificada" significa:** cada fold mantém a mesma proporção de classes (Positiva, Negativa, Neutra) que o dataset completo. Sem isso, um fold poderia ter muitas Positivas e poucas Neutras por azar.

**Perguntas prováveis:**
- **"O desvio padrão de 2,5% é alto?"** → "Para um dataset de ~1800 frases, é normal. Desvios abaixo de 3% indicam boa estabilidade. O NB teve o menor desvio com k=5 (1,82%), mostrando que é o modelo mais robusto entre os três."

---

### 7. Curvas de Aprendizado — O que mostram

**O que é:** Gráficos que mostram como o desempenho (F1-Score) varia conforme se aumenta a quantidade de dados de treino, de 10% até 100%.

**Para que servem:** Diagnosticar (1) se o modelo está com overfitting (curva de treino alta, validação baixa = gap grande), (2) se mais dados ajudariam (curva de validação ainda subindo no final), (3) se o dataset atual é suficiente (curva de validação estabilizou = platô).

**Resultados do seu trabalho:**
- NB: platô com 50-60% dos dados → 1798 frases já são suficientes
- LR e SVM: platô com 70-80% → se beneficiariam de mais dados
- Nenhum modelo tem overfitting severo (gaps pequenos no final)

**Perguntas prováveis:**
- **"Se o NB atinge platô com 50% dos dados, por que não usou menos dados?"** → "Porque o dataset serve para os três modelos. LR e SVM ainda melhoram até 70-80%. Além disso, usar o dataset completo dá robustez à validação cruzada."

---

### 8. Análise de Erros — Os achados mais interessantes

**O que é:** Análise detalhada dos 50 erros do Naive Bayes no conjunto de teste (360 amostras, 13,9% de erro).

**Dois padrões principais de erro:**
1. **Inversão de polaridade (24/50):** Frases com negação ou vocabulário ambíguo. Ex: "os efeitos especiais são muito ruins para a época" → "especiais" tem conotação positiva isoladamente, mas o contexto é negativo. O TF-IDF não captura dependência entre palavras.
2. **Neutra classificada com polaridade (resto):** Frases factuais com palavras que em outros contextos são opinativas. Ex: "O roteiro de Pulp Fiction é conhecido por sua narrativa não linear" → "conhecido" e "não linear" confundem o modelo.

**Análise por fonte geradora (achado-chave):**
- ChatGPT: 9,9% de erro → frases mais curtas, polaridade mais explícita
- Claude: 14,1% → frases mais longas e elaboradas
- Gemini: 17,4% → vocabulário mais descritivo, fronteira tênue entre opinião e neutralidade

**Perguntas prováveis:**
- **"O que explica o ChatGPT ter menos erros?"** → "O ChatGPT tende a gerar frases mais curtas e diretas, com palavras-chave de sentimento mais explícitas. Isso facilita a classificação por modelos baseados em frequência de termos. O Gemini usa vocabulário mais variado e descritivo, o que dificulta."
- **"Como resolveria esses erros de negação?"** → "Modelos como BERT capturam dependências contextuais entre palavras, o que permitiria entender que 'muito ruins' inverte o sentido de 'efeitos especiais'. Isso é trabalho futuro."
- **"A análise de erros só foi feita no NB — por que não nos outros?"** → "O NB foi o modelo com melhor F1-Score e é o baseline do trabalho. Analisar os erros do melhor modelo é a abordagem mais informativa — se o melhor erra, os outros provavelmente erram nos mesmos casos e em mais."

---

### 9. Limitações — Saber admitir com segurança

**Limitações que você deve mencionar proativamente (mostra maturidade):**
1. **Dataset 100% sintético** — sem validação contra corpus real. Não é possível afirmar que o desempenho se manteria em produção.
2. **Tamanho moderado (1798 frases)** — suficiente para NB, mas LR e SVM se beneficiariam de mais dados.
3. **Sem controle de temperatura** — prompts enviados via interface web, sem controle de parâmetros de geração. Limita reprodutibilidade exata.
4. **Modelos lineares com TF-IDF** — não capturam dependências entre palavras (negação, ironia).
5. **Domínio específico** — críticas de filmes e séries. Resultados podem não generalizar para outros domínios (saúde, política, etc.).

**Como falar de limitações sem parecer fraco:** "Toda pesquisa tem escopo. Essas limitações não invalidam os resultados — elas definem os limites dentro dos quais as conclusões são válidas e apontam direções claras para trabalhos futuros."

---

### 10. Trabalhos Futuros — Respostas prontas

- **Validação com dados reais:** Testar os classificadores em corpus de reviews reais (IMDb, Letterboxd, AdoroCinema) sem retreinar, para medir o gap entre sintético e real.
- **BERTimbau:** Usar embeddings contextuais que capturam semântica e dependências, especialmente para tratar negação e ironia.
- **Mais dados e mais LLMs:** Ampliar o dataset e incluir outros geradores (Llama, Mistral) para aumentar diversidade.
- **Controle de geração:** Usar APIs com controle de temperatura para reprodutibilidade.

---

### 11. Perguntas Genéricas de Banca — Preparação

- **"Qual a contribuição do seu trabalho?"** → "Mostrar que dados sintéticos de múltiplos LLMs são viáveis para treinar classificadores de sentimento em português brasileiro, com F1 de até 89,63%, e que a escolha do LLM gerador impacta a qualidade do dataset."
- **"O que você faria diferente se começasse de novo?"** → "Incluiria desde o início uma etapa de validação com dados reais, e usaria as APIs dos LLMs ao invés das interfaces web para ter mais controle sobre os parâmetros de geração."
- **"Esse trabalho tem aplicação prática?"** → "Sim. Para qualquer empresa que precisa de um classificador de sentimento em português e não tem dados rotulados, a abordagem mostra que é possível gerar o dataset com LLMs e treinar um modelo funcional rapidamente, sem custo de anotação humana."
- **"Por que três classes e não duas (positivo/negativo)?"** → "Porque reviews reais frequentemente contêm frases neutras (sinopses, dados factuais). Um classificador binário forçaria essas frases em uma classe errada. Três classes representam melhor a realidade do domínio."

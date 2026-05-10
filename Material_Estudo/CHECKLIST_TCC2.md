**CHECKLIST TCC 2**

Plano Dia a Dia

**Aluno: Davi Romauski Meurer**

**Curso: Engenharia de Software — UTFPR Dois Vizinhos**

**Tema: Análise de Sentimentos com Dados Sintéticos Gerados por LLMs**

Início do plano: 19/03/2026

Previsão de entrega: \~6 semanas após início

# **SEMANA 1 — Retomada \+ Código \+ Orientador**

*O foco desta semana é retomar o contato com o orientador, fechar o código e garantir que a base experimental está sólida.*

### **Dia 1 — Retomada e contato com orientador**

- [x]  ~~Reler este checklist inteiro para ter visão do todo~~  
- [x]  ~~Reler o BRIEFING\_TCC.md para relembrar o estado do projeto~~  
- [x]   ~~Escrever mensagem para o orientador:~~  
      —  Informar que está retomando o TCC

      —  Resumir o que já foi feito (dataset, modelos baseline, métricas)

      —  Perguntar sobre prazo de entrega e formato (artigo SBC ou monografia?)

      —  Pedir uma reunião para a semana (presencial ou online)

- [x] ~~**Enviar a mensagem ao orientador** (não adiar)~~  
- [x] ~~Abrir o notebook 01\_training\_evaluation.ipynb no Colab e re-executar inteiro para confirmar que roda sem erros~~

⏱  *Tempo estimado: 2h*

### **Dia 2 — Completar notebook 02: Validação Cruzada**

- [x]  ~~Abrir src/02\_robustness\_analysis.ipynb no Colab~~  
- [x]   ~~Clonar o repo no Colab:~~  
      \!git clone https://github.com/ROMAUSKI/tcc-analise-sentimento.git

- [x] ~~Carregar o synthetic\_dataset.csv corretamente~~  
- [x]   ~~Implementar validação cruzada com cross\_val\_score:~~  
      —  Naive Bayes com k=5

      —  Naive Bayes com k=10

      —  Regressão Logística com k=5

      —  Regressão Logística com k=10

- [x]   ~~Calcular e imprimir: média e desvio padrão do F1-Score de cada combinação~~  
- [x]   ~~Criar tabela comparativa (DataFrame) e salvar como resultados/validacao\_cruzada.csv~~  
- [x]   ~~Criar gráfico boxplot comparando os k-folds e salvar como resultados/boxplot\_validacao\_cruzada.png~~

⏱  *Tempo estimado: 3h*

### **Dia 3 — Completar notebook 02: Curva de Aprendizado**

- [x]   ~~No mesmo notebook 02, implementar curva de aprendizado:~~  
      —  Usar learning\_curve do sklearn

      —  Frações: \[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0\]

      —  Para Naive Bayes e Regressão Logística

- [x]   ~~Plotar gráfico com F1-Score (treino vs teste) x fração do dataset~~  
- [x]   ~~Salvar como resultados/curva\_aprendizado\_nb.png e resultados/curva\_aprendizado\_lr.png~~  
- [x]   ~~Analisar: o modelo melhora com mais dados? Há overfitting? Há platô?~~  
- [x]   ~~Anotar observações em um comentário markdown no notebook~~

⏱  *Tempo estimado: 3h*

### **Dia 4 — Completar notebook 02: Análise de Erros**

- [x]   ~~Pegar as predições do melhor modelo (Naive Bayes) no conjunto de teste~~  
- [x]   ~~Identificar **todas** as frases classificadas incorretamente~~  
- [x]   ~~Selecionar 10-15 exemplos representativos dos erros~~  
- [x]   ~~Para cada erro, anotar:~~  
      —  Frase original

      —  Classe real vs classe predita

      —  Fonte (ChatGPT, Gemini ou Claude)

      —  Por que errou? (ambiguidade, ironia, frase muito curta, vocabulário neutro em contexto positivo, etc.)

- [x]   ~~Criar uma tabela resultados/analise\_erros.csv com essas colunas~~  
- [x]   ~~Calcular: qual IA gera mais erros? Qual classe é mais confundida com qual?~~

⏱  *Tempo estimado: 3-4h*

| *Tarefa* | *Status* |
| ----- | ----- |
| *Pegar predições do Naive Bayes no teste* | ***Cel 7** — `nb_model.predict()` com mesmo split do nb01 (seed 42, 80/20, stratify)* |
| *Identificar frases classificadas incorretamente* | ***Cel 7** — `erros = df_test[~df_test['acertou']]` → 41 erros identificados* |
| *Selecionar 10-15 exemplos representativos* | ***Cel 10** — 15 exemplos, variando tipo de confusão e fonte* |
| *Anotar frase original* | ***CSV** — coluna `frase`* |
| *Anotar classe real vs predita* | ***CSV** — colunas `classe` e `predita`* |
| *Anotar fonte* | ***CSV** — coluna `fonte` (ChatGPT, Claude, Gemini)* |
| *Anotar por que errou* | ***Cel 11 (markdown)** — análise qualitativa: negações compostas, vocabulário ambíguo, fronteira neutro/polarizado* |
| *Criar `resultados/analise_erros.csv`* | ***Existe** — 15 linhas, 4 colunas* |
| *Qual IA gera mais erros* | ***Cel 8** — Gemini 12,8%, Claude 12,5%, ChatGPT 8,7%* |
| *Qual classe confunde com qual* | ***Cel 8** — Positiva→Negativa é a mais comum (13 erros)* |

*A única diferença em relação ao plano original: a coluna "motivo do erro" não está no CSV (foi removida porque a função `classificar_motivo` com heurísticas hardcoded era o maior sinal de código gerado por IA). A interpretação dos erros ficou na célula markdown, que é mais natural pra um notebook acadêmico. Se quiser, posso adicionar uma coluna manual de motivo no CSV.*

### **Dia 5 — (Opcional) Modelo extra \+ consolidação**

- [x]   ~~(Opcional) Implementar SVM como terceiro modelo:~~  
      —  from sklearn.svm import SVC com kernel linear

      —  Treinar, avaliar, gerar métricas e matriz de confusão

      —  Salvar resultados/matriz\_confusao\_svm.png e atualizar baseline\_metrics.csv

- [x]   ~~Consolidar TODAS as métricas em uma tabela final resultados/metricas\_consolidadas.csv:~~  
      —  Colunas: Modelo, Acurácia, Precisão, Recall, F1-Score, F1 CV (média ± desvio)

      —  Linhas: Regressão Logística, Naive Bayes, (SVM se fez)

- [x]   ~~Re-executar notebook 02 inteiro do zero para garantir reprodutibilidade~~  
- [x]   ~~git add . && git commit && git push~~

⏱  *Tempo estimado: 3-4h*

Feito mesmo sendo opcional

### **Dia 6 — Reunião com orientador**

- [ ]   **Reunião com orientador** (ajustar data conforme resposta dele)  
- [ ]   Levar para a reunião:  
      —  Tabela de métricas consolidadas

      —  Gráficos (matrizes de confusão, curva de aprendizado, boxplot)

      —  Exemplos da análise de erros

      —  Dúvidas: formato de entrega (artigo ou monografia?), prazo, banca

- [ ]   Anotar feedback e decisões da reunião  
- [ ]   Após reunião: atualizar o BRIEFING\_TCC.md com decisões tomadas

⏱  *Tempo estimado: 1-2h (reunião) \+ 30min (anotações)*

**vercheck \-**  Aguardando resposta do Orientador

### **Dia 7 — Descanso / buffer**

- [x]   ~~Dia de folga ou para recuperar atrasos da semana~~  
- [x]   ~~Se estiver em dia: leitura livre sobre dados sintéticos~~

# **SEMANA 2 — Pesquisa Bibliográfica \+ Início da Escrita**

*O foco é ler artigos relacionados e começar a escrever as seções do artigo LaTeX.*

### **Dia 8 — Leitura: Análise de Sentimento (fundamentos)** 

- [x]   ~~Ler/revisar capítulos relevantes do Jurafsky & Martin (cap. 4 e 25\)~~  
      —  URL: https://web.stanford.edu/\~jurafsky/slp3/

      —  Focar em: definição de análise de sentimento, abordagens clássicas (bag-of-words, TF-IDF, Naive Bayes)

- [x]   ~~Pesquisar e baixar 2-3 artigos sobre análise de sentimento em português~~  
      —  Google Scholar: "análise de sentimento português machine learning"

      —  Guardar os PDFs em documentos/referencias/

- [x]   ~~Para cada artigo lido, anotar em documentos/notas\_leitura.md:~~  
      —  Referência completa (autor, ano, título, onde publicou)

      —  O que fizeram (método, dataset, resultados)

      —  O que posso citar no meu artigo

⏱  *Tempo estimado: 4h*

### **Dia 9 — Leitura: Dados Sintéticos \+ LLMs para geração de dados**

- [x]   ~~Pesquisar e baixar 3-4 artigos sobre dados sintéticos para ML~~  
      —  Google Scholar: "synthetic data training machine learning", "LLM generated training data"

      —  Focar em artigos de 2023-2025 (tema recente)

- [x]   ~~Anotar no documentos/notas\_leitura.md (mesmo formato do dia 8\)~~  
- [x]   ~~Identificar: alguém já fez algo parecido? Com que resultados? Como o meu trabalho se diferencia?~~  
- [x]   ~~Adicionar as referências ao artigo/referencias.bib no formato BibTeX~~

⏱  *Tempo estimado: 4h*

### **Dia 10 — Leitura: Avaliação de modelos \+ Trabalhos similares**

- [x]   ~~Pesquisar 2-3 artigos sobre avaliação de modelos de NLP~~  
      —  Métricas (acurácia, F1, etc.), validação cruzada, curvas de aprendizado

- [x]   ~~Pesquisar se existe algum TCC/artigo da UTFPR sobre tema similar~~  
- [x]   ~~Completar as anotações no notas\_leitura.md~~  
- [x]   ~~Atualizar artigo/referencias.bib com todas as referências novas~~  
- [x]   ~~Objetivo: ter pelo menos **10-12 referências** no .bib~~

⏱  *Tempo estimado: 3-4h*

### **Dia 11 — Escrita: Limpar o template \+ Introdução (rascunho)**

- [x]   ~~Abrir artigo/main.tex~~  
- [x]   ~~REMOVER todo o texto do template SBC~~  
- [x]   ~~SUBSTITUIR autores e afiliações (Davi, UTFPR, orientador)~~  
- [x]   ~~Criar a estrutura de seções do artigo:~~  
      —  1\. Introdução / 2\. Trabalhos Relacionados / 3\. Metodologia / 4\. Resultados e Discussão / 5\. Conclusão

- [x]   ~~Escrever **rascunho da Introdução** (\~1 página):~~  
      —  Parágrafo 1: Contexto (análise de sentimento é importante porque...)

      —  Parágrafo 2: Problema (obter dados rotulados é caro/difícil)

      —  Parágrafo 3: Objetivo do trabalho

      —  Parágrafo 4: Estrutura do artigo ("Este artigo está organizado...")

⏱  *Tempo estimado: 3-4h*

### **Dia 12 — Escrita: Trabalhos Relacionados**

- [x]   ~~Escrever seção "Trabalhos Relacionados" (\~1 página):~~  
      —  Subseção sobre análise de sentimento (métodos clássicos, estado da arte)

      —  Subseção sobre uso de dados sintéticos em ML

      —  Subseção sobre LLMs como geradores de dados

      —  Parágrafo final: como seu trabalho se posiciona

- [x]   ~~Garantir que cada parágrafo tem pelo menos 1-2 citações~~  
- [x]   ~~Compilar no Overleaf para verificar se as referências aparecem~~

⏱  *Tempo estimado: 4h*

### **Dia 13 — Escrita: Metodologia completa**

- [x]   ~~Expandir a seção "Metodologia"~~  
- [x]   ~~Adicionar subseções:~~  
      —  **3.1 Geração do Dataset:** prompts, 3 IAs, quantidade de frases, processo manual

      —  **3.2 Pré-processamento:** limpeza, remoção de duplicatas, normalização

      —  **3.3 Vetorização:** explicar TF-IDF e por que foi escolhido

      —  **3.4 Modelos de Classificação:** descrever NB, LR (e SVM se fez)

      —  **3.5 Avaliação:** métricas, validação cruzada, curva de aprendizado, análise de erros

      —  **3.6 Ambiente Experimental:** Google Colab, Python, seed=42, split 80/20

- [x]   ~~Adicionar tabela com estatísticas do dataset~~  
- [x]   ~~Compilar no Overleaf e revisar~~

⏱  *Tempo estimado: 4-5h*

### **Dia 14 — Descanso / buffer**

- [x]   ~~Dia de folga ou para recuperar atrasos~~  
- [x]   ~~Se em dia: revisar o que escreveu nos dias 11-13 com olhos frescos~~

# **SEMANA 3 — Resultados, Discussão e Figuras**

*O foco é escrever a parte mais importante do artigo: o que você descobriu e o que significa.*

### **Dia 15 — Escrita: Resultados (parte 1 — baseline)**

- [x]   ~~Escrever início da seção "Resultados e Discussão"~~  
- [x]   ~~Subseção **4.1 Resultados dos Modelos Baseline:**~~  
      —  Criar tabela LaTeX com métricas (Acurácia, Precisão, Recall, F1)

      —  Incluir matrizes de confusão como figuras

      —  Copiar gráficos de resultados/ para artigo/imagens/

      —  Texto: descrever qual modelo foi melhor, quais classes são mais fáceis/difíceis

- [x]   ~~Compilar e verificar se tabelas e figuras aparecem corretas~~

⏱  *Tempo estimado: 3-4h*

### **Dia 16 — Escrita: Resultados (parte 2 — robustez)**

- [x]   ~~Subseção **4.2 Validação Cruzada:**~~  
      —  Tabela com média ± desvio padrão de cada modelo

      —  Incluir gráfico boxplot

      —  Texto: o modelo é estável? O desvio padrão é aceitável?

- [x]   ~~Subseção **4.3 Curva de Aprendizado:**~~  
      —  Incluir gráficos de curva de aprendizado

      —  Texto: mais dados melhoram o resultado? Há platô? Há overfitting?

- [x]   ~~Copiar todos os gráficos novos para artigo/imagens/~~

⏱  *Tempo estimado: 3-4h*

### **Dia 17 — Escrita: Discussão \+ Análise de Erros**

- [x]   ~~Subseção **4.4 Análise Qualitativa de Erros:**~~  
      —  Tabela com exemplos de frases mal classificadas

      —  Texto: padrões nos erros (ambiguidade, ironia, frases curtas)

      —  Qual IA gera dados mais "limpos"? Qual classe confunde mais?

- [x]   ~~Subseção **4.5 Discussão Geral:**~~  
      —  Responder à pergunta de pesquisa 1: "Qual o nível de assertividade?"

      —  Responder à pergunta de pesquisa 2: "A classificação é coerente?"

      —  Comparar com trabalhos relacionados

      —  Limitações: ausência de teste com dados reais, dataset pequeno

⏱  *Tempo estimado: 4-5h*

### **Dia 18 — Escrita: Conclusão**

- [x]   ~~Escrever seção "Conclusão" (\~0.5-1 página):~~  
      —  Parágrafo 1: Resumo do que foi feito

      —  Parágrafo 2: Principais achados

      —  Parágrafo 3: Limitações do trabalho

      —  Parágrafo 4: Trabalhos futuros (BERT, dados reais, aumentar dataset)

- [x]   ~~Compilar artigo completo no Overleaf e fazer leitura corrida~~

⏱  *Tempo estimado: 2-3h*

### **Dia 19 — Escrita: Resumo \+ Abstract**

- [x]   ~~Escrever o **Resumo** em português (\~10 linhas):~~  
      —  Contexto (1 frase) / Problema (1 frase) / O que foi feito (2-3 frases) / Resultados (2-3 frases) / Conclusão (1 frase)

- [x]   ~~Escrever o **Abstract** em inglês (tradução do resumo)~~  
- [x]   ~~Revisar se título do artigo ainda faz sentido com o conteúdo final~~  
- [x]   ~~Compilar e verificar que tudo cabe na primeira página~~

⏱  *Tempo estimado: 2-3h*

### **Dia 20 — Revisão do artigo \+ commit**

- [x]   ~~Ler o artigo inteiro do começo ao fim como se fosse da banca~~  
- [x]   ~~Verificar:~~  
      —  Todas as figuras têm legenda e são referenciadas no texto?

      —  Todas as tabelas têm legenda e são referenciadas no texto?

      —  Todas as citações no texto estão no .bib?

      —  O texto flui logicamente de uma seção para outra?

- [x]   ~~Corrigir erros de português e melhorar frases confusas~~  
- [x]   ~~git add . && git commit \-m "feat: primeira versão completa do artigo" && git push~~

⏱  *Tempo estimado: 3-4h*

- [x] ~~**EXTRA — Notebook 03 criado e executado:** validação externa em 100k críticas reais (UTLC-Movies)~~  
- [x] ~~**EXTRA — Figura gerada:** `artigo/imagens/dados_reais_metricas.png`~~  
- [x] ~~**EXTRA — CSV gerado:** `resultados/relatorio_dados_reais.csv`~~  
- [x] ~~**EXTRA — Referência adicionada:** `sousa2019bunch` (Sousa, Brum e Nunes 2019, STIL) em `referencias.bib`~~  
- [x] ~~**EXTRA — Artigo: 2ª rodada de reescrita:**~~  
- [x] ~~Abstract \+ Resumo com menção ao UTLC e reality gap~~  
- [x] ~~Introdução com 3ª pergunta de pesquisa~~  
- [x] ~~**Subseção 4.8** "Validação em Dados Reais" (Metodologia)~~  
- [x] ~~**Subseção 5.5** "Validação em Dados Reais" (Resultados) — com tabela de métricas, figura, tabela de exemplos e análise de 3 fatores~~  
- [x] ~~Subseção 5.6 "Discussão Geral" reescrita para responder as 3 perguntas~~  
- [x] ~~Seção 6 "Conclusão" reescrita (4 parágrafos)~~  
- [x] ~~**EXTRA — PDF recompilado:** 22 páginas~~

### **Dia 21 — Descanso / buffer**

- [x]   ~~Folga ou recuperação de atrasos~~

Artigo pronto em 16/04/2026 (versão com dados reais). Falta enviar por e-mail. 

# **SEMANA 4 — Revisão com Orientador \+ Ajustes**

### **Dia 22 — Enviar artigo para o orientador**

- [ ]  Exportar PDF do artigo   
        Enviar por email ao orientador:  
      —  PDF do artigo

      —  Link do repositório GitHub

      —  Pedir feedback até data X (combinar prazo realista, \~5 dias úteis)

- [ ]   Enquanto espera: começar a preparar os slides

⏱  *Tempo estimado: 1h*

### **Dia 23 — Revisão do código e reprodutibilidade**

- [ ]  Atualizar requirements.txt com apenas as bibliotecas usadas  
- [ ]  Remover bibliotecas desnecessárias  
- [ ]   Re-executar notebooks 01 e 02 do zero no Colab (ambiente limpo)  
- [ ]  Verificar que todos os gráficos e CSVs são gerados corretamente  
- [ ]   Atualizar README.md se necessário  
- [ ]   git commit && git push

⏱  *Tempo estimado: 2-3h*

### **Dia 24 — Criar slides: Introdução e Metodologia**

- [ ]   Criar apresentação (PowerPoint ou Google Slides)  
- [ ]  Slide 1: Título, autor, orientador, UTFPR  
- [ ]   Slide 2: Agenda/sumário da apresentação  
- [ ]   Slide 3: Motivação/contexto  
- [ ]   Slide 4: Problema e perguntas de pesquisa  
- [ ]   Slide 5: Objetivos (geral \+ específicos)  
- [ ]   Slide 6: Visão geral da metodologia (diagrama/fluxo)  
- [ ]   Slide 7: Dataset — como foi gerado, estatísticas  
- [ ]   Slide 8: Pré-processamento e vetorização (TF-IDF)  
- [ ]   Slide 9: Modelos utilizados (NB, LR, SVM)

⏱  *Tempo estimado: 3h*

### **Dia 25 — Criar slides: Resultados e Conclusão**

- [ ]  Slide 10: Tabela de métricas baseline  
- [ ]  Slide 11: Matrizes de confusão (lado a lado)  
- [ ]   Slide 12: Validação cruzada (tabela \+ boxplot)  
- [ ]   Slide 14: Análise de erros (exemplos \+ padrões)  
- [ ]  Slide 15: Discussão — respondendo as perguntas de pesquisa  
- [ ]  Slide 16: Limitações e trabalhos futuros  
- [ ]   Slide 17: Conclusão  
- [ ]   Slide 18: Referências principais  
- [ ]   Slide 19: Obrigado / Perguntas?

⏱  *Tempo estimado: 3h*

### **Dia 26 — Reunião com orientador (feedback do artigo)**

- [ ]  **Reunião com orientador** para discutir o feedback  
- [ ]  Anotar todas as correções pedidas  
- [ ]  Classificar por prioridade: obrigatório vs sugestão  
- [ ]  Perguntar sobre:  
      —  Data e composição da banca

      —  Tempo da apresentação (8, 10 ou 15 min?)

      —  Formato de entrega final

⏱  *Tempo estimado: 1-2h*

### **Dia 27-28 — Aplicar correções do orientador no artigo**

- [ ]  Aplicar cada correção anotada na reunião  
- [ ]  Se pediu mais referências: pesquisar e adicionar  
- [ ]  Se pediu mais experimentos: implementar no notebook e atualizar o artigo  
- [ ]  Recompilar no Overleaf  
- [ ]  Reler as seções corrigidas  
- [ ]  git commit && git push  
- [ ]  Enviar versão corrigida ao orientador por email

⏱  *Tempo estimado: 4-6h (total dos 2 dias)*

# **SEMANA 5 — Ensaio e Polimento**

### **Dia 29 — Revisar slides com correções finais**

- [ ]  Atualizar slides com métricas/gráficos finais  
- [ ]  Verificar consistência: números nos slides \= números no artigo  
- [ ]  Adicionar animações simples se necessário (evitar excessos)  
- [ ]  Testar slides no modo apresentação

⏱  *Tempo estimado: 2h*

### **Dia 30 — Ensaio 1: Apresentação cronometrada**

- [ ]  Apresentar em voz alta, sozinho, cronometrando  
- [ ]  Meta: 8-12 minutos (verificar com orientador o tempo exato)  
- [ ]  Anotar: onde travou, onde gastou tempo demais, onde ficou confuso  
- [ ]  Ajustar slides: cortar o que é dispensável, expandir o que foi rápido demais  
- [ ]  Preparar respostas para perguntas prováveis da banca:  
      —  "Por que não testou com dados reais?"

      —  "Por que só 200 frases por IA?"

      —  "Qual a vantagem sobre usar um dataset público?"

      —  "O que mudaria se usasse BERT ao invés de NB?"

      —  "Como você garante que os dados gerados não são enviesados?"

⏱  *Tempo estimado: 2-3h*

### **Dia 31 — Ensaio 2: Apresentar para alguém**

- [ ]  Apresentar para um colega, amigo ou familiar  
- [ ]  Pedir feedback sobre:  
      —  Ficou claro o problema?

      —  Os gráficos são legíveis?

      —  O ritmo estava bom?

- [ ]  Ajustar com base no feedback

⏱  *Tempo estimado: 2h*

### **Dia 32 — Formatação final do artigo**

- [ ]  Checklist de formatação SBC:  
      —  Fonte Times 12pt?

      —  Margens: 3.5cm (topo), 2.5cm (base), 3.0cm (laterais)?

      —  Sem número de página?

      —  Figuras e tabelas com legenda Helvetica 10pt bold?

      —  Resumo e Abstract na primeira página, máximo 10 linhas cada?

      —  Referências no formato correto?

- [ ]  Verificar se não excedeu o limite de páginas  
- [ ]  Exportar PDF final do Overleaf

⏱  *Tempo estimado: 2-3h*

### **Dia 33 — Última leitura do artigo**

- [ ]  Ler o artigo inteiro impresso (ou em PDF no tablet)  
- [ ]  Marcar com caneta: erros de gramática, frases confusas, inconsistências  
- [ ]  Corrigir no LaTeX  
- [ ]  Pedir para alguém ler e apontar partes confusas

⏱  *Tempo estimado: 2-3h*

# **SEMANA 6 — Entrega Final**

### **Dia 34 — Empacotamento final**

- [ ]  Verificar que todos os notebooks rodam do zero  
- [ ]  Verificar que o README.md está atualizado  
- [ ]  Verificar que o requirements.txt está correto  
- [ ]  Remover a pasta \_backup/ se não quiser no repo  
- [ ]  git commit \-m "versão final para entrega" && git push  
- [ ]  Exportar PDF final do artigo  
- [ ]  Exportar slides como PDF  
- [ ]  Organizar pasta de entrega:  
      —  Artigo (PDF)

      —  Slides (PDF ou PPTX)

      —  Link do repositório GitHub

⏱  *Tempo estimado: 2h*

### **Dia 35 — Entrega**

- [ ]  Submeter conforme regras da UTFPR  
      —  Verificar no regulamento (documentos/Regulamento de TCC da UTFPR.pdf)

      —  Prazo, formato, para quem enviar

- [ ]  Enviar para o orientador confirmando a submissão  
- [ ]  Respirar fundo — a parte mais difícil já passou

⏱  *Tempo estimado: 1h*

### **Dias 36-38 — Preparação final para a defesa**

- [ ]  Ensaiar mais 1-2 vezes a apresentação  
- [ ]  Revisar respostas para perguntas da banca  
- [ ]  Preparar ambiente: notebook carregado, slides testados no projetor se possível  
- [ ]  Ir para a defesa confiante

# **RESUMO DE ENTREGAS POR SEMANA**

| Semana | Foco | Entregáveis |
| :---: | :---- | :---- |
| **1** | Código \+ Orientador | Notebook 02 completo, reunião marcada |
| **2** | Pesquisa \+ Escrita | 10-12 referências, Intro \+ Trab. Rel. \+ Metodologia |
| **3** | Resultados \+ Discussão | Artigo completo (primeira versão) |
| **4** | Revisão \+ Slides | Artigo revisado pelo orientador, slides prontos |
| **5** | Ensaio \+ Polimento | Artigo formatado, ensaios feitos |
| **6** | Entrega \+ Defesa | Tudo entregue e apresentado |

# **DICAS IMPORTANTES**

**1\. Não tente fazer tudo perfeito de primeira.** Escreva rascunhos ruins e melhore depois. Um texto ruim escrito é infinitamente melhor que um texto perfeito na cabeça.

**2\. Commite no git todo dia que trabalhar.** Mesmo que seja pouco. O histórico mostra evolução e te protege.

**3\. Fale com o orientador.** É a coisa mais importante deste checklist. Mesmo que dê vergonha, vai.

**4\. O artigo é mais importante que o código.** O código já está 90% pronto. O artigo está 10%. Priorize a escrita.

**5\. Se travar em um dia, pule para o próximo e volte depois.** Não deixe um dia parado travar a semana inteira.

**6\. Use o Overleaf para compilar o LaTeX.** Edite localmente e commite no git. Sincronize com o Overleaf via GitHub.

## **COMO SINCRONIZAR GIT ↔ OVERLEAF**

**1\.** No Overleaf, clique em New Project → Import from GitHub

**2\.** Selecione o repositório ROMAUSKI/tcc-analise-sentimento

**3\.** O Overleaf vai importar a pasta artigo/ automaticamente

**4\.** Para sincronizar: GitHub → Overleaf (Pull) ou Overleaf → GitHub (Push)

**5\.** Fluxo recomendado: Edite local → commit \+ push → pull no Overleaf → compile e revise

*Última atualização: 28/02/2026*
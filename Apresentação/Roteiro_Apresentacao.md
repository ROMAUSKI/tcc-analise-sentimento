# Notas de fixação — Apresentação TCC (flashcards)

> Bater o olho e lembrar. Não é roteiro de leitura.

## Slide 1 — Utilização de LLMs para Geração de Bases de Treinamento em Classificação de Sentimento: Uma Análise de Viabilidade Prática

ABERTURA — nome, orientador (Prof. Marlon), tema.
Pitch (1 frase): testar se LLMs servem pra gerar base de treino JÁ ROTULADA pra análise de sentimento em pt-BR — e se funciona em reviews reais.
Respirar, olhar a banca, não correr.

## Slide 2 — Sumário

Roteiro da fala: Contexto → Método → Resultados → Conclusão.
Só situar a banca; NÃO ler item por item.

## Slide 3 — Introdução

Análise de sentimento = classificar opinião em positiva / negativa / neutra.
• Treinar exige base rotulada: cara e lenta; pt-BR tem pouco.
• Ideia: o LLM gera o dado JÁ rotulado.
Pergunta central (pipeline): gera → treina → testa no REAL → funciona?

## Slide 4 — Objetivos

Geral: avaliar a viabilidade prática de treinar com dados sintéticos.
3 perguntas: (1) assertividade do sintético; (2) coerência ENTRE os LLMs; (3) cross-domain = treino sintético, teste real.
A 3ª (cross-domain) é a estrela — foi sugestão do Marlon.

## Slide 5 — Justificativa

Por que importa: anotação humana é cara/lenta; pt-BR escasso.
• LLM rotula sem anotação manual.
• 3 LLMs reduzem viés de fonte única.
• 2 nichos + cross-domain mostram ONDE funciona.

## Slide 6 — Referencial Teórico

Base teórica: análise de sentimento = classificação supervisionada (Pang, 2002).
• Clássicos: TF-IDF + NB / LR / SVM.
• Neurais: LSTM e BERTimbau (BERT pré-treinado em pt-BR).
• Métrica: F1-macro (justo com classes desbalanceadas).

## Slide 7 — Materiais

O que usei: 3 LLMs geradores, 5 classificadores, 2 datasets reais (UTLC-Movies/Apps, via kagglehub).
Stack: Python, scikit-learn, PyTorch, HuggingFace. Neurais rodaram no Colab (GPU T4).

## Slide 8 — Métodos (1/4): Geração e Dados

NÚMERO-CHAVE: 200 frases POR LLM por classe → 3 LLMs = 600/classe → 1.800/nicho.
• 2 nichos (filmes/séries e apps).
• Real: ~100k reviews/nicho; nota 1-5 → 3 classes (≥4 pos, ≤2 neg, =3 neu).
Pipeline: geração → pré-proc (TF-IDF) → treino → avaliação.

## Slide 9 — Métodos (2/4): Prompts

Prompt ISOMORFO: mesmo pros 3 LLMs, só muda a classe (comparação justa).
• Pede 200 frases, máx. 30 palavras, saída em CSV.
• CSV: frase | classe | fonte (qual LLM gerou).
LEMBRAR: o '200' é POR LLM → 3×200 = 600 por classe.

## Slide 10 — Métodos (3/4): Estilo de Cada LLM

Estilo de geração (comprimento): ChatGPT ~50 (curto/regular); Claude ~95 em filmes (longo); Gemini ~60.
• Em apps (texto técnico) os 3 se aproximam.
Por que importa: frase longa/elaborada se afasta da review real → ajuda a explicar o gap e a diferença entre nichos.

## Slide 11 — Métodos (4/4): Avaliação

5 visões = FONTE do treino (sint/real) × TESTE (controlado/natural).
• V1 = baseline sintético; V5 = cross-domain realista (a que importa).
• Pares: V2 vs V3 e V4 vs V5 isolam a fonte; V1 vs V5 = reality gap.
Métrica principal: F1-macro.

## Slide 12 — Resultados (1/4): Domínio Sintético e Real

V1 (sint→sint) = 97% com BERTimbau — sintético é ótimo 'em casa'.
Real (V2/V4) = 60-67% — patamar normal da tarefa.
ARMADILHA: 97% NÃO significa sucesso; é só dentro do mundo sintético.

## Slide 13 — Resultados (2/4): Cross-domain — a Queda

V5 (sint→real natural) DESPENCA: 43% filmes / 56% apps → inviável pra uso prático.
• Matriz (V3-SVM): a classe Neutra é a mais sacrificada.
Mensagem: o modelo treinado em sintético NÃO generaliza pro real.

## Slide 14 — Resultados (3/4): Reality Gap

Por que cai: frase sintética é limpa e direta; review real tem gíria, erro, ironia.
• Exemplos reais: 'PQP q filme', 'interesante', 'mais' (em vez de mas).
Causa = diferença de DISTRIBUIÇÃO entre os textos.

## Slide 15 — Resultados (4/4): Volume e Nichos

Teste de volume: triplicar o sintético (600 → 1.800 no nicho) NÃO fecha o gap em V3.
• Logo: limitação é ESTRUTURAL, não falta de dados (argumento central!).
• Apps > filmes no desbalanceado (vocabulário mais objetivo).
Legenda: Reduzido = 600/nicho; Completo = 1.800/nicho. Redução = amostra aleatória por classe (seed 42).

## Slide 16 — Conclusão (1/3): Objetivo Atendido

Objetivo ATENDIDO: avaliamos a viabilidade.
• 97% no sintético, MAS 43-56% no cross-domain real → inviável pra produção.
• Limitação é estrutural (distribuição), não falta de dados.

## Slide 17 — Conclusão (2/3): Dificuldades e Limitações

• Geração manual: ~3-4h por nicho (interface web).
• BERT estourou a RAM do Colab → subamostra estratificada de 100k (distribuição preservada).
• Paradoxo: calibrar o sintético exige dado real.
• TF-IDF não pega negação/ironia → por isso testei LSTM e BERT.

## Slide 18 — Conclusão (3/3): Trabalhos Futuros

• Adaptação de domínio (pouco real + muito sintético).
• Outros nichos; prompts mais elaborados.
• Gerar via API (controle de temperatura) e mais LLMs.

## Slide 19 — Referências

Citar de passagem; não ler.
Principais: Pang 2002 (base); Souza 2022 (sentimento pt-BR); Li 2023 / Hellwig 2025 (LLM gerando dado sintético).

## Slide 20 — Obrigado pela atenção!

Agradecer e abrir pra perguntas.
Mensagem final (1 frase): dado sintético de LLM serve pra protótipo/pesquisa, mas ainda NÃO substitui dado real em produção.


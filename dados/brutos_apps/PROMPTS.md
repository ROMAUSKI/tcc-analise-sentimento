# Prompts para geração dos 9 CSVs sintéticos — Nicho APPS

Mesmo padrão dos prompts de Movies (em `dados/brutos/metadata.csv`), só trocando "filmes e séries" → "aplicativos móveis" e "espectador" → "usuário".

**Use os 3 prompts abaixo nas interfaces web do ChatGPT, Gemini e Claude (3 LLMs × 3 classes = 9 arquivos).**

---

## 📋 Prompt 1 — POSITIVAS

```
Escreva 200 frases positivas avaliando aplicativos móveis. Cada frase deve expressar elogios ou satisfação do usuário. Use no máximo 30 palavras por frase. Liste apenas as frases em formato CSV, sem cabeçalho, com cada frase entre aspas.
```

## 📋 Prompt 2 — NEGATIVAS

```
Escreva 200 frases negativas avaliando aplicativos móveis. Cada frase deve expressar críticas ou insatisfação do usuário. Use no máximo 30 palavras por frase. Liste apenas as frases em formato CSV, sem cabeçalho, com cada frase entre aspas.
```

## 📋 Prompt 3 — NEUTRAS

```
Escreva 200 frases neutras sobre aplicativos móveis. Cada frase deve apresentar informações objetivas ou descrições factuais, sem expressar opinião. Use no máximo 30 palavras por frase. Liste apenas as frases em formato CSV, sem cabeçalho, com cada frase entre aspas.
```

---

## 🗃️ Como salvar os arquivos

Salve os 9 arquivos nesta pasta (`dados/brutos_apps/`) com **exatamente** estes nomes:

| LLM | Classe | Arquivo |
|---|---|---|
| ChatGPT | Positiva | `positive_gpt_01.csv` |
| ChatGPT | Negativa | `negative_gpt_01.csv` |
| ChatGPT | Neutra   | `neutral_gpt_01.csv` |
| Gemini  | Positiva | `positive_gemini_01.csv` |
| Gemini  | Negativa | `negative_gemini_01.csv` |
| Gemini  | Neutra   | `neutral_gemini_01.csv` |
| Claude  | Positiva | `positive_claude_01.csv` |
| Claude  | Negativa | `negative_claude_01.csv` |
| Claude  | Neutra   | `neutral_claude_01.csv` |

**Importante:** mesmo padrão de nomenclatura de Movies (`dados/brutos/`), só muda a pasta. Os notebooks que vou criar (05-08) detectam pelo nome do arquivo: `positive`/`negative`/`neutral` → classe; `gpt`/`gemini`/`claude` → fonte.

## 📝 Formato esperado do CSV

Sem cabeçalho, uma frase por linha entre aspas:

```
"O app é prático e atende todas as minhas necessidades."
"Interface limpa e funcionalidades bem pensadas."
"Excelente desempenho e atualizações frequentes."
...
```

## ✅ Checklist depois de gerar

- [ ] 9 arquivos salvos em `dados/brutos_apps/`
- [ ] Cada arquivo tem ~200 linhas
- [ ] Encoding UTF-8 (padrão do download das interfaces web)
- [ ] Atualizar `dados/brutos_apps/metadata.csv` (modelo abaixo)
- [ ] Commit + push pra eu pegar e processar

## 📊 Template do metadata.csv (preencher conforme for gerando)

```csv
id_lote,prompt,ferramenta_ia,versao_ia,classe,data_geracao,arquivo_saida
pos_01,"Escreva 200 frases positivas avaliando aplicativos móveis. Cada frase deve expressar elogios ou satisfação do usuário. Use no máximo 30 palavras por frase. Liste apenas as frases em formato CSV, sem cabeçalho, com cada frase entre aspas.",ChatGPT,VERSAO,Positiva,YYYY-MM-DD,positive_gpt_01.csv
neg_01,"Escreva 200 frases negativas avaliando aplicativos móveis. Cada frase deve expressar críticas ou insatisfação do usuário. Use no máximo 30 palavras por frase. Liste apenas as frases em formato CSV, sem cabeçalho, com cada frase entre aspas.",ChatGPT,VERSAO,Negativa,YYYY-MM-DD,negative_gpt_01.csv
neu_01,"Escreva 200 frases neutras sobre aplicativos móveis. Cada frase deve apresentar informações objetivas ou descrições factuais, sem expressar opinião. Use no máximo 30 palavras por frase. Liste apenas as frases em formato CSV, sem cabeçalho, com cada frase entre aspas.",ChatGPT,VERSAO,Neutra,YYYY-MM-DD,neutral_gpt_01.csv
pos_01,"Escreva 200 frases positivas avaliando aplicativos móveis. Cada frase deve expressar elogios ou satisfação do usuário. Use no máximo 30 palavras por frase. Liste apenas as frases em formato CSV, sem cabeçalho, com cada frase entre aspas.",Gemini,VERSAO,Positiva,YYYY-MM-DD,positive_gemini_01.csv
neg_01,"Escreva 200 frases negativas avaliando aplicativos móveis. Cada frase deve expressar críticas ou insatisfação do usuário. Use no máximo 30 palavras por frase. Liste apenas as frases em formato CSV, sem cabeçalho, com cada frase entre aspas.",Gemini,VERSAO,Negativa,YYYY-MM-DD,negative_gemini_01.csv
neu_01,"Escreva 200 frases neutras sobre aplicativos móveis. Cada frase deve apresentar informações objetivas ou descrições factuais, sem expressar opinião. Use no máximo 30 palavras por frase. Liste apenas as frases em formato CSV, sem cabeçalho, com cada frase entre aspas.",Gemini,VERSAO,Neutra,YYYY-MM-DD,neutral_gemini_01.csv
pos_01,"Escreva 200 frases positivas avaliando aplicativos móveis. Cada frase deve expressar elogios ou satisfação do usuário. Use no máximo 30 palavras por frase. Liste apenas as frases em formato CSV, sem cabeçalho, com cada frase entre aspas.",Claude,VERSAO,Positiva,YYYY-MM-DD,positive_claude_01.csv
neg_01,"Escreva 200 frases negativas avaliando aplicativos móveis. Cada frase deve expressar críticas ou insatisfação do usuário. Use no máximo 30 palavras por frase. Liste apenas as frases em formato CSV, sem cabeçalho, com cada frase entre aspas.",Claude,VERSAO,Negativa,YYYY-MM-DD,negative_claude_01.csv
neu_01,"Escreva 200 frases neutras sobre aplicativos móveis. Cada frase deve apresentar informações objetivas ou descrições factuais, sem expressar opinião. Use no máximo 30 palavras por frase. Liste apenas as frases em formato CSV, sem cabeçalho, com cada frase entre aspas.",Claude,VERSAO,Neutra,YYYY-MM-DD,neutral_claude_01.csv
```

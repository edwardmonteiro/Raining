# Packs Raining v1

ZIP UTF-8 com `episode.json` na raiz e imagens em `art/`. Referência completa: `app/src/main/assets/episode.json`.

Campos obrigatórios: `schemaVersion:1`, `id` único (minúsculas, números e hífen, até 60), `version`, `episode`, `title`, `cardCount`, `start`, `cover`, `cards`. Campos de apresentação: `series`, `subtitle`, `minutes`, `nextTitle`, `endingTitle`.

Cada card: `id`, `step` (1 até cardCount), `image`, `speaker`, `text` e exatamente uma forma de continuação: `next`, `choices` ou `ending:true`.

Uma escolha tem `label`, `next`, `memory`. `key` e `value` ficam preservados no progresso, reservados para continuidade entre capítulos. A versão atual adapta cenas através de ramificações `next`, sem interpretação de código e sem avaliação de expressões.

O progresso e as lembranças são isolados por ID do episódio. IDs instalados não são sobrescritos, para preservar a leitura. Limites: 150 entradas ZIP, 40 MB extraídos, 8 MB por arquivo, JSON 200 KB, imagens de até 2400 px por dimensão, no máximo 150 cards e 100 posições, 2–4 opções por decisão. Caminhos absolutos, travessia de diretórios, duplicatas, ciclos e referências ausentes são rejeitados. Importação usa diretório temporário e só disponibiliza o episódio após validação.

Não há código executável, HTML ou links nos cards. Não há download remoto. Não há assinatura de autoria nesta primeira versão: a validação estrutural protege o leitor, mas não atesta quem produziu a história.

Exemplo de criação, executado na pasta contendo episode.json e art/:

```sh
zip -r episodio-02.raining episode.json art/
```

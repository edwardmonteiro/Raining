# Episódio 3 · O retrato que faltava

Continuação original de **Quando a chuva passar**. O comprovante encontrado no episódio 2 leva Hana e Jiho ao laboratório fotográfico.

18 cards por leitura, duas decisões, quatro percursos possíveis, 20 ilustrações distintas. Cada nó narrativo referencia sua própria imagem. As duas consequências de cada decisão têm ilustrações próprias. Nenhuma imagem de card é reutilizada entre cards. A capa de navegação usa a chegada ao laboratório, para não antecipar a revelação.

## Importar

Raining 0.1.0 → **Episódios → Importar pack de episódio** → selecionar `Raining-Episodio-03-O-retrato-que-faltava.zip`, sem extrair. Não é necessário reinstalar o APK. Progresso e escolhas são separados por episódio. Não existe transferência automática de variáveis entre capítulos nesta versão do leitor.

## Produção

Fonte editorial: `scripts/write_episode3.py`. Depois de editar: executar `python3 scripts/write_episode3.py` e `python3 scripts/build_episode3.py`.

O empacotador valida todas as quatro rotas, referências, limites, contagem de passos, cobertura de todos os nós e unicidade dos arquivos de imagem por caminho e SHA-256. ZIP reproduzível em `dist/`, apenas JSON e imagens. O teste Android importa o arquivo pelo seletor do sistema e percorre duas rotas complementares, cobrindo todos os 20 cards ilustrados.

Ilustrações originais geradas com a ferramenta integrada de imagens. Personagens de referência: Hana e Jiho do episódio 1. O avental floral retoma o objeto mostrado na mesa do episódio 1. `art-prompts.json` registra as instruções de cada cena. Arquivos finais em `art/` foram redimensionados e codificados em JPEG para distribuição móvel. Sem assets de anime ou dorama de terceiros.

## Continuidade (spoilers)

- O filme estava revelado havia quatro meses. Seoyeon morreu três meses antes do retorno de Hana.
- Senhor Park guardou as duas cópias de cada fotografia; a mãe queria dar uma seleção à filha.
- A última fotografia mostra Seoyeon rindo ao lado do notebook com Hana numa chamada de vídeo.
- Jiho ajudou a apoiar a câmera e configurar o temporizador. Saiu antes da fotografia e não conhecia seu resultado.
- A descoberta não substitui o retrato presencial que mãe e filha não chegaram a fazer. Hana cola a cópia na página anterior, preservando o espaço vazio.
- Hana veste o avental floral da mãe e cogita cozinhar; ainda não decidiu vender nem reabrir o restaurante.
- Uma menina de cerca de dez anos, capa amarela e marmita vazia, entra para devolver o recipiente da avó. Nomes da menina e da avó ainda não foram revelados.
- Próximo capítulo: **Uma mesa a mais**. A pergunta sobre abrir amanhã permanece sem resposta.

# Raining

**Quando a chuva passar** — um dorama original para ler, sentir e escolher. Aplicativo Android nativo, em português, com cards ilustrados estáticos.

## Primeiro episódio: Uma mesa para dois

Hana volta à sua cidade para vender o restaurante da mãe. Uma mesa posta, um amigo de infância e uma carta interrompem seus planos.

18 cards por leitura, cinco ilustrações, duas escolhas e quatro percursos. Aproximadamente três minutos, sem limite de tempo. Lembranças, retorno ao card anterior, salvamento local e três tamanhos de texto. Sem rede, contas, anúncios ou coleta de dados.

O APK é disponibilizado como artifact `Raining-APK` nas [execuções de compilação](https://github.com/edwardmonteiro/Raining/actions).

## Desenvolvimento

Java 17 e Android SDK (platform 35, build-tools 35.0.0). Sem Gradle ou dependências externas em tempo de execução.

```sh
export ANDROID_HOME=/caminho/do/android-sdk
bash scripts/build.sh
```

A saída é `dist/Raining-v0.1.0.apk`. O GitHub Actions compila, verifica os quatro caminhos do roteiro, instala em emulador Android 15, percorre as quatro combinações, verifica retomada após encerramento do processo e leitura com fonte grande em tela pequena. Capturas ficam nos artifacts da execução.

Cada execução gera uma chave temporária de teste, que não é publicada nem incluída nos artifacts. Builds diferentes podem exigir desinstalação, com perda de progresso. Antes de uma distribuição contínua, configurar uma chave de produção em armazenamento privado. O aplicativo de distribuição não habilita depuração.

## Packs de conteúdo

Acesse Episódios → Importar pack. Selecione um ZIP com extensão `.raining` ou `.zip` que contenha `episode.json` e `art/*.jpg`, `*.png` ou `*.webp`. Consulte [PACK_FORMAT.md](PACK_FORMAT.md). Os packs contêm somente dados e imagens, nunca código. Importação manual, sem catálogo remoto nesta versão.

## Arte e história

História original: Raining. Ilustrações geradas com o recurso integrado de geração de imagens, em cinco cenas coerentes de anime pintado. Nenhum personagem, imagem ou diálogo de séries existentes foi usado. Prompts e proveniência em [ART_DIRECTION.md](ART_DIRECTION.md). Os arquivos finais estão em `app/src/main/assets/art/`.

## Limites do piloto

Primeiro episódio apenas; capítulo 2 ainda não publicado. Sem dublagem, música, nuvem, download automático ou assinatura digital de packs. A verificação de packs é estrutural, não prova de autoria; importe apenas arquivos de fonte conhecida. APK de desenvolvimento, não publicação em loja. Dados permanecem no aparelho e são apagados ao desinstalar.

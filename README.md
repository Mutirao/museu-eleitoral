# Museu Eleitoral

A memória pública do discurso de campanha. O Museu guarda o que candidatas e candidatos publicam nos canais que declararam ao TSE, com data, link para o original e um identificador criptográfico (CID) de cada registro. Qualquer pessoa consulta, confere e cobra depois da eleição.

Protótipo apresentado em hackathon (setembro de 2026). No ar em **https://museu.eleitoral.org.br**.

## O que o protótipo mostra

- **Página do candidato**, com dados reais de Jones Manoel (PSOL, PE) e Nikolas Ferreira (PL, MG), coletados de 18 a 25/09/2026: ficha oficial do TSE, canais declarados, linha do tempo dos posts e trechos classificados em propostas, compromissos, críticas e propostas de fiscalização.
- **Trecho no original**: cada trecho abre o post ou vídeo de origem, com transcrição automática (YouTube) e CID.
- **Simulações dentro do DivulgaCandContas** (`memoria-da-campanha.html` e `conteudo-digital-oficial.html`): como a funcionalidade ficaria na ficha oficial do TSE.
- Telas ilustrativas de verificação de prints, transparência e campanhas anteriores.

## Estrutura

```
prototipo/          fontes das três páginas (formato .dc.html) e o runtime support.js
coleta/             scripts de coleta e normalização
  dados/brutos/     o que foi coletado: Instagram, X, feed do YouTube, legendas automáticas
  dados/            dados curados: candidatos.json, classificacao.json, tse-fichas.json
scripts/            geradores do site a partir das fontes e dos dados
apresentacao/       deck do pitch
docs/referencias/   capturas de tela de referência
build.sh            gera o site em dist/ (e publica, com `./build.sh deploy`)
wrangler.jsonc      configuração do Cloudflare Workers (serve dist/)
```

`dist/` e `coleta/dados/gerados/` não entram no repositório: o `build.sh` recria os dois.

## Gerar e publicar

Precisa só de Python 3 (biblioteca padrão).

```bash
./build.sh           # gera dist/
./build.sh deploy    # gera e publica no Cloudflare (npx wrangler deploy)
```

O pipeline roda nesta ordem:

1. `coleta/legendas.py`: converte as legendas automáticas do YouTube em trechos com marcação de tempo.
2. `coleta/norm.py`: junta Instagram, X e YouTube em um só formato, aplica o recorte de datas (`START`) e calcula o CID v1 (sha2-256) de cada registro.
3. `coleta/prep.py`: cruza os itens com `classificacao.json` e `candidatos.json`.
4. `scripts/build_proto.py` e `scripts/build_pages.py`: geram as páginas em `dist/`.

## Coletar de novo

A coleta usa o [opencli](https://github.com/jackwener/opencli) com a extensão Browser Bridge no Chromium, logado no Instagram e no X, e o `yt-dlp` para as legendas.

```bash
opencli twitter tweets jonesmanoel_pe --limit 15 -f json > coleta/dados/brutos/x-jonesmanoel_pe.json
opencli twitter tweets nikolas_dm --limit 15 -f json > coleta/dados/brutos/x-nikolas_dm.json
python3 coleta/ig.py jones.manoel:12 nikolasferreiradm:12 nikolasferreirabr:4 oquenikolasfez:4
curl -s "https://www.youtube.com/feeds/videos.xml?channel_id=UCxI9vN6UbxmBt8VIvUKtJaA" > coleta/dados/brutos/rss-UCxI9vN6UbxmBt8VIvUKtJaA.xml
yt-dlp --skip-download --write-auto-subs --sub-langs pt-orig --sub-format json3 \
  -o "coleta/dados/brutos/legendas/%(id)s.%(ext)s" "https://www.youtube.com/watch?v=<id>"
```

Depois de coletar o X, rode `python3 coleta/separar_terceiros.py`: ele move repostagens e tweets citados de outras pessoas para `coleta/dados/privado/`, fora do git.

Para ampliar o período, mude `START` em `coleta/norm.py`. Depois de coletar, revise `classificacao.json` e rode `./build.sh`.

## Critérios

- **Só canais declarados ao TSE.** A lista de cada candidato vem do DivulgaCandContas. Canais não declarados ficam fora, mesmo quando existem.
- **O que não foi coletado aparece na página, com o motivo**: TikTok (o opencli falhou), Facebook (o opencli não lê posts de páginas), WhatsApp, Telegram, Kwai e sites (sem adaptador).
- **Classificação**: cada trecho é uma citação literal e segue o mesmo critério para todos os candidatos (ver `_criterio` em `classificacao.json`). A classificação deste protótipo não passou por revisão humana, e a página diz isso.
- **Nenhuma avaliação de cumprimento.** A aba de compromissos do mandato mostra os compromissos reais como "Sem avaliação". Organizações parceiras avaliam depois da posse.
- **Conteúdo de terceiros fica fora do repositório.** Repostagens e tweets citados de outras pessoas ficam em `coleta/dados/privado/`. Quando essa pasta existe, o build junta tudo e o site mostra as repostagens dos candidatos. Num clone do repositório, o site sai sem elas.
- **Dados pessoais**: `tse-fichas.json` guarda só os campos que o site usa. CPF, título de eleitor, e-mails e bens ficam fora do repositório. Nas simulações do DivulgaCandContas o CPF aparece mascarado.

## Direito autoral

Um post em rede social continua protegido por direito autoral. A Lei 9.610/98 garante os direitos ao autor desde a criação, e publicar não coloca o conteúdo em domínio público. Os termos de uso licenciam o conteúdo à plataforma, não a terceiros. Em material de campanha, os direitos costumam ser da campanha, do partido ou da produtora, e um vídeo pode trazer músicas e imagens de outras pessoas.

O Museu se apoia no que a lei não protege ou permite usar:

- **Fatos e metadados.** Ideias e informações não têm direito autoral (art. 8º). Data, canal, métricas públicas, link e CID de cada post são fatos sobre a publicação.
- **Citação.** A lei permite citar trechos de qualquer obra para estudo, crítica ou polêmica, na medida necessária, com o nome do autor e a origem (art. 46, III). Os trechos em "Contribuições por tipo" são citações literais, cada uma com autor, canal, data e link para o original.
- **O original fica na plataforma.** O site aponta para o post de origem, e os vídeos tocam no player do YouTube, que só carrega quando a pessoa clica.

Os cuidados que já tomamos:

- Coletamos só canais que os próprios candidatos declararam ao TSE como canais de campanha.
- Repostagens e tweets citados de outras pessoas ficam em `coleta/dados/privado/`, fora do repositório.
- O conteúdo coletado fica fora da licença AGPL do projeto (veja "Licença").
- CPF, título de eleitor, e-mails e bens dos candidatos ficam fora do repositório.

O que ainda está em aberto: `coleta/dados/brutos/` guarda o texto integral dos posts dos candidatos e as legendas automáticas completas dos vídeos. Essa cópia integral vai além da citação e serve como registro para conferir os CIDs. Antes de ampliar a coleta, pretendemos ouvir especialistas em direito digital e avaliar se essa cópia deve ficar só no arquivo privado. No nosso entendimento, um arquivo integral e permanente do discurso de campanha tem base mais sólida quando é mantido pelo TSE, como parte da fiscalização eleitoral e do arquivo público oficial. Essa é uma das razões da proposta.

Se você é autor ou titular de algum conteúdo deste repositório e quer que ele seja retirado, abra uma issue ou fale com o time. Tiramos o conteúdo do repositório e registramos a remoção.

## Time

Uirá Porã, Jader Gama, Yasodara Córdova e Lucas Pirola.

## Licença

O código e as páginas do Museu Eleitoral são software livre, sob a [GNU Affero General Public License v3.0](LICENSE) (AGPL-3.0). Se você rodar uma versão modificada como serviço na rede, precisa oferecer o código-fonte dessa versão a quem a usa.

Ficam fora da AGPL:

- `prototipo/support.js`, runtime da ferramenta de design em que as páginas foram feitas, que pertence aos seus autores.
- O conteúdo em `coleta/dados/brutos/` (posts, vídeos, legendas e métricas), que pertence a quem publicou e está aqui como registro de interesse público.

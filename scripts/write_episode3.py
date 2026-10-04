"""Original episode 3. One distinct illustration per narrative node."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
cards=[]
def c(id,step,speaker,text,next=None,choices=None,ending=False,caption=None):
    d=dict(id=id,step=step,image='art/'+id+'.jpg',speaker=speaker,text=text)
    if next:d['next']=next
    if choices:d['choices']=choices
    if ending:d['ending']=True
    if caption:d['caption']=caption
    cards.append(d)
def o(label,next,memory):return dict(label=label,next=next,memory=memory)
c('receipt',1,'HANA','O comprovante ficou entre meus dedos até amassar.\n\nQuatro meses esperando numa gaveta. Três meses sem minha mãe.\n\nEm algum lugar, havia imagens dela que o mundo ainda não tinha me mostrado.','crossing',caption='Sexta-feira · depois da estação')
c('crossing',2,'JIHO','Jiho me esperou na esquina.\n\n“É perto?”\n\n“Duas ruas. Três, se você continuar andando para o lado errado.”\n\nEle virou meu guarda-chuva na direção da subida. Eu deixei.','shop')
c('shop',3,'HANA','O laboratório era estreito, entre uma sapataria e uma loja fechada.\n\nNa vitrine, bebês que já deviam ter filhos.\n\nEmpurrei a porta. O sino soou alto demais.','keeper')
c('keeper',4,'SENHOR PARK','O homem do balcão leu o comprovante e tirou os óculos.\n\n“Filha da Seoyeon?”\n\nAssenti. Ele abriu um arquivo de envelopes.\n\n“Eu guardei. Não sabia para quem ligar.”','envelope')
c('envelope',5,'O QUE VOCÊ PRECISA PRIMEIRO?','No envelope, reconheci a letra dela.\n\nMeu polegar parou debaixo da aba. Abrir significava encontrar alguma coisa. Também significava chegar à última foto.',choices=[o('“Como ela estava quando veio?”','last-visit','Você procurou uma lembrança da última visita de Seoyeon.'),o('Abrir o envelope com cuidado','opening','Você encontrou primeiro os pequenos detalhes das fotografias.')])
c('last-visit',6,'SENHOR PARK','“Reclamou que eu cobrava por foto tremida.”\n\nEle sorriu, sem esconder a tristeza.\n\n“Depois pediu duas cópias de todas. Uma para você escolher quando viesse.”\n\nPuxei a primeira fotografia.','crooked',caption='Quatro meses antes · a lembrança do senhor Park')
c('opening',6,'HANA','Abri pela lateral para não rasgar o nome.\n\nDuas cópias de cada foto. Nas primeiras, reconheci a cozinha, uma cortina nova, o canto do balcão.\n\nCoisas pequenas que tinham mudado enquanto eu estava longe.','crooked')
c('crooked',7,'HANA','Uma fotografia mostrava Jiho diante de uma panela soltando fumaça.\n\n“Você queimou arroz?”\n\n“A panela participou.”\n\nVirei a foto antes de rir alto. Ele tentou olhar por cima do meu ombro.','ordinary')
c('ordinary',8,'HANA','Depois vieram três vasos na janela. Um sapato molhado. Uma tangerina descascada de uma vez só.\n\nEu esperava um segredo. Minha mãe tinha fotografado uma sexta-feira qualquer.\n\nSenti saudade até da casca.','portrait')
c('portrait',9,'A FOTOGRAFIA','Na última imagem, ela estava sentada à mesa, rindo.\n\nAo lado, um notebook aberto. Na tela, meu rosto.\n\nA foto tinha ficado um pouco torta. Nós duas cabíamos nela.','recognition')
c('recognition',10,'HANA','Era nossa chamada de domingo. Eu usava fones e respondia mensagens do trabalho.\n\nLembrei de ter dito: “Mãe, fala. Estou ouvindo.”\n\nNão lembrava daquele sorriso.','timer')
c('timer',11,'JIHO','Jiho olhou a fotografia.\n\n“Ajudei a apoiar a câmera no balcão. Ela queria aprender o temporizador.”\n\nEle fez uma pausa.\n\n“Depois fui embora. Não sabia se tinha dado certo.”','tell')
c('tell',12,'O QUE VOCÊ CONSEGUE DIZER?','Passei a unha pela borda branca. Naquele domingo, eu tinha pressa. Agora, ficaria ali o tempo que fosse.\n\nJiho afastou os outros retratos para a foto não dobrar.',choices=[o('“Eu devia ter fechado o trabalho.”','regret','Jiho ficou ao seu lado enquanto você nomeava o arrependimento.'),o('“Lembrei do que fez ela rir.”','joke','Você recuperou uma conversa que ainda conseguia fazer você rir.')])
c('regret',13,'JIHO','“Devia. Eu queria que você tivesse conseguido.”\n\nEle não tentou corrigir minha lembrança.\n\nDepois apontou para o retrato.\n\n“E ela riu com você. Essa parte também aconteceu.”','holding')
c('joke',13,'HANA','“Eu disse que miojo contava como jantar.”\n\nJiho levantou uma sobrancelha.\n\n“Ela ameaçou vir morar comigo para fiscalizar a geladeira.”\n\nOlhei a foto de novo. Dessa vez, consegui ouvir a risada junto.','holding')
c('holding',14,'HANA','Pedi um envelope novo. Guardei as duas cópias sem separá-las.\n\nAquela imagem não devolvia o abraço que faltou.\n\nMas eu tinha uma coisa nova para lembrar, além da última vez no hospital.','homeward')
c('homeward',15,'HANA','Na volta, a chuva diminuiu. O envelope foi por dentro do casaco.\n\nJiho acompanhou meus passos, sem perguntar sobre o restaurante.\n\nDessa vez, fui eu quem encontrou a rua.','album')
c('album',16,'HANA','Colei uma cópia na página anterior àquela que minha mãe tinha reservado.\n\nDeixei o espaço vazio como estava.\n\nO retrato que não fizemos e o que eu acabara de encontrar podiam ficar no mesmo caderno.','apron')
c('apron',17,'HANA','Fechei o caderno. Peguei o avental da cadeira e amarrei na cintura. Ficou comprido.\n\nJiho parou à porta da cozinha.\n\n“Você vai cozinhar?”\n\n“Primeiro, vou descobrir o que ainda tem na geladeira.”','doorbell')
c('doorbell',18,'HANA','Antes que eu abrisse a geladeira, o sino da porta tocou.\n\nUma menina entrou segurando uma marmita vazia.\n\n“Minha avó pediu para devolver. Vocês vão abrir amanhã?”\n\nOlhei para Jiho. Depois, para a mesa.\n\n“Como é o nome dela?”',ending=True,caption='Uma pergunta tinha acabado de entrar pela porta.')
episode=dict(schemaVersion=1,id='o-retrato-que-faltava',version=1,episode=3,title='O retrato que faltava',series='Quando a chuva passar',subtitle='Há lembranças que ainda estão esperando para chegar.',minutes=3,cardCount=18,start='receipt',cover='art/shop.jpg',endingTitle='Hoje, uma lembrança\nencontrou você.',nextTitle='Uma mesa a mais',cards=cards)
path=ROOT/'episodes/03-o-retrato-que-faltava/episode.json';path.parent.mkdir(parents=True,exist_ok=True)
path.write_text(json.dumps(episode,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(path)

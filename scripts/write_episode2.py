"""Authoring source for the second original Raining episode (Portuguese)."""
import json
from pathlib import Path

cards=[]
def card(id,step,image,speaker,text,next=None,choices=None,ending=False,caption=None):
    c=dict(id=id,step=step,image='art/'+image+'.jpg',speaker=speaker,text=text)
    if next:c['next']=next
    if choices:c['choices']=choices
    if ending:c['ending']=True
    if caption:c['caption']=caption
    cards.append(c)
def choice(label,next,memory):return dict(label=label,next=next,memory=memory)

card('morning',1,'station','HANA','Na manhã seguinte, levei a fotografia à estação.\n\nA mala aos pés da minha mãe parecia pequena demais para uma vida inteira. Ou talvez ela não pretendesse levar tudo.','umbrella',caption='Sexta-feira · a estação à beira-mar')
card('umbrella',2,'bench','JIHO','Jiho me encontrou na plataforma.\n\n“Você esqueceu o guarda-chuva.”\n\n“E você atravessou a cidade por isso?”\n\n“Também precisava perder uma discussão com a senhora do chá.”','name')
card('name',3,'kiosk','EUN-SOOK','Atrás do balcão, uma mulher de cabelos grisalhos pegou a foto.\n\n“Seoyeon. Nesse dia, ela quase perdeu o trem procurando o pente.”\n\nFazia tanto tempo que eu só ouvia chamarem minha mãe de mãe.','dream')
card('dream',4,'kiosk','EUN-SOOK','“Sou Eun-sook. Nós duas crescemos aqui.”\n\nEla serviu o chá.\n\n“Sua mãe queria fotografar gente que ainda não conhecia. Dizia que toda pessoa tinha um rosto que só aparecia quando esquecia a câmera.”','question')
card('question',5,'station','O QUE VOCÊ QUER DESCOBRIR?','Olhei outra vez a jovem da fotografia.\n\nEu conhecia as mãos dela cortando legumes. Nunca as tinha imaginado segurando uma passagem.',choices=[choice('“Por que ela não foi embora?”','departure','Você descobriu que a história dela continuava depois da fotografia.'),choice('“Foi a senhora que tirou essa foto?”','photographer','Você ouviu a lembrança de quem acompanhou a partida.')])
card('departure',6,'kiosk','EUN-SOOK','Eun-sook ergueu uma sobrancelha.\n\n“Quem disse que não foi? Ficou seis meses em Busan.”\n\nDe repente, percebi: eu tinha decidido o fim da história olhando uma única fotografia.','train')
card('photographer',6,'kiosk','EUN-SOOK','“Fui. Ela me ensinou a apertar o botão três vezes. Depois saiu com meu pente no bolso.”\n\nEun-sook sorriu.\n\n“Só devolveu seis meses depois, quando voltou de Busan.”','train')
card('train',7,'train','HANA','Tentei imaginar minha mãe naquele trem: vinte e poucos anos, uma câmera, medo de errar a plataforma.\n\nSem saber fazer minha sopa. Sem saber meu nome.\n\nSem saber que eu existiria.','postcards')
card('postcards',8,'train','EUN-SOOK','“Arranjou trabalho num laboratório de fotografia. Mandava cartões contando sobre as pessoas. A moça da lavanderia. Um homem que comprava flores toda terça.”\n\n“E por que voltou?”','return')
card('return',9,'kiosk','EUN-SOOK','“Disse que sentia falta do mar daqui. E que a cidade grande não era do jeito que imaginava.”\n\n“Ela se arrependeu?”\n\n“Alguns dias, sim. Em outros, planejava outra viagem. Sua mãe mudava de ideia, Hana.”','bench')
card('bench',10,'bench','HANA','Levamos o chá para o banco da plataforma. Um trem passou sem parar.\n\n“Eu achava que ela tinha desistido de tudo por minha causa.”\n\nJiho esperou o barulho dos vagões diminuir.','answer')
card('answer',11,'bench','JIHO','“Você ainda nem tinha nascido.”\n\n“Eu sei. Agora eu sei.”\n\nEle empurrou meu copo para longe da beirada.\n\nEu queria ter perguntado mais. Sobre o trabalho. Sobre as flores de terça-feira.','say')
card('say',12,'bench','O QUE VOCÊ DIVIDE COM JIHO?','Havia coisas que eu só dizia quando já era tarde.\n\nJiho continuava ali. A conversa ainda podia acontecer.',choices=[choice('“Tenho medo de esquecer a voz dela.”','voice','Você confiou a Jiho o medo de esquecer a voz da sua mãe.'),choice('“Me conta uma coisa engraçada sobre ela.”','laugh','Você abriu espaço para rir de uma lembrança com Jiho.')])
card('voice',13,'bench','JIHO','“Eu tenho um áudio dela brigando comigo por molhar as plantas demais.”\n\nOlhei para ele.\n\n“Não apaga.”\n\n“Não apago. Quando você quiser, a gente escuta.”','drawer')
card('laugh',13,'bench','JIHO','“Ela tirou vinte e três fotos de uma sopa e comeu tudo frio.”\n\n“Por quê?”\n\n“Disse que o vapor estava posando errado.”\n\nRi com o rosto molhado. Dessa vez, não pedi desculpa.','drawer')
card('drawer',14,'kiosk','EUN-SOOK','Eun-sook veio recolher os copos.\n\n“Procura o caderno azul. Gaveta de baixo, no restaurante. Ela colava os retratos ali.”\n\n“Ela continuou fotografando?”\n\n“Até quando a gente fingia que não queria.”','notebook')
card('notebook',15,'notebook','HANA','De volta ao restaurante, encontrei o caderno debaixo dos panos limpos.\n\nO peixeiro rindo. Eun-sook de olhos fechados. Jiho, mais jovem, queimando alguma coisa.\n\nO mundo tinha passado pela nossa mesa. Ela tinha reparado.','blank')
card('blank',16,'notebook','HANA','Na última página, quatro cantoneiras seguravam um espaço vazio.\n\nEmbaixo, a letra dela:\n\n“Hana e eu, do outro lado da mesa. Pedir ao Jiho. Quando ela voltar.”','missing')
card('missing',17,'notebook','HANA','Passei o dedo onde a foto deveria estar. Eu tinha voltado tarde demais para aquele retrato.\n\nPor um instante, quis fechar o caderno. Em vez disso, deixei a página aberta.','last')
card('last',18,'notebook','HANA','Dentro da capa, caiu um comprovante de revelação. Um rolo de filme. Pronto para retirar havia quatro meses.\n\nPeguei o telefone.\n\n“Jiho, você sabe onde fica esse laboratório?”',ending=True,caption='Ainda havia uma fotografia por encontrar.')

episode=dict(schemaVersion=1,id='a-mulher-da-estacao',version=1,episode=2,title='A mulher da estação',series='Quando a chuva passar',subtitle='Antes de ser mãe, ela também tinha uma passagem.',minutes=3,cardCount=18,start='morning',cover='art/station.jpg',endingTitle='Hoje, você conheceu\numa parte dela.',nextTitle='O retrato que faltava',cards=cards)
path=Path(__file__).resolve().parents[1]/'episodes/02-a-mulher-da-estacao/episode.json'
path.write_text(json.dumps(episode,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(path)

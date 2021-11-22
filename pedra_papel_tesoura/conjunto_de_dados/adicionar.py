from argparse import ArgumentParser, RawTextHelpFormatter
from captura_imagens import CapturaImagens

descricao = """
    Script para obtenção de conjunto de dados para treino de classificador  de 
    sinais do jogo Pedra, Papel e Tesoura.
    
    Ações:
      > Pressione a tecla 'Espaço' para começar/pausar.
      > Pressione a tecla 'Q' para fechar o sistema.
"""


def str_or_int(arg):
    try:
        return int(arg)
    except ValueError:
        return str(arg)


parser = ArgumentParser(
    description=descricao,
    formatter_class=RawTextHelpFormatter
)
parser.add_argument(
    '-ns',
    '--nome-do-sinal',
    help='Nome do sinal referente das imagens a serem capturadas.',
    type=str,
    choices=['pedra', 'papel', 'tesoura', 'desconhecido'],
    required=True
)
parser.add_argument(
    '-q',
    '--quantidade',
    help='Quantidade de imagens a serem capturadas',
    type=int,
    required=True
)
parser.add_argument(
    '-cv',
    '--captura-de-video',
    help='Dispositivo/Video do qual serão capturadas as imagens.',
    type=str_or_int,
    default=0
)

args = parser.parse_args()

captura_imagens = CapturaImagens(
    nome_do_sinal=args.nome_do_sinal,
    quantidade_de_capturas=args.quantidade,
    captura_de_video=args.captura_de_video
)
captura_imagens.executar()

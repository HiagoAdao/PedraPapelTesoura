from argparse import ArgumentParser
from captura_images import CapturaImagens

descricao = """
    Arquivo para obtenção de conjunto de dados para treino de classificador 
    de sinais do jogo Pedra, Papel ou Tesoura.
"""

parser = ArgumentParser(description=descricao)
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
    default=0
)

args = parser.parse_args()

captura_imagens = CapturaImagens(
    nome_do_sinal=args.nome_do_sinal,
    quantidade_de_capturas=args.quantidade,
    captura_de_video=args.captura_de_video
)
captura_imagens.executar()

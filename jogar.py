from argparse import ArgumentParser
from pedra_papel_tesoura import PedraPapelTesoura, Util

descricao = """
    Arquivo para obtenção de conjunto de dados para treino de classificador 
    de sinais do jogo Pedra, Papel ou Tesoura.

    Ações:
     > Utilize a cor X para Y
"""

parser = ArgumentParser(description=descricao)
parser.add_argument(
    '-cv',
    '--captura-de-video',
    help='Dispositivo/Video do qual serão capturadas as imagens.',
    type=Util.str_or_int,
    default=0
)

args = parser.parse_args()

if __name__ == '__main__':
    pedra_papel_tesoura = PedraPapelTesoura(
        captura_de_video=args.captura_de_video
    )
    pedra_papel_tesoura.jogar()

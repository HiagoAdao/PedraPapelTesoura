from argparse import ArgumentParser, RawTextHelpFormatter
from pedra_papel_tesoura import PedraPapelTesoura

descricao = """
    Script para inicialização do jogo Pedra, Papel e Tesoura.

    Ações:
      > Utilize a cor 'Azul' para iniciar o jogo.
      > Pressione a tecla 'D' para iniciar uma disputa.
      > Utilize a cor 'Rosa' ou pressione a tecla 'Q' para encerra o jogo.
"""

parser = ArgumentParser(
    description=descricao,
    formatter_class=RawTextHelpFormatter
)
parser.add_argument(
    '-cv',
    '--captura-de-video',
    help='Dispositivo do qual serão capturadas as imagens.',
    type=int,
    default=0
)

args = parser.parse_args()

if __name__ == '__main__':
    pedra_papel_tesoura = PedraPapelTesoura(
        captura_de_video=args.captura_de_video
    )
    pedra_papel_tesoura.jogar()

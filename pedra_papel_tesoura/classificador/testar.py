from argparse import ArgumentParser, RawTextHelpFormatter
from pedra_papel_tesoura import ClassificadorPedraPapelTesoura

descricao = """
    Script para teste de classificação do modelo treinado para reconhecer 
    sinais do jogo Pedra, Papel e Tesoura. 
"""

parser = ArgumentParser(
    description=descricao,
    formatter_class=RawTextHelpFormatter
)
parser.add_argument(
    '-i',
    '--imagem',
    help='Imagem para teste de classificação',
    type=str,
    required=True
)
args = parser.parse_args()

classificador = ClassificadorPedraPapelTesoura()
classificador.testar(args.imagem)

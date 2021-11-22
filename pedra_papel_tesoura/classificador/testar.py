from argparse import ArgumentParser
from pedra_papel_tesoura import ClassificadorPedraPapelTesoura

descricao = """
    Script para testar classificação do modelo treinado para reconhecer 
    sinais do jogo Pedra, Papel ou Tesoura.
"""

parser = ArgumentParser(description=descricao)
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

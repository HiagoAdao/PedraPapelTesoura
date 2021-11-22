# ✊✋✌️ com visão computacional 🙆‍♂️

Pedra, papel, e tesoura, com visão computacional.

Este projeto consiste em um jogo de pedra, papel, e tesoura.

## Principais tecnologias utilizadas
 - [Python](https://www.python.org/)
 - [OpenCV](https://opencv.org/)
 - [Face recognition](https://github.com/ageitgey/face_recognition)
 - [Tensor flow](https://www.tensorflow.org/?hl=pt-br)
 - [Keras squeezenet](https://pypi.org/project/keras_squeezenet/)
 
## Requerimentos
É necessário fazer a instalação e preparo do projeto antes do rodar localmente, para isso execute os passos abaixo na raiz do projeto:

- Criar um ambiente virtual ([venv](https://docs.python.org/3/library/venv.html)) para a instalação, executando o seguinte comando:
```sh
python3 -m venv {nome da sua venv}
```
- Ativar o ambiente virtual (LINUX e MAC).
```bash
source {nome da sua venv}/bin/activate
```
- Ativar o ambiente virtual (WINDOWS).
```bash
{nome da sua venv}/bin/activate.bat
```
- Instalar as dependências.
```sh
pip3 install -r requirements.txt
```

Agora com as dependências instaladas, será necessário criar o conjunto de dados para treinar um classificador de Pedra, Papel e Tesoura.
Para isso, execute os passos abaixo na raiz do projeto:

- Para adicionar a massa de dados.
```sh
python3 pedra_papel_tesoura/conjunto_de_dados/adicionar.py -ns {pedra/papel/tesoura/desconhecido} -q {quantidade de capturas}
```

- Após adicionar massa para Pedra, Papel, Tesoura e Desconhecidos, será necessário treinar um classificador para identificação dos sinais.
```sh
python3 pedra_papel_tesoura/classificador/treinar.py
```

- Após treinar o classificador podemos fazer um teste. Utilize o comando abaixo para o passo a passo detalhado.
```sh
python3 pedra_papel_tesoura/classificador/testar.py -i {path da imagem a ser testada}
```

Pronto! Agora estamos prontos para jogar!

**Obs: Todos os detalhes dos comandos podem ser encontrados executando o arquivo com o parâmetro -h ou --help**

## Execução

Para execução do jogo, utilize o comando abaixo na raiz do projeto:

```sh
python3 jogar.py
```

Funcionalidades:

- São reconhecidas as faces dos jogadores de acordo com a posição em que se encontram.
- São reconhecidos os gestos do tradicional jogo de pedra, papel, e tesoura. Sendo:
  - ✊ -> Pedra
  - 🖐 -> Papel
  - ✌️ -> Tesoura
 
- São reconhecidas duas cores, uma inicia o jogo e outra encerra.
  - Cor Azul -> Inicia o jogo
  - Cor Rosa -> Encerra o jogo
  - Cor Azul + Rosa -> Encerra o sistema

- São reconhecidas duas cores, uma inicia o jogo e outra encerra.
  - Cor Azul -> Inicia o jogo
  - Cor Rosa -> Encerra o jogo
  - Cor Azul + Rosa -> Encerra o sistema

- Para o jogo em si, são reconhecidos os seguintes comandos:
  - Tecla 'D' -> Inicia a disputa.
  - Tecla 'Q' -> Força encerramento do sistema.
 
## Contato

- [Hiago Adão Müller Oliveira](https://www.linkedin.com/in/hiago-adão-müller-oliveira-b223b1161)
- [Isaura Koch](https://www.linkedin.com/in/isaura-koch-a3a990169/)
 

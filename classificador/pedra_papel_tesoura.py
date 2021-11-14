import cv2
import numpy as np
from os import path, listdir
from keras.optimizers import Adam
from keras.utils import np_utils
from keras.layers import (
    Activation,
    Dropout,
    Convolution2D,
    GlobalAveragePooling2D
)
from keras.models import Sequential
from keras.models import load_model
from keras_squeezenet import SqueezeNet


class ClassificadorPedraPapelTesoura:
    def __init__(self):
        self.__diretorio_conjunto_de_dados = 'imagens_capturadas'

        self.__mapeamento_sinais = {
            "pedra": 0,
            "papel": 1,
            "tesoura": 2,
            "desconhecido": 3
        }

        self.__conjunto_de_dados = []
        self.__modelo: Sequential = None

    def testar(self, diretorio_imagem: str):
        print(f"\n[INFO] Obtendo imagem para classificação...\n")

        if not path.exists('modelo_pedra_papel_tesoura.h5'):
            print('[ERROR] Classificador não encontrado.')
            return

        classificador = load_model("modelo_pedra_papel_tesoura.h5")

        mapeamento_sinais_inverso = {
            valor: sinal
            for sinal, valor in self.__mapeamento_sinais.items()
        }

        imagem = cv2.imread(diretorio_imagem)
        imagem_redimensionada = cv2.resize(
            cv2.cvtColor(
                imagem,
                cv2.COLOR_BGR2RGB
            ),
            (227, 227)
        )

        predicao = classificador.predict(np.array([imagem_redimensionada]))
        sinal_identificado = mapeamento_sinais_inverso.get(
            np.argmax(predicao[0])
        )

        print(
            "\n[INFO] Sinal identificado/classificado como: "
            f"{sinal_identificado}.\n"
        )

    def treinar(self) -> None:
        self.__carrega_capturas()
        self.__monta_modelo()
        self.__treina_modelo()
        self.__salva_modelo()

    def __monta_modelo(self) -> None:
        print('\n[INFO] Montando classificador...\n')
        modelo = Sequential([
            SqueezeNet(
                input_shape=(227, 227, 3),
                include_top=False
            ),
            Dropout(0.5),
            Convolution2D(
                len(self.__mapeamento_sinais),
                (1, 1),
                padding='valid'
            ),
            Activation('relu'),
            GlobalAveragePooling2D(),
            Activation('softmax')
        ])
        modelo.compile(
            optimizer=Adam(lr=0.0001),
            loss='categorical_crossentropy',
            metrics=['accuracy']
        )
        self.__modelo = modelo

        print('\n[INFO] Classificador montado com sucesso...\n')

    def __carrega_capturas(self) -> None:
        print("\n[INFO] Importando capturas...\n")

        capturas = []
        for nome_sinal in listdir(self.__diretorio_conjunto_de_dados):
            diretorio_sinal = path.join(
                self.__diretorio_conjunto_de_dados,
                nome_sinal
            )
            if not path.isdir(diretorio_sinal):
                continue

            for sinal in listdir(diretorio_sinal):
                if sinal.startswith("."):
                    continue

                captura = cv2.imread(path.join(diretorio_sinal, sinal))
                captura_redimensionada = cv2.resize(
                    cv2.cvtColor(
                        captura,
                        cv2.COLOR_BGR2RGB
                    ),
                    (227, 227)
                )
                capturas.append(
                    [captura_redimensionada, nome_sinal]
                )
        self.__conjunto_de_dados = capturas

        print("\n[INFO] Capturas importadas com sucesso.\n")

    def __treina_modelo(self) -> None:
        print("\n[INFO] Treinando classificador...\n")

        capturas, sinais = zip(*self.__conjunto_de_dados)
        sinais = list(map(
            lambda captura: self.__mapeamento_sinais[captura],
            sinais
        ))

        sinais = np_utils.to_categorical(sinais)

        self.__modelo.fit(
            np.array(capturas),
            np.array(sinais),
            epochs=10
        )

        print("[INFO] Classificador treinado com sucesso.")

    def __salva_modelo(self) -> None:
        print("\n[INFO] Salvando classificador...\n")

        self.__modelo.save("modelo_pedra_papel_tesoura.h5")

        print("\n[INFO] Classificador salvo com sucesso.\n")

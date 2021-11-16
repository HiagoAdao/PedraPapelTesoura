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


class ClassificadorPedraPapelTesouraException(BaseException):
    def __init__(self, msg):
        super(ClassificadorPedraPapelTesouraException, self).__init__(msg)


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

    def classificar(self, imagem: np.ndarray) -> str:
        print(f"\n[INFO] Obtendo imagem para classificação...\n")
        self.__importar_modelo()

        imagem_redimensionada: np.ndarray = self.__redimensionar_imagem(imagem)
        sinal_identificado: str = self.__classificar(imagem_redimensionada)

        print(
            "\n[INFO] Sinal identificado/classificado como: "
            f"{sinal_identificado}.\n"
        )

        return sinal_identificado

    def testar(self, diretorio_imagem: str) -> None:
        print(f"\n[INFO] Obtendo imagem para classificação...\n")
        self.__importar_modelo()

        imagem_redimensionada: np.ndarray = self.__redimensionar_imagem(
            cv2.imread(diretorio_imagem)
        )
        sinal_identificado: str = self.__classificar(imagem_redimensionada)

        print(
            "\n[INFO] Sinal identificado/classificado como: "
            f"{sinal_identificado}.\n"
        )

    def treinar(self) -> None:
        self.__carregar_capturas()
        self.__montar_modelo()
        self.__treinar_modelo()
        self.__salvar_modelo()

    def __montar_modelo(self) -> None:
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

    def __carregar_capturas(self) -> None:
        print("\n[INFO] Importando capturas...\n")

        capturas = []
        for nome_sinal in listdir(self.__diretorio_conjunto_de_dados):
            diretorio_sinal: str = path.join(
                self.__diretorio_conjunto_de_dados,
                nome_sinal
            )
            if not path.isdir(diretorio_sinal):
                continue

            for sinal in listdir(diretorio_sinal):
                if sinal.startswith("."):
                    continue

                captura: np.ndarray = cv2.imread(
                    path.join(diretorio_sinal, sinal)
                )
                captura_redimensionada: np.ndarray = (
                    self.__redimensionar_imagem(captura)
                )
                capturas.append(
                    [captura_redimensionada, nome_sinal]
                )
        self.__conjunto_de_dados: list = capturas

        print("\n[INFO] Capturas importadas com sucesso.\n")

    def __treinar_modelo(self) -> None:
        print("\n[INFO] Treinando classificador...\n")

        capturas, sinais = zip(*self.__conjunto_de_dados)
        sinais = list(map(
            lambda captura: self.__mapeamento_sinais[captura],
            sinais
        ))

        sinais: np.ndarray = np_utils.to_categorical(sinais)

        self.__modelo.fit(
            np.array(capturas),
            np.array(sinais),
            epochs=10
        )

        print("[INFO] Classificador treinado com sucesso.")

    def __salvar_modelo(self) -> None:
        print("\n[INFO] Salvando classificador...\n")

        self.__modelo.save("modelo_pedra_papel_tesoura.h5")

        print("\n[INFO] Classificador salvo com sucesso.\n")

    def __importar_modelo(self) -> None:
        if not path.exists('modelo_pedra_papel_tesoura.h5'):
            msg_error = '[ERROR] Classificador não encontrado.'
            print(msg_error)
            raise ClassificadorPedraPapelTesouraException(msg_error)

        self.__modelo = load_model("modelo_pedra_papel_tesoura.h5")

    def __classificar(self, imagem: np.ndarray) -> str:
        mapeamento_sinais_inverso = {
            valor: sinal
            for sinal, valor in self.__mapeamento_sinais.items()
        }

        predicao: int = self.__modelo.predict(np.array([imagem]))
        sinal_identificado: str = mapeamento_sinais_inverso.get(
            np.argmax(predicao[0]),
            self.__mapeamento_sinais['desconhecido']
        )
        return sinal_identificado

    def __redimensionar_imagem(self, imagem: np.ndarray):
        imagem_redimensionada: np.ndarray = cv2.resize(
            cv2.cvtColor(
                imagem,
                cv2.COLOR_BGR2RGB
            ),
            (227, 227)
        )
        return imagem_redimensionada

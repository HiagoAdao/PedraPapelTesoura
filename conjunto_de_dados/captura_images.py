import cv2
from os import path, mkdir, walk


class CapturaImagens:
    def __init__(self,
                 nome_do_sinal: str,
                 quantidade_de_capturas: int,
                 captura_de_video: int):
        self.__nome_do_sinal = nome_do_sinal

        self.__quantidade_de_capturas = quantidade_de_capturas
        self.__captura_de_video = cv2.VideoCapture(captura_de_video)

        self.__dados_diretorio_salvamento = dict(
            caminho='',
            ultima_captura=0
        )

    def executar(self) -> None:
        self.__monta_diretorio_de_salvamento()
        self.__captura_imagens()

    def __captura_imagens(self) -> None:
        print("======== Iniciando captura de imagens ========")

        capturar = False
        quantidade_de_capturas = 0

        while True:
            _, frame = self.__captura_de_video.read()
            frame = cv2.flip(frame, 1)

            self.__monta_posicao_captura(frame)

            if capturar:
                numero_captura = quantidade_de_capturas + 1
                self.__salva_captura(frame, numero_captura)
                quantidade_de_capturas = numero_captura
                print(f"[INFO] Captura número {numero_captura} ")

            self.__informa_quantidade_de_capturas(
                frame,
                quantidade_de_capturas
            )

            tecla = cv2.waitKey(10)
            if tecla == ord(' '):
                capturar = not capturar

            parar_processamento = bool(
                quantidade_de_capturas == self.__quantidade_de_capturas or
                tecla == ord('q')
            )
            if parar_processamento:
                break

        cv2.destroyAllWindows()
        print(
            "[INFO] Captura de imagens encerrada. "
            f"Total de {quantidade_de_capturas} imagens capturadas. "
            "As imagens foram salvas em: "
            f"'{self.__dados_diretorio_salvamento['caminho']}'."
        )

    def __monta_posicao_captura(self, frame) -> None:
        posicao = (100, 200)
        largura_e_altura = (650, 750)
        cv2.rectangle(
            frame,
            posicao,
            largura_e_altura,
            (0, 0, 0),
            2
        )

    def __informa_quantidade_de_capturas(self,
                                         frame,
                                         quantidade_de_capturas: int) -> None:
        cv2.putText(
            frame,
            f"Imagens capturadas: {quantidade_de_capturas}",
            (100, 190),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 0, 0),
            2,
            cv2.LINE_AA
        )
        cv2.imshow("Captura de imagem", frame)

    def __salva_captura(self, frame, numero_captura: int) -> None:
        nome_captura = (
            self.__dados_diretorio_salvamento['ultima_captura'] +
            numero_captura
        )
        cv2.imwrite(
            path.join(
                self.__dados_diretorio_salvamento['caminho'],
                f'{nome_captura}.jpg'
            ),
            frame[220:750, 100:590]
        )

    def __monta_diretorio_de_salvamento(self) -> None:
        diretorio_de_imagens_capturadas = 'imagens_capturadas'
        if not path.exists(diretorio_de_imagens_capturadas):
            mkdir(diretorio_de_imagens_capturadas)

        diretorio_sinal = path.join(
            diretorio_de_imagens_capturadas,
            self.__nome_do_sinal
        )
        if not path.exists(diretorio_sinal):
            mkdir(diretorio_sinal)

        ultimas_capturas = [
            int(captura.replace('.jpg', ''))
            for captura in next(walk(diretorio_sinal))[2]
        ]

        self.__dados_diretorio_salvamento['caminho'] = diretorio_sinal
        self.__dados_diretorio_salvamento['ultima_captura'] = (
            max(ultimas_capturas)
            if ultimas_capturas
            else 0
        )

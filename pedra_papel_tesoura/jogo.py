import cv2
from numpy import ndarray
from typing import Union
from .util import Util, Timer
from .classificador import ClassificadorPedraPapelTesoura
from .reconhecimento_facial import ReconhecedorFacial
from .reconhecimento_cores import ReconhecedorCores


class PedraPapelTesoura:
    def __init__(self, captura_de_video: Union[int, str]):
        self.__captura_de_video = cv2.VideoCapture(captura_de_video)
        self.__classificador = ClassificadorPedraPapelTesoura()
        self.__reconhecedor_cores = ReconhecedorCores()
        self.__timer = Timer()

        self.__frame: ndarray = None
        self.__regras = {}

        self.__layout_color = (18, 10, 143)

        self.__dados_jogo = dict(
            comecar=False,
            encerrar=False,
            preparar_disputa=True,
            dados_ultimo_jogo=dict(
                resultado='??',
                cor_texto=self.__layout_color[::-1]
            ),
            logs=[]
        )

    def jogar(self) -> None:
        self.__inicializar_regras()
        self.__iniciar()
        self.__salvar_log()
        self.__encerrar()

    def __inicializar_regras(self) -> None:
        regras = {
            ('pedra', 'papel'): 'papel',
            ('pedra', 'tesoura'): 'pedra',
            ('papel', 'tesoura'): 'tesoura'
        }
        self.__regras = regras

    def __iniciar(self) -> None:
        while True:
            _, frame = self.__captura_de_video.read()
            self.__frame: ndarray = cv2.flip(frame, 1)

            self.__detectar_cor()

            if self.__dados_jogo['comecar']:
                sinal_identificado_jogador1 = self.__detectar_sinal(
                    self.__frame[430:710, 620:920]
                )
                sinal_identificado_jogador2 = self.__detectar_sinal(
                    self.__frame[430:710, 980:1270]
                )

                self.__detectar_jogador(
                    self.__frame[0:1290, 10:940],
                    'Jogador 1'
                )
                self.__detectar_jogador(
                    self.__frame[0:1180, 960:2050],
                    'Jogador 2'
                )

                if cv2.waitKey(10) == ord('d'):
                    self.__reinicia_disputa()

                self.__organizar_layout()

                self.__informa_sinal_identificado(
                    posicao=(620, 410),
                    sinal=sinal_identificado_jogador1
                )
                self.__informa_sinal_identificado(
                    posicao=(980, 410),
                    sinal=sinal_identificado_jogador2
                )

                if not self.__dados_jogo['preparar_disputa']:
                    resultado = self.__obter_resultado_disputa({
                        sinal_identificado_jogador1,
                        sinal_identificado_jogador2
                    })
                    self.__apresentar_ganhador(
                        sinal_identificado_jogador1,
                        sinal_identificado_jogador2,
                        resultado
                    )

                    is_jogada_valida: bool = (
                        "desconhecido" not in
                        [sinal_identificado_jogador1,
                         sinal_identificado_jogador2]
                    )
                    if is_jogada_valida and not self.__timer.is_running:
                        self.__timer.start(3)
                else:
                    self.__apresentar_resultado_indefinido()

                self.__timer.execute_function_when_end(
                    self.__reinicia_disputa
                )

            cv2.imshow("Pedra, Papel e Tesoura", self.__frame)

            parar_execucao = bool(
                cv2.waitKey(10) == ord('q') or
                self.__dados_jogo['encerrar']
            )
            if parar_execucao:
                break

    def __organizar_layout(self) -> None:
        self.__adicionar_titulos()
        self.__dividir_tela()

        self.__montar_area_jogador(
            (620, 430),
            (920, 710)
        )
        self.__montar_area_jogador(
            (980, 430),
            (1270, 710)
        )

    def __adicionar_titulos(self) -> None:
        cv2.putText(
            self.__frame,
            "Pedra, Papel e Tesoura",
            (710, 50),
            cv2.FONT_HERSHEY_TRIPLEX,
            1.2,
            self.__layout_color[::-1],
            2,
            cv2.LINE_AA
        )
        cv2.putText(
            self.__frame,
            "Resultado: ",
            (760, 190),
            cv2.FONT_HERSHEY_DUPLEX,
            1.2,
            self.__layout_color[::-1],
            2,
            cv2.LINE_AA
        )

    def __dividir_tela(self) -> None:
        cv2.line(
            self.__frame,
            (950, 70),
            (950, 150),
            self.__layout_color[::-1],
            thickness=4
        )

        cv2.line(
            self.__frame,
            (950, 220),
            (950, 1080),
            self.__layout_color[::-1],
            thickness=4
        )

    def __montar_area_jogador(self,
                              posicao: tuple,
                              largura_altura: tuple) -> None:
        cv2.rectangle(
            self.__frame,
            posicao,
            largura_altura,
            self.__layout_color[::-1],
            cv2.FILLED if self.__dados_jogo['preparar_disputa'] else 4
        )

    def __detectar_sinal(self, sinal_para_identificacao: ndarray) -> str:
        sinal_identificado = self.__classificador.classificar(
            sinal_para_identificacao
        )
        return sinal_identificado

    def __informa_sinal_identificado(self, posicao: tuple, sinal: str) -> None:
        cor_borda = (
            (0, 255, 0)
            if sinal != "desconhecido"
            else (0, 0, 255)
        )
        texto_sinal = (
            sinal.capitalize()
            if not self.__dados_jogo['preparar_disputa']
            else '******'
        )
        cv2.putText(
            self.__frame,
            f"Sinal: {texto_sinal}",
            posicao,
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            cor_borda,
            2,
            cv2.LINE_AA
        )

    def __detectar_jogador(self, frame_jogador: ndarray, nome: str):
        localizacao = ReconhecedorFacial.reconhecer(frame_jogador)
        if localizacao:
            ReconhecedorFacial.destacar_face(
                frame_jogador,
                localizacao[0],
                nome,
                cor_borda=self.__layout_color[::-1]
            )

    def __detectar_cor(self):
        cor = self.__reconhecedor_cores.identificar(self.__frame)
        if cor == 'Color1':
            self.__dados_jogo['comecar'] = True
            self.__dados_jogo['encerrar'] = False
        elif cor == 'Color2':
            self.__dados_jogo['encerrar'] = True
            self.__dados_jogo['comecar'] = False

    def __apresentar_ganhador(self,
                              sinal_jogador1: str,
                              sinal_jogador2: str,
                              resultado: str) -> None:
        if "desconhecido" in [sinal_jogador1, sinal_jogador2]:
            self.__apresentar_resultado_indefinido()
            return

        cor_texto = (0, 140, 255)
        resultado_jogo = 'Empate!!'
        if resultado == sinal_jogador1:
            resultado_jogo = 'Jogador 1 venceu!!'
            cor_texto = (0, 255, 0)
        elif resultado == sinal_jogador2:
            resultado_jogo = 'Jogador 2 venceu!!'
            cor_texto = (0, 255, 0)

        cv2.putText(
            self.__frame,
            resultado_jogo,
            (970, 190),
            cv2.FONT_HERSHEY_DUPLEX,
            1.2,
            cor_texto,
            2,
            cv2.LINE_AA
        )

        self.__dados_jogo['dados_ultimo_jogo'] = dict(
            resultado=resultado_jogo,
            cor_texto=cor_texto
        )

        msg_log = (
            f'Jogo feito em: {Util.get_current_date("%d/%m/%Y %H:%M:%S")} '
            f'Movimento Jogador1: {sinal_jogador1.upper()}. '
            f'Movimento Jogador2: {sinal_jogador2.upper()}. '
            f'Vencedor: {resultado_jogo.upper()}.'
        )
        self.__dados_jogo['logs'].append(msg_log)

    def __apresentar_resultado_indefinido(self):
        cv2.putText(
            self.__frame,
            self.__dados_jogo['dados_ultimo_jogo']['resultado'],
            (970, 190),
            cv2.FONT_HERSHEY_DUPLEX,
            1.2,
            self.__dados_jogo['dados_ultimo_jogo']['cor_texto'],
            2,
            cv2.LINE_AA
        )

    def __obter_resultado_disputa(self, disputa: set) -> str:
        movimento = next(filter(
            lambda regra: set(regra) == disputa,
            self.__regras
        ), None)
        return self.__regras.get(movimento)

    def __reinicia_disputa(self):
        self.__dados_jogo['dados_ultimo_jogo'] = dict(
            resultado='??',
            cor_texto=self.__layout_color[::-1]
        )
        self.__dados_jogo['preparar_disputa'] = (
            not self.__dados_jogo['preparar_disputa']
        )

    def __salvar_log(self):
        if not self.__dados_jogo['logs']:
            return

        with open('logs_partidas.txt', 'w') as arquivo:
            for log in self.__dados_jogo['logs']:
                arquivo.write(f'{log}\n')

    def __encerrar(self) -> None:
        cv2.destroyAllWindows()
        self.__captura_de_video.release()

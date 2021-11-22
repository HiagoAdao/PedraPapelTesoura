import cv2
import numpy as np
import face_recognition


class ReconhecedorFacial:
    @staticmethod
    def reconhecer(frame: np.ndarray):
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = small_frame[:, :, ::-1]

        faces_localizadas = face_recognition.face_locations(
            rgb_small_frame
        )
        return faces_localizadas

    @staticmethod
    def destacar_face(frame: np.ndarray,
                      localizacao: np.ndarray,
                      nome: str,
                      cor_borda: tuple = (0, 0, 255),
                      cor_nome: tuple = (255, 255, 255)):
        top, right, bottom, left = localizacao

        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        cv2.rectangle(
            frame,
            (left, top),
            (right, bottom),
            cor_borda,
            2
        )
        cv2.rectangle(
            frame,
            (left, bottom - 35),
            (right, bottom),
            cor_borda,
            cv2.FILLED
        )
        cv2.putText(
            frame,
            nome,
            (left + 6, bottom - 6),
            cv2.FONT_HERSHEY_DUPLEX,
            1.0,
            cor_nome,
            1
        )

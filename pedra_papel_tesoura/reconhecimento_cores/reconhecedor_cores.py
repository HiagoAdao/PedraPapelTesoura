import cv2
import numpy as np
from typing import Tuple


class ReconhecedorCores:
    def __init__(self):
        self.__color1 = (
            np.array([100, 69, 75]),
            np.array([117, 255, 255]),
        )

        self.__color2 = (
            np.array([138, 48, 158]),
            np.array([179, 255, 255])
        )

    def identificar(self, frame: np.ndarray) -> str:
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        has_color1_in_frame = self.__identify_color(
            frame,
            hsv_frame,
            self.__color1
        )
        if has_color1_in_frame:
            return 'Color1'

        has_color2_in_frame = self.__identify_color(
            frame,
            hsv_frame,
            self.__color2
        )
        if has_color2_in_frame:
            return 'Color2'

    def __identify_color(self,
                         frame: np.ndarray,
                         frame_hsv: np.ndarray,
                         color_hsv: tuple) -> Tuple[bool, tuple]:
        mask = cv2.inRange(frame_hsv, *color_hsv)
        _, border = cv2.threshold(
            cv2.cvtColor(
                cv2.bitwise_and(frame, frame, mask=mask),
                cv2.COLOR_BGR2GRAY
            ),
            3,
            255,
            cv2.THRESH_BINARY
        )
        contours, _ = cv2.findContours(
            border,
            cv2.RETR_LIST,
            cv2.CHAIN_APPROX_SIMPLE
        )

        found_color = False
        for contour in contours:
            area = cv2.contourArea(contour)
            x, y, width, height = cv2.boundingRect(
                contour)
            if area > 500:
                cv2.rectangle(
                    frame,
                    (x, y),
                    (x + width, y + height),
                    (0, 0, 0),
                    4
                )
                found_color = True
        return found_color

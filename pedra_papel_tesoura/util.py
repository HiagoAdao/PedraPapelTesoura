from datetime import datetime, timedelta
from typing import Any, Union, Callable


class Util:
    @staticmethod
    def str_or_int(arg: Any) -> Union[str, int]:
        try:
            return int(arg)
        except ValueError:
            return str(arg)

    @staticmethod
    def get_current_date(format_date: str):
        current_date = datetime.today()
        formated_date = current_date.strftime(format_date)
        return formated_date


class Timer:
    def __init__(self):
        self.__start_time: float = None
        self.__end_time: Union[int, float] = None

    @property
    def is_running(self) -> bool:
        return bool(self.__start_time and self.__end_time)

    def start(self, time: Union[int, float]) -> None:
        current_time = self.__get_current_date()
        self.__start_time: datetime = current_time
        self.__end_time = current_time + timedelta(0, time)

    def execute_function_when_end(self, func: Callable) -> None:
        if not self.__start_time or not self.__end_time:
            return

        current_time = self.__get_current_date()
        print(current_time, self.__end_time, current_time >= self.__end_time)
        if current_time >= self.__end_time:
            self.__start_time = None
            func()

    def __get_current_date(self) -> datetime:
        return datetime.today()

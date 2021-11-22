from typing import Any, Union
from datetime import datetime


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

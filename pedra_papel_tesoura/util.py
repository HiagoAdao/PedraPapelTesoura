from typing import Any, Union


class Util:
    @staticmethod
    def str_or_int(arg: Any) -> Union[str, int]:
        try:
            return int(arg)
        except ValueError:
            return str(arg)

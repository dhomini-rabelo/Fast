from typing import Callable
from ..utils.main import get_decimal_str

adapt_data_functions: dict[Callable] = {
    'int': lambda value: int(value),
    'str': lambda value: str(value),
    'decimal_2': lambda value: get_decimal_str(value),
}
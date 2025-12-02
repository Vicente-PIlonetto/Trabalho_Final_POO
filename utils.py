from datetime import date
from globals import ITEM_TYPES


def is_float(string: str) -> bool:
    try:
        float(string)
        return True
    except ValueError:
        return False


def get_tipo_descricao(tipo: int):
    for i in ITEM_TYPES:
        if tipo == i[0]:
            return i[1]

    return "Padrão"

def get_pcnt(value: float) -> str:
    return f"{value*100:.1f} %"

def timestamp_to_date(timestamp: int) -> str:
    dt = date.fromtimestamp(timestamp)
    return dt.strftime("%d/%m/%Y")
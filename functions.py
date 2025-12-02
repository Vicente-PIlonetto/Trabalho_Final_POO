import asyncio
from tkinter import StringVar, INSERT
from tkinter.ttk import Entry
from typing import Any, Callable, Coroutine, ParamSpec, TypeVar

from constraints import DATA_PADRAO


def possui_digitos(senha: str):
    for i in senha:
        if "0" <= i <= "9":
            return True
    return False


def possui_letras(senha: str):
    for i in senha:
        if "a" <= i <= "z" or "A" <= i <= "Z":
            return True
    return False


def _replace_chars(string: str, l: int):
    _string = ""
    for i in range(len(string[:l])):
        if "0" <= string[i] <= "9" or string[i] == "_":
            _string += string[i]
    return _string.ljust(l, "_")


def date_mask(entry: Entry, var: StringVar):
    value = var.get().split("/")
    if value[0] == "":
        entry.icursor(0)
        var.set(DATA_PADRAO)
        return

    for i in range(3):
        value[i] = _replace_chars(value[i], 2 if i != 2 else 4)

    if value[0].isdigit() and value[0] > "31":
        value[0] = "31"
    if value[1].isdigit() and value[1] > "12":
        value[1] = "12"
    if value[2].isdigit():
        if value[2] > "2025":
            value[2] = "2025"
        elif value[2] < "1865":
            value[2] = "1865"

    pos = entry.index(INSERT)
    if pos in (2, 5):
        entry.icursor(pos + 1)
    var.set("/".join(value))


def int_mask(entry: Entry, var: StringVar):
    value = var.get()

    if value.isdigit() or value == '':
        return
    pos = entry.index(INSERT)

    _chars = []
    for char in value:
        if "0" <= char <= "9":
            _chars.append(char)
        else:
            pos -= 1

    var.set("".join(_chars))
    entry.after(1, lambda: entry.icursor(pos))


def float_mask(entry: Entry, var: StringVar):
    value = var.get()

    if value.isdigit() or value == '':
        return
    pos = entry.index(INSERT)

    _chars = []
    if value[0] in '.,':
        _chars.append('0')
        pos += 1

    for char in value:
        if "0" <= char <= "9" or char == '.':
            _chars.append(char)
        elif char == ',':
            _chars.append('.')
        else:
            pos -= 1

    var.set("".join(_chars))
    entry.after(1, lambda: entry.icursor(pos))


def hex_to_rgb(hex_color: str) -> tuple[int, ...]:
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def luminance(r: int, g: int, b: int) -> float:
    return 0.299*r + 0.587*g + 0.114*b

def text_by_color(hex_color: str) -> str:
    r, g, b = hex_to_rgb(hex_color)
    return "#000000" if luminance(r, g, b) > 186 else "#FFFFFF"

R = TypeVar("R")
P = ParamSpec("P")


def wrapper(
    func: Callable[P, Coroutine[Any, Any, R]], *args: P.args, **kwargs: P.kwargs
) -> None:
    asyncio.create_task(func(*args, **kwargs))

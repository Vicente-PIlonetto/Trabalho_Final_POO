from tkinter import Widget, ttk, Frame, StringVar
from tkinter.colorchooser import askcolor
from typing import Callable, Literal

from constraints import DATA_PADRAO
from functions import date_mask, float_mask, int_mask, text_by_color


class Default_input(Frame):
    ID = 0

    def __init__(
        self,
        master,
        input_name: str,
        input_type: Literal[
            "input", "combo", "password", "date", "int", "float", "color"
        ] = "input",
        values: list[str] | tuple[str, ...] | None = None,
        on_change: Callable[[ttk.Entry | ttk.Combobox, StringVar], None] | None = None,
        default_value: str | None = None,
        block: bool = False,
    ):
        super().__init__(master)
        self._id = self.ID
        self.ID += 1

        _default_value = ""
        if input_type == "date":
            _default_value = DATA_PADRAO
        elif input_type == "color":
            _default_value = "#FFFFFF"
        self._var = StringVar(self, _default_value)

        ttk.Label(self, text=input_name).grid(
            row=0, column=0, padx=5, pady=5, sticky="w"
        )

        if input_type in ("input", "password", "date", "int", "float"):
            self._input = ttk.Entry(
                self,
                textvariable=self._var,
                show="*" if input_type == "password" else "",
                state="disabled" if block else "normal",
                width=10 if input_type == "date" else 16,
            )
            if input_type == "date":
                self._var.trace_add(
                    "write",
                    lambda *args: date_mask(self._input, self._var),
                )
            elif input_type == "int":
                self._var.trace_add(
                    "write", lambda *args: int_mask(self._input, self._var)
                )
            elif input_type == "float":
                self._var.trace_add(
                    "write", lambda *args: float_mask(self._input, self._var)
                )
            if on_change:
                self._var.trace_add(
                    "write", lambda *args: on_change(self._input, self._var)
                )
        elif input_type == "combo":
            if not values:
                raise ValueError("Values is empty")
            self._values = values
            self._input = ttk.Combobox(
                self,
                values=values,
                state="disabled" if block else "readonly",
                textvariable=self._var,
                width=14,
            )
            self._input.set(default_value or values[0])

            if on_change:
                self._input.bind(
                    "<<ComboboxSelected>>",
                    lambda *args: on_change(self._input, self._var),
                )
        elif input_type == "color":
            style_name = f"Custom.ColorPickerInput{self._id}"
            self.style = ttk.Style()
            self.style.layout(style_name, self.style.layout("TEntry"))
            self.style.configure(
                style_name,
                fieldbackground="#FFFFFF",
                readonlybackground="#FFFFFF",
                foreground="#000000",
            )
            self.style.map(style_name)
            self._input = ttk.Entry(
                self,
                textvariable=self._var,
                state="readonly",
                style=style_name,
                width=7,
            )
            self._input.bind("<Button-1>", lambda *args: self._get_color())

        if self._input:
            self._input.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        self.columnconfigure(0, weight=1)

    def get(self) -> str | int:
        value = self._input.get()

        if isinstance(self._input, ttk.Combobox):
            return self._values.index(value)
        else:
            return value

    def grid(self, row: int = 0, column: int = 0, columnspan: int = 2, **kwargs):
        super().grid(
            **kwargs, row=row, column=column, columnspan=columnspan, sticky="ew"
        )

    def _get_color(self):
        cor = askcolor(title="Escolha uma cor")
        if cor[1]:
            self._var.set(cor[1])
            self._input.config(background=cor[1])

            self.style.configure(
                f"Custom.ColorPickerInput{self._id}",
                readonlybackground=cor[1],
                fieldbackground=cor[1],
                foreground=text_by_color(cor[1]),
            )
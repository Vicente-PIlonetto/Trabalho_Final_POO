from tkinter import ttk, Frame
from typing import Callable


class Link(Frame):
    def __init__(self, master, name: str, on_click: Callable):
        super().__init__(master)

        self.grid_columnconfigure(1, weight=1)

        ttk.Label(self, text=name).grid(row=0, column=0, sticky="w")
        ttk.Button(self, text=">", command=on_click).grid(
            row=0, column=2, sticky="e"
        )

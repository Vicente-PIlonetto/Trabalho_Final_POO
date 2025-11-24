from functools import partial
from tkinter import Frame, ttk
from typing import Callable

from components.link import Link
from database import db
from functions import wrapper
from models.usuario import Usuario


class Compra_view(Frame):
    def __init__(self, master, user, go_to: Callable):
        super().__init__(master)

        Link(self, "Geral", lambda: go_to("/compras", 0, user)).pack(fill="x")
        self._pack_separator()

        self.links_frame = Frame(self)
        self.links_frame.pack()
        self.links_frame.pack(fill="x")

        ttk.Button(
            self, text="Voltar", command=lambda: go_to("/index", user), width=30
        ).pack(fill="x")

        wrapper(self.get_links, go_to, user)

    def _pack_separator(self):
        return ttk.Separator(self, orient="horizontal").pack(fill="x")

    async def get_links(self, go_to: Callable, user: Usuario):
        arr = await db.load_product_types_with_items()

        for widget in self.links_frame.winfo_children()[2:]:
            widget.destroy()

        for val in arr:
            Link(
                self.links_frame, val[1], partial(go_to, "/compras", val[0], user)
            ).pack(fill="x")
            ttk.Separator(self.links_frame, orient="horizontal").pack(fill="x")

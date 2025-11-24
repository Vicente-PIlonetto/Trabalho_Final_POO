from tkinter import Frame, ttk
from typing import Callable, ParamSpec

from components import Link
from constraints import CARGOS_IDS
from models.usuario import Cliente, Fornecedor, Funcionario, Usuario

PRODUCTS = 0
HIST_PRODUCTS = 1
CARRINHO = 2

ALL_LINKS = (PRODUCTS, HIST_PRODUCTS, CARRINHO)


class Index_view(Frame):
    def __init__(self, master, user: Usuario, go_to: Callable):
        super().__init__(master)

        self.user = user

        is_adm = isinstance(user, Funcionario) and user.cargo == CARGOS_IDS[1]
        items = set([PRODUCTS])

        if isinstance(user, Cliente) or is_adm:
            items.add(HIST_PRODUCTS)
            items.add(CARRINHO)
        if isinstance(user, Funcionario):
            pass
        if isinstance(user, Fornecedor) or is_adm:
            pass

        for i in ALL_LINKS:
            if i in items:
                if i == PRODUCTS:
                    Link(self, "Compras", lambda: go_to("/compras", None, user)).pack(
                        fill="x"
                    )
                elif i == HIST_PRODUCTS:
                    Link(
                        self,
                        "Histórico de compras",
                        lambda: go_to("/historico-compras", user),
                    ).pack(fill="x")
                elif i == CARRINHO:
                    Link(self, "Carrinho", lambda: go_to("/carrinho", user)).pack(
                        fill="x"
                    )

            ttk.Separator(self, orient="horizontal").pack(fill="x", pady=10)

        ttk.Button(self, text="Sair", command=lambda: go_to("/login"), width=40).pack()

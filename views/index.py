from tkinter import Frame, ttk
from typing import Callable

from components import Link
from constraints import CARGOS_IDS
from models.usuario import Cliente, Fornecedor, Funcionario, Usuario

PRODUCTS = 0
HIST_PRODUCTS = 1
CARRINHO = 2
CADASTRO_PRODUTOS = 3

ALL_LINKS = (PRODUCTS, HIST_PRODUCTS, CARRINHO, CADASTRO_PRODUTOS)


class Index_view(Frame):
    def __init__(self, master, user: Usuario, go_to: Callable):
        super().__init__(master)

        self.user = user

        items = set([PRODUCTS])

        if isinstance(user, Cliente):
            items.add(CARRINHO)
        elif isinstance(user, Funcionario):
            items.add(CADASTRO_PRODUTOS)

        for i in ALL_LINKS:
            added = False
            if i in items:
                if i == PRODUCTS:
                    Link(self, "Compras", lambda: go_to("/compras", None, user)).pack(
                        fill="x"
                    )
                    added = True
                elif i == HIST_PRODUCTS:
                    Link(
                        self,
                        "Histórico de compras",
                        lambda: go_to("/historico-compras", user),
                    ).pack(fill="x")
                    added = True
                elif i == CARRINHO:
                    Link(self, "Carrinho", lambda: go_to("/carrinho", user)).pack(
                        fill="x"
                    )
                    added = True
                elif i == CADASTRO_PRODUTOS:
                    Link(
                        self,
                        "Cadastrar produto",
                        lambda: go_to("/cadastro_produto", user),
                    ).pack(fill="x")
                    added = True
            if added:
                ttk.Separator(self, orient="horizontal").pack(fill="x", pady=10)

        ttk.Button(self, text="Sair", command=lambda: go_to("/login"), width=40).pack()

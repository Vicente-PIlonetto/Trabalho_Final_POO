from tkinter import Frame, ttk
from typing import Callable

from components import Link
from models.usuario import Cliente, Funcionario, Usuario

PRODUCTS = 0
HIST_PRODUCTS = 1
CARRINHO = 2
CADASTRO_PRODUTOS = 3
CADASTRO_USUARIOS = 4
PEDIDOS = 5

ALL_LINKS = (PRODUCTS, HIST_PRODUCTS, CARRINHO, CADASTRO_PRODUTOS, CADASTRO_USUARIOS, PEDIDOS)


class Index_view(Frame):
    def __init__(self, master, user: Usuario, go_to: Callable):
        super().__init__(master)

        self.user = user

        items = set([PRODUCTS])

        if isinstance(user, Cliente):
            items.add(CARRINHO)
        elif isinstance(user, Funcionario):
            items.add(CADASTRO_PRODUTOS)
            items.add(PEDIDOS)

            if user.cargo == 1:
                items.add(CADASTRO_USUARIOS)
        else:
            items.add(PEDIDOS)

        added = False
        for i in items:
            if added:
                ttk.Separator(self, orient="horizontal").pack(fill="x", pady=10)
            else:
                added = True

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
                Link(self, "Carrinho", lambda: go_to("/carrinho", user)).pack(fill="x")
            elif i == CADASTRO_PRODUTOS:
                Link(
                    self,
                    "Cadastrar produto",
                    lambda: go_to("/cadastro_produto", user),
                ).pack(fill="x")
            elif i == CADASTRO_USUARIOS:
                Link(
                    self,
                    "Cadastrar usuário",
                    lambda: go_to("/sign_up", user),
                ).pack(fill="x")
            elif i == PEDIDOS:
                Link(
                    self,
                    "Lista Pedidos",
                    lambda: go_to("/pedidos", user),
                ).pack(fill="x")

        ttk.Button(self, text="Sair", command=lambda: go_to("/login"), width=40).pack(pady=(10, 0))

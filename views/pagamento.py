from typing import Callable
from functions import wrapper
from models import Cliente
from tkinter import ttk, Frame
from database import db


class Pagamento_view(Frame):
    def __init__(self, master, user: Cliente, go_to: Callable):
        super().__init__(master)
        self.user = user

        ttk.Label(
            self, text=f"R$ {sum(map(lambda x: x.preco, user.carrinho.produtos))}"
        ).pack(fill="both")

        ttk.Button(
            self, text="Finalizar", command=lambda: wrapper(self.realizar_pedido, go_to)
        ).pack(fill="x")
        ttk.Button(self, text="Cancelar", command=lambda: go_to("/carrinho")).pack(
            fill="x"
        )

    async def realizar_pedido(self, go_to: Callable):
        sucess = await db.insert_pedido(self.user.id_usuario, self.user.carrinho)
        if sucess:
            go_to("/carrinho")

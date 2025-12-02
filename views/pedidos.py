import asyncio
from tkinter import ttk, Frame, Label, Button
from tkinter import BOTH, LEFT, X, Y, RIGHT
from typing import Callable
from functions import wrapper
from models import Usuario
from database import db
from models.usuario import Fornecedor, Funcionario


class Pedidos_view(Frame):
    def __init__(self, master, usuario: Usuario, back: Callable):
        super().__init__(master)
        self.usuario = usuario
        self.pedidos_carregados = False

        if isinstance(usuario, Fornecedor):
            wrapper(self.load_pedidos, 0, 1)
        elif isinstance(usuario, Funcionario):
            wrapper(self.load_pedidos)

        ttk.Button(self, text="Voltar", command=lambda*args:back("/index", usuario)).pack(fill="x")
        self.create_widgets()

    def create_widgets(self):

        table_frame = Frame(self)
        table_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)

        columns = ("id", "usuario", "tipo", "completo", "valor")

        self.tree = ttk.Treeview(
            table_frame, columns=columns, show="headings", height=15
        )

        self.tree.heading("id", text="ID do Pedido")
        self.tree.heading("usuario", text="Usuário")
        self.tree.heading("tipo", text="Tipo")
        self.tree.heading("completo", text="Estado")
        self.tree.heading("valor", text="Valor Total")

        self.tree.column("id", width=100)
        self.tree.column("usuario", width=100)
        self.tree.column("tipo", width=100)
        self.tree.column("completo", width=100)
        self.tree.column("valor", width=120)

        scrollbar = ttk.Scrollbar(
            table_frame, orient="vertical", command=self.tree.yview
        )
        self.tree.configure(yscroll=scrollbar.set)

        self.tree.pack(side=LEFT, fill=BOTH, expand=True)
        scrollbar.pack(side=RIGHT, fill=Y)
        if not self.pedidos_carregados:
            wrapper(self.load_pedidos)
            self.pedidos_carregados = True

    async def load_pedidos(self, completo=None, tipo=None):
        for item in self.tree.get_children():
            self.tree.delete(item)

        pedidos = await db.listar_pedidos(completo, tipo)

        for p in pedidos:
            self.tree.insert(
                "",
                "end",
                values=(
                    p["id_pedido"],
                    p["id_usuario"],
                    p["tipo"],
                    "Finalizado" if p["completo"] else "Aguardando",
                    f"R$ {p['valor_total']:.2f}",
                ),
            )

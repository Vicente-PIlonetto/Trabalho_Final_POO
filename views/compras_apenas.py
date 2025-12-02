from tkinter import Frame, ttk, CENTER
from typing import Callable
from functions import wrapper
from models.produto import Alimento, Eletronico, Produto, Roupas
from models.usuario import Cliente, Usuario
from database import db


class Compras_apenas_view(Frame):
    def __init__(self, master, type: int, user: Usuario, go_to: Callable):
        super().__init__(master)
        self.type = type

        self.is_client = isinstance(user, Cliente)

        cls = Produto
        if type == 1:
            cls = Alimento
        elif type == 2:
            cls = Eletronico
        elif type == 3:
            cls = Roupas

        columns = cls.COLUMNS

        ttk.Button(
            self, text="Voltar", command=lambda: go_to("/compras", None, user)
        ).grid(row=0, column=0, columnspan=2, sticky="ew", pady=5)

        self.table = ttk.Treeview(
            self, columns=tuple(map(lambda x: x[0], columns)), show="headings"
        )
        self.table.grid(row=1, column=0, sticky="nsew")

        scrollbar_vertical = ttk.Scrollbar(
            self, orient="vertical", command=self.table.yview
        )
        self.table.configure(yscrollcommand=scrollbar_vertical.set)
        scrollbar_vertical.grid(row=1, column=1, sticky="ns")

        for col in columns:
            self.table.heading(col[0], text=col[0])
            self.table.column(col[0], width=col[1], anchor=CENTER)

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        wrapper(self.get_products, user)

    def _add_cart(self, user: Cliente, qnt: int):
        is_geral = None
        selected_items = self.table.selection()
        for item_id in selected_items:
            values = self.table.item(item_id)["values"]
            is_geral = isinstance(values[-1], str) and values[-1][-1] == "%"
            i_qnt = 5 if is_geral else 4
            i_preco = 3 if is_geral else 2
            if values[i_qnt] >= qnt:
                user.carrinho.adicionar_produto(values[0], qnt, values[i_preco])
                values[i_qnt] -= qnt
                self.table.item(item_id, values=values)

    async def get_products(self, user: Usuario):
        self.dados = await db.load_products(self.type)

        for item in self.dados:
            values = item.to_tuple()
            item_id = values[0]

            if self.is_client and user.carrinho.produtos.get(item_id):
                carrinho_qtd = user.carrinho.produtos[item_id][0]
                i = 5 if isinstance(values[-1], str) and values[-1][-1] == "%" else 4

                new_val5 = values[i] - carrinho_qtd

                values = values[:i] + (new_val5,) + values[i + 1 :]

            self.table.insert("", "end", values=values)

        if self.is_client:
            frame = Frame(self)

            ttk.Button(
                frame, text="+ Cart", command=lambda: self._add_cart(user, 1)
            ).pack(fill="x")
            ttk.Button(
                frame, text="+5 Cart", command=lambda: self._add_cart(user, 5)
            ).pack(fill="x")
            frame.grid(row=2, column=0, sticky="ew")

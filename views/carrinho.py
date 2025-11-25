from tkinter import Frame, ttk, CENTER
from typing import Callable
from functions import wrapper
from models.produto import Produto
from models.usuario import Cliente, Usuario
from database import db


class Carrinho_view(Frame):
    def __init__(self, master, user: Cliente, go_to: Callable):
        super().__init__(master)
        self.user = user

        columns = Produto.COLUMNS

        ttk.Button(self, text="Voltar", command=lambda: go_to("/index", user)).grid(
            row=0, column=0, columnspan=2, sticky="ew", pady=5
        )

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

        wrapper(self.get_products)

    def _remove_cart(self, qnt: int):
        selected_items = self.table.selection()
        for item_id in selected_items:
            values = self.table.item(item_id)["values"]
            if values[5] >= qnt:
                self.user.carrinho.adicionar_produto(values[0], qnt)
                values[5] -= qnt
                self.table.item(item_id, values=values)

    async def get_products(self):
        self.dados = await db.load_products_id(
            tuple(self.user.carrinho.produtos.keys())
        )

        for item in self.dados:
            values = item.to_tuple()
            item_id = values[0]

            if self.user.carrinho.produtos.get(item_id):
                carrinho_qtd = self.user.carrinho.produtos[item_id]
                i = 5 if isinstance(values[-1], str) and values[-1][-1] == "%" else 4

                if carrinho_qtd > values[i]:
                    self.user.carrinho.produtos[item_id] = values[index_qnt]
                    new_val = 0
                else:
                    new_val = max(0, values[i] - carrinho_qtd)

                values = values[:i] + (new_val,) + values[i + 1 :]
            else:
                values = values

            self.table.insert("", "end", values=values)

        frame = Frame(self)

        ttk.Button(frame, text="- Cart", command=lambda: self._remove_cart(1)).pack(
            fill="x"
        )
        ttk.Button(frame, text="-5 Cart", command=lambda: self._remove_cart(5)).pack(
            fill="x"
        )
        if len(self.user.carrinho.produtos):
            ttk.Button(
                frame, text="Finalizar compra", command=lambda: self._remove_cart(5)
            ).pack(fill="x")
        frame.grid(row=2, column=0, sticky="ew")

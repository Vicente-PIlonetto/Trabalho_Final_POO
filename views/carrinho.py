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

        ttk.Button(
            self, text="Voltar", command=lambda: go_to("/index", None, user)
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

    def _remove_cart(self, qnt: int):
        selected_items = self.table.selection()
        for item_id in selected_items:
            values = self.table.item(item_id)["values"]
            if values[5] >= qnt:
                user.carrinho.adicionar_produto(values[0], qnt)
                values[5] -= qnt
                self.table.item(item_id, values=values)

    async def get_products(self):
        self.dados = await db.load_products(tuple(self.user.carrinho.produtos.keys()))
        for dado in dados:
            pass


        for item in self.dados:
            old_values = item.to_tuple()
            item_id = old_values[0]

            if self.is_client and user.carrinho.produtos.get(item_id):
                carrinho_qtd = user.carrinho.produtos[item_id]

                if carrinho_qtd > old_values[5]:
                    user.carrinho.produtos[item_id] = old_values[5]
                    new_val5 = 0
                else:
                    new_val5 = max(0, old_values[5] - carrinho_qtd)

                values = old_values[:5] + (new_val5,) + old_values[6:]
            else:
                values = old_values

            self.table.insert("", "end", values=values)

        if self.is_client:
            frame = Frame(self)

            ttk.Button(
                frame, text="- Cart", command=lambda: self._remove_cart(user, 1)
            ).pack(fill="x")
            ttk.Button(
                frame, text="-5 Cart", command=lambda: self._remove_cart(user, 5)
            ).pack(fill="x")
            frame.grid(row=2, column=0, sticky="ew")

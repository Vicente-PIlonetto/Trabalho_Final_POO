import asyncio
from tkinter import Frame
from tkinter import ttk
from typing import Callable

from constraints import TIPOS_USUARIO_IDS
from functions import wrapper
from models import usuario
from models.usuario import Cliente, Fornecedor, Funcionario, Usuario
from database import db


class Login_view(Frame):
    def __init__(
        self,
        master,
        on_sign_up_click: Callable,
        on_login_click: Callable[[Usuario], None],
    ) -> None:
        super().__init__(master)
        self.on_login_click = on_login_click

        self.label = ttk.Label(self, text="Nome:")
        self.label.grid(row=0, column=0, padx=5, pady=5)

        self.name_entry = ttk.Entry(self)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5)

        self.label = ttk.Label(self, text="Senha:")
        self.label.grid(row=1, column=0, padx=5, pady=5)

        self.password_entry = ttk.Entry(self, show="*")
        self.password_entry.grid(row=1, column=1, padx=5, pady=5)

        self.label_error = ttk.Label(self, foreground="red")
        self.label_error.grid(row=2, columnspan=2)

        _frame = Frame(self)

        self.login_btn = ttk.Button(
            _frame, text="Login", command=lambda: wrapper(self._on_login_click)
        )
        self.login_btn.pack(side="left")

        self.signup_btn = ttk.Button(_frame, text="Sign up", command=on_sign_up_click)
        self.signup_btn.pack(side="right")

        _frame.grid(row=3, columnspan=2)

    async def _on_login_click(self):
        res = await self._validade()
        error = ""

        if isinstance(res, tuple):
            user_type = res[4]
            usuario = None
            if TIPOS_USUARIO_IDS[0] == user_type:
                usuario = Cliente(res[1], res[3], res[7])
            elif TIPOS_USUARIO_IDS[1] == user_type:
                usuario = Funcionario(res[1], res[3], res[5], res[6])
            elif TIPOS_USUARIO_IDS[2] == user_type:
                usuario = Fornecedor(res[1], res[3])
            usuario.id_usuario = res[0]

            return self.on_login_click(usuario)
        else:
            if res == 0:
                error = "Usuário precisa de ao menos 5 caracters"
            elif res == 1:
                error = "Senha precisa de ao menos 5 caracters"
            elif res == 2:
                error = "Usuário ou senha inválidos"

        self.label_error.config(text=error)

    async def _validade(self):
        if len(self.name_entry.get()) < 5:
            return 0
        elif len(self.password_entry.get()) < 5:
            return 1
        res = await db.login(self.name_entry.get(), self.password_entry.get())

        if not res:
            return 2

        return res

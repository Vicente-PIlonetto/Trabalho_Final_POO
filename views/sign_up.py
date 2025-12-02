from tkinter import Frame, ttk
from datetime import datetime
from typing import Callable

from components.default_input import Default_input
from constraints import (
    CARGOS,
    CARGOS_IDS,
    TIPOS_USUARIO,
    TIPOS_USUARIO_IDS,
)
from functions import possui_digitos, possui_letras, wrapper
from database import db
from globals import INFOS_PADAO
from utils import is_float


class Sign_up_view(Frame):

    def __init__(self, master, back: Callable) -> None:
        super().__init__(master)
        self.__back = back

        self.name_input = Default_input(self, "Nome:")
        self.name_input.grid(row=0, columnspan=2)

        self.password_input = Default_input(self, "Senha:", "password")
        self.password_input.grid(row=1, columnspan=2)

        self.confirm_password = Default_input(self, "Confirmar senha:", "password")
        self.confirm_password.grid(row=2, columnspan=2)

        self.born_date_input = Default_input(self, "Data Nascimento:", "date")
        self.born_date_input.grid(row=3, columnspan=2)

        self.user_type = Default_input(
            self,
            "Tipo usuario:",
            "combo",
            TIPOS_USUARIO,
            lambda *args: self._change_tipo_usuario(),
            default_value="Funcionário" if INFOS_PADAO["primeiro_usuario"] else None,
            block=INFOS_PADAO["primeiro_usuario"],
        )
        self.user_type.grid(row=4, columnspan=2)

        self.current_user_infos = ttk.Frame(self)
        self.cargo_input = Default_input(
            self.current_user_infos,
            "Cargo",
            "combo",
            CARGOS,
            default_value="Administrador" if INFOS_PADAO["primeiro_usuario"] else None,
            block=INFOS_PADAO["primeiro_usuario"],
        )
        self.salario_input = Default_input(self.current_user_infos, "Salario:", "float")
        self.cargo_input.pack(fill="x")
        self.salario_input.pack(fill="x")

        if INFOS_PADAO["primeiro_usuario"]:
            self._change_tipo_usuario(False)

        self.label_error = ttk.Label(self, foreground="red")
        self.label_error.grid(row=7, columnspan=2)

        frame = Frame(self)
        btn = ttk.Button(
            frame, text="Criar Conta", command=lambda: wrapper(self.sign_up)
        )
        if not INFOS_PADAO["primeiro_usuario"]:
            ttk.Button(frame, text="Voltar", command=back).grid(row=0, column=0)
            btn.grid(row=0, column=1)
        else:
            btn.pack()
        frame.grid(row=8, columnspan=2)

    async def sign_up(self):
        error = None
        name = self.name_input.get()
        password = self.password_input.get()
        password2 = self.confirm_password.get()
        born_dt = self.born_date_input.get()
        user_type = int(self.user_type.get())
        cargo = None
        salario = None

        if len(name) < 5:
            error = "Usuário precisa ter ao menos 5 caracteres"
        elif len(password) < 5:
            error = "Senha precisa ter ao menos 5 caracteres"
        elif password != password2:
            error = "As 2 senhas precisam ser iguais"
        elif not possui_digitos(password):
            error = "Adicione ao menos 1 número na senha"
        elif not possui_letras(password):
            error = "Adicione ao menos 1 letra na senha"
        elif "_" in born_dt:
            error = "Preencha a data de nascimento"
        elif user_type == 1:
            cargo = self.cargo_input.get()
            salario = float(self.salario_input.get())

            if salario < 0:
                error = "Salário negativo"

            else:
                salario = float(salario)
                cargo = CARGOS_IDS[cargo]

        user_type = TIPOS_USUARIO_IDS[user_type]

        if not error:
            dt = int(datetime.strptime(born_dt, "%d/%m/%Y").timestamp() * 1000)

            duplicado = await db.varificar_usuario_duplicado(name, dt)
            if duplicado:
                error = "usuario já cadastrado"
            else:
                res = await db.insert_user(
                    name, password, dt, user_type, salario, cargo
                )
                if res == -1:
                    error = "Falha ao cadastrar o usuario"
                else:
                    self.__back()

        if error:
            self.label_error.configure(text=error)

    def _change_tipo_usuario(self, deletar=True):
        tipo = self.user_type.get()

        if deletar and tipo != TIPOS_USUARIO[1]:
            self.current_user_infos.grid_forget()

        if tipo == 1:
            self.current_user_infos.grid(row=5, column=0, columnspan=2, sticky="ew")

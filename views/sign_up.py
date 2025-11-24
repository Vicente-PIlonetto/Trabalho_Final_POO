from tkinter import Frame, Event, StringVar, ttk
from datetime import datetime
from typing import Callable

from constraints import (
    CARGOS,
    CARGOS_IDS,
    DATA_PADRAO,
    TIPOS_USUARIO,
    TIPOS_USUARIO_IDS,
)
from functions import date_mask, possui_digitos, possui_letras, wrapper
from models.usuario import Cliente, Funcionario, Usuario
from database import db
from utils import is_float


class Sign_up_view(Frame):

    def __init__(self, master, on_sign_up: Callable) -> None:
        super().__init__(master)
        self.__on_sign_up = on_sign_up
        self.born_date = StringVar(None, DATA_PADRAO)

        # Nome:
        ttk.Label(self, text="Nome:").grid(row=0, column=0, padx=5, pady=5)
        self.name_entry = ttk.Entry(self)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5)

        # Senha:
        ttk.Label(self, text="Senha:").grid(row=1, column=0, padx=5, pady=5)
        self.password_entry = ttk.Entry(self, show="*")
        self.password_entry.grid(row=1, column=1, padx=5, pady=5)

        # Confirmação
        ttk.Label(self, text="Confirmar senha:").grid(row=2, column=0, padx=5, pady=5)
        self.confirm_password = ttk.Entry(self, show="*")
        self.confirm_password.grid(row=2, column=1, padx=5, pady=5)

        # dt nascimento
        ttk.Label(self, text="Data Nascimento:").grid(row=3, column=0, padx=5, pady=5)
        self.born_date_entry = ttk.Entry(self, textvariable=self.born_date)
        self.born_date_entry.grid(row=3, column=1, padx=5, pady=5)
        self.born_date.trace_add(
            "write", lambda *args: date_mask(self.born_date_entry, self.born_date)
        )

        # Tipo usuario r=4
        ttk.Label(self, text="Tipo usuario:").grid(row=4, column=0, padx=5, pady=5)
        self.user_type = ttk.Combobox(
            self,
            values=TIPOS_USUARIO,
            state="readonly",
        )
        self.user_type.set(TIPOS_USUARIO[0])
        self.user_type.grid(row=4, column=1)
        self.user_type.bind("<<ComboboxSelected>>", self._change_tipo_usuario)

        self.current_user_infos = ttk.Frame(self)
        self.salario_entry = ttk.Entry(self.current_user_infos)
        self.cargo_combo = ttk.Combobox(
            self.current_user_infos, values=CARGOS, state="readonly"
        )
        self.cargo_combo.set(CARGOS[0])

        # Erro r=7
        self.label_error = ttk.Label(self, foreground="red")
        self.label_error.grid(row=7, columnspan=2)

        self.login_btn = ttk.Button(
            self, text="Criar Conta", command=lambda: wrapper(self.sign_up)
        )
        self.login_btn.grid(row=8, column=0)

    async def sign_up(self):
        error = None
        name = self.name_entry.get()
        password = self.password_entry.get()
        password2 = self.confirm_password.get()
        born_dt = self.born_date.get()
        user_type = self.user_type.get()
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
        elif user_type == TIPOS_USUARIO[1]:
            cargo = self.cargo_combo.get()
            salario = self.salario_entry.get()

            if not is_float(salario):
                error = "Salário não é um decimal"

            else:
                salario = float(salario)
                cargo = CARGOS_IDS[CARGOS.index(cargo)]

        user_type = TIPOS_USUARIO_IDS[TIPOS_USUARIO.index(user_type)]

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
                    self.__on_sign_up()

        if error:
            self.label_error.configure(text=error)

    def _change_tipo_usuario(self, _):
        tipo = self.user_type.get()

        if self.current_user_infos and tipo != TIPOS_USUARIO[1]:
            self.current_user_infos.destroy()

        if tipo == TIPOS_USUARIO[1]:
            frame = self.current_user_infos

            ttk.Label(frame, text="Cargo:").grid(row=0, column=0)
            ttk.Label(frame, text="Salário:").grid(row=1, column=0)

            self.cargo_combo.grid(row=0, column=1)
            self.salario_entry.grid(row=1, column=1)

            frame.grid(row=5, columnspan=2, column=0)

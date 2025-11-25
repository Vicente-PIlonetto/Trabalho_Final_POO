from tkinter import Entry, Frame, StringVar, ttk
from typing import Callable

from constraints import DATA_PADRAO, ITEM_TYPES
from functions import date_mask
from models.usuario import Funcionario
from utils import is_float
from datetime import datetime


class Cadastro_produto_view(Frame):

    def __init__(self, master, user: Funcionario, go_to: Callable) -> None:
        super().__init__(master)
        self._current_tipo = "Padrão"
        self.__back = lambda: go_to("/index", user)

        ttk.Label(self, text="Nome:").grid(row=0, column=0, padx=5, pady=5)
        self.nome_entry = ttk.Entry(self)
        self.nome_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(self, text="Quantidade:").grid(row=1, column=0, padx=5, pady=5)
        self.qnt_entry = ttk.Entry(self)
        self.qnt_entry.grid(row=1, column=1)

        ttk.Label(self, text="Preço:").grid(row=2, column=0, padx=5, pady=5)
        self.preco_entry = ttk.Entry(self)
        self.preco_entry.grid(row=2, column=1)

        ttk.Label(self, text="Fabricante(ID):").grid(row=3, column=0, padx=5, pady=5)
        self.fabricante_entry = ttk.Entry(self)
        self.fabricante_entry.grid(row=3, column=1)

        ttk.Label(self, text="NCM(%):").grid(row=4, column=0, padx=5, pady=5)
        self.ncm_entry = ttk.Entry(self)
        self.ncm_entry.grid(row=4, column=1)

        ttk.Label(self, text="Tipo de produto:").grid(row=5, column=0, padx=5, pady=5)
        self.tipo_combo = ttk.Combobox(
            self,
            values=("Padrão",) + tuple(map(lambda x: x[1], ITEM_TYPES)),
            state="readonly",
        )
        self.tipo_combo.set("Padrão")
        self.tipo_combo.grid(row=5, column=1)
        self.tipo_combo.bind("<<ComboboxSelected>>", self._change_tipo_produto)

        self.current_prod_infos = ttk.Frame(self)

        self.validade_entry: Entry = None

        self.tensao_entry: Entry = None
        self.potencia_entry: Entry = None

        self.tamanho_entry: Entry = None
        self.tipo_roupa_entry: Entry = None
        self.tecido_entry: Entry = None
        self.cor_entry: Entry = None
        self.estampa_entry: Entry = None
        self.genero_entry: Entry = None

        self.ano_entry: Entry = None
        self.marca_entry: Entry = None
        self.funcao_entry: Entry = None
        self.tipo_eletro_entry: Entry = None

        self.label_error = ttk.Label(self, foreground="red")
        self.label_error.grid(row=20, columnspan=2)

        frame = Frame(self)
        ttk.Button(frame, text="Voltar", command=self.__back).grid(row=0, column=0)
        ttk.Button(frame, text="Salvar", command=self.save).grid(row=0, column=1)
        frame.grid(row=21, columnspan=2)

    def save(self):
        error = None

        nome = self.nome_entry.get()
        qnt = self.qnt_entry.get()
        preco = self.preco_entry.get()
        fabricante = self.fabricante_entry.get()
        ncm = self.ncm_entry.get()
        tipo = self.tipo_combo.get()

        if len(nome) < 2:
            error = "Nome muito curto"
        elif not qnt.isdigit():
            error = "Quantidade inválida"
        elif not is_float(preco):
            error = "Preço inválido"
        elif not fabricante.isdigit():
            error = "Fabricante deve ser ID numérico"
        elif not is_float(ncm):
            error = "NCM inválido"
        else:
            dados_especificos = {}

            if ITEM_TYPES[0][1] == tipo:
                tipo = ITEM_TYPES[0][0]

                data_validade = self.validade_entry.get()
                if "_" in data_validade:
                    error = "Data validade não completamente preenchida"
                else:
                    dados_especificos["data_validade"] = data_validade

            elif ITEM_TYPES[1][1] == tipo:
                tensao = self.tensao_entry.get()
                potencia = self.potencia_entry.get()

                if not tensao or not tensao.isdigit():
                    error = "Tensão não é u número inteiro"
                elif not potencia or not potencia.isdigit():
                    error = "Potência não é u número inteiro"
                else:
                    dados_especificos["tensao"] = int(tensao)
                    dados_especificos["potencia"] = int(potencia)
            elif ITEM_TYPES[2][1] == tipo:
                tamanho =self.tamanho_entry.get()
                cloatch_tipo =self.tipo_roupa_entry.get()
                tecido =self.tecido_entry.get()
                cor =self.cor_entry.get()
                estampa =self.estampa_entry.get()
                genero = self.genero_entry.get()

                if not tamanho or not tamanho.isdigit():
                    error = "Tamanho não é um número"

                dados_especificos.update(
                    dict(
                        tamanho=int(),
                        tipo=cloatch_tipo,
                        tecido=int(),
                        cor=int(),
                        estampa=int(),
                        genero=int(),
                    )
                )

        # elif t == "Eletrodoméstico":

        #     if not self.ano_entry.get().isdigit():
        #         error = "Ano inválido"

        #     dados_especificos.update(
        #         dict(
        #             ano_lancamento=int(self.ano_entry.get()),
        #             marca=self.marca_entry.get(),
        #             funcao=self.funcao_entry.get(),
        #             tipo=int(self.tipo_eletro_entry.get()),
        #         )
        #     )

        if error:
            self.label_error.configure(text=error)
            return

        self.__back()

    def _change_tipo_produto(self, _):
        tipo = self.tipo_combo.get()

        if self.current_prod_infos:
            self.current_prod_infos.destroy()
            if self._current_tipo == ITEM_TYPES[0][1]:
                del self._data_validade

        frame = ttk.Frame(self)
        self.current_prod_infos = frame

        if tipo == ITEM_TYPES[0][1]:
            self._data_validade = StringVar(None, DATA_PADRAO)
            ttk.Label(frame, text="Data validade (DD/MM/AAAA):").grid(
                row=0, column=0, padx=5, pady=5
            )
            self.validade_entry = ttk.Entry(frame, textvariable=self._data_validade)
            self.validade_entry.grid(row=0, column=1, padx=5, pady=5)
            self._data_validade.trace_add(
                "write",
                lambda *args: date_mask(self.validade_entry, self._data_validade),
            )

        elif tipo == ITEM_TYPES[1][1]:
            ttk.Label(frame, text="Tensão:").grid(row=0, column=0, padx=5, pady=5)
            ttk.Label(frame, text="Potência:").grid(row=1, column=0, padx=5, pady=5)

            self.tensao_entry = ttk.Entry(frame)
            self.potencia_entry = ttk.Entry(frame)
            self.tensao_entry.grid(row=0, column=1, padx=5, pady=5)
            self.potencia_entry.grid(row=1, column=1, padx=5, pady=5)

        elif tipo == ITEM_TYPES[2][1]:
            self.tamanho_entry = ttk.Entry(frame)
            self.tipo_roupa_entry = ttk.Entry(frame)
            self.tecido_entry = ttk.Entry(frame)
            self.cor_entry = ttk.Entry(frame)
            self.estampa_entry = ttk.Entry(frame)
            self.genero_entry = ttk.Combobox(
                frame, width=2, values=("H", "M"), state="readonly"
            )

            entries = (
                self.tamanho_entry,
                self.tipo_roupa_entry,
                self.tecido_entry,
                self.cor_entry,
                self.estampa_entry,
                self.genero_entry,
            )
            for i, label in enumerate(
                ("Tamanho", "Tipo", "Tecido", "Cor", "Estampa", "Gênero")
            ):
                ttk.Label(frame, text=f"{label}:").grid(row=i, column=0, padx=5, pady=5)
                entries[i].grid(row=i, column=1, padx=5, pady=5, sticky="E")

        elif tipo == ITEM_TYPES[3][1]:
            self.ano_entry = ttk.Entry(frame)
            self.marca_entry = ttk.Entry(frame)
            self.funcao_entry = ttk.Entry(frame)
            self.tipo_eletro_entry = ttk.Entry(frame)

            entries = (
                self.ano_entry,
                self.marca_entry,
                self.funcao_entry,
                self.tipo_eletro_entry,
            )
            for i, label in enumerate(("Ano", "Marca", "Função", "Tipo interno")):
                ttk.Label(frame, text=f"{label}:").grid(row=i, column=0, padx=5, pady=5)
                entries[i].grid(row=i, column=1, padx=5, pady=5)

        frame.grid(row=10, columnspan=2)

        self._current_tipo = tipo

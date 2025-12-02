from datetime import datetime
from tkinter import Frame, ttk
from typing import Callable

from components.default_input import Default_input
from functions import wrapper
from globals import FABRICANTES, ITEM_TYPES
from models.produto import Alimento, Eletrodomestico, Eletronico, Produto, Roupas
from models.usuario import Funcionario
from utils import is_float
from database import db

TIPOS_TECIDO = ("Algodão", "Seda", "Cheta")


class Cadastro_produto_view(Frame):

    def __init__(self, master, user: Funcionario, go_to: Callable) -> None:
        super().__init__(master)
        self._current_tipo = "Padrão"
        self.__back = lambda: go_to("/index", user)

        self.nome_input = Default_input(self, "Nome:")
        self.nome_input.grid(row=0)

        self.qnt_input = Default_input(self, "Quantidade", "int")
        self.qnt_input.grid(row=1)

        self.preco_entry = Default_input(self, "Preço:", "float")
        self.preco_entry.grid(row=2)

        self.fabricante_entry = Default_input(
            self, "Fabricante", "combo", tuple(map(lambda x: x[1], FABRICANTES))
        )
        self.fabricante_entry.grid(row=3)

        self.ncm_entry = Default_input(self, "NCM(%):", "float")
        self.ncm_entry.grid(row=4)

        self.tipo_combo = Default_input(
            self,
            "Tipo de produto:",
            "combo",
            ("Padrão",) + tuple(map(lambda x: x[1], ITEM_TYPES)),
            lambda *args: self._change_tipo_produto(),
        )
        self.tipo_combo.grid(row=5)

        self.tipo_combo.bind("<<ComboboxSelected>>", self._change_tipo_produto)

        self.current_prod_infos = ttk.Frame(self)

        self.validade_entry: Frame = None

        self.tensao_entry: Frame = None
        self.potencia_entry: Frame = None

        self.tamanho_entry: Frame = None
        self.tipo_roupa_entry: Frame = None
        self.tecido_combo: Frame = None
        self.cor_entry: Frame = None
        self.estampa_entry: Frame = None
        self.genero_entry: Frame = None

        self.ano_entry: Frame = None
        self.marca_entry: Frame = None
        self.funcao_entry: Frame = None
        self.tipo_eletro_entry: Frame = None

        self.label_error = ttk.Label(self, foreground="red")
        self.label_error.grid(row=20, columnspan=2)

        frame = Frame(self)
        ttk.Button(frame, text="Voltar", command=self.__back).grid(row=0, column=0)
        ttk.Button(frame, text="Salvar", command=lambda *args: wrapper(self.save)).grid(
            row=0, column=1
        )
        frame.grid(row=21, columnspan=2)

    async def save(self):
        produto: Produto | None = None
        error = None

        nome = str(self.nome_input.get())
        qnt = int(self.qnt_input.get() or "0")
        preco: float = float(self.preco_entry.get() or "0")
        fabricante = int(self.fabricante_entry.get())
        ncm = float(self.ncm_entry.get() or "0")
        tipo = self.tipo_combo.get()

        if len(nome) < 2:
            error = "Nome muito curto"
        elif qnt < 0:
            error = "Quantidade negativa!"
        elif preco < 0:
            error = "Preço negativo"
        elif ncm < 0:
            error = "NCM Negativo"
        else:
            dados_especificos = {}

            if ITEM_TYPES[0][1] == tipo:
                data_validade = self.validade_entry.get()
                if "_" in data_validade:
                    error = "Data validade não completamente preenchida"
                else:
                    dados_especificos["data_validade"] = data_validade
                    produto = Alimento(
                        0,
                        nome,
                        qnt,
                        preco,
                        fabricante,
                        float(ncm) / 100,
                        int(datetime.strptime(data_validade, "%d/%m/%Y").timestamp()),
                    )

            elif ITEM_TYPES[1][1] == tipo:
                tensao = int(self.tensao_entry.get())
                potencia = int(self.potencia_entry.get())

                if tensao < 0:
                    error = "Tensão negativa"
                elif potencia < 0:
                    error = "Potência negativa"
                else:
                    dados_especificos["tensao"] = tensao
                    dados_especificos["potencia"] = potencia
                    produto = Eletronico(
                        0,
                        nome,
                        qnt,
                        preco,
                        fabricante,
                        float(ncm) / 100,
                        tensao,
                        potencia,
                    )
            elif ITEM_TYPES[2][1] == tipo:
                tamanho = int(self.tamanho_entry.get())
                cloatch_tipo = int(self.tipo_roupa_entry.get())
                tecido: int = self.tecido_combo.get()
                cor: str = self.cor_entry.get()
                estampa = self.estampa_entry.get()
                genero: int = self.genero_entry.get()

                if tamanho < 0:
                    error = "Tamanho negativo"
                else:
                    produto = Roupas(
                        0,
                        nome,
                        qnt,
                        preco,
                        fabricante,
                        float(ncm) / 100,
                        tamanho,
                        cloatch_tipo,
                        tecido,
                        cor,
                        estampa,
                        genero,
                    )
            elif ITEM_TYPES[3][1] == tipo:
                ano = int(self.ano_entry.get())
                marca = self.marca_entry.get()
                funcao = self.funcao_entry.get()
                tipo_eletro = self.tipo_eletro_entry.get()

                produto = Eletrodomestico(
                    0,
                    nome,
                    qnt,
                    preco,
                    fabricante,
                    float(ncm) / 100,
                    ano,
                    marca,
                    funcao,
                    tipo_eletro,
                )
            else:
                produto = Produto(0, nome, qnt, 0, preco, fabricante, float(ncm) / 100)

        if error:
            self.label_error.configure(text=error)
            return

        await db.insert_produto(produto)

        self.__back()

    def _change_tipo_produto(self):
        tipo = self.tipo_combo.get()

        if self.current_prod_infos:
            self.current_prod_infos.destroy()
            if self._current_tipo == ITEM_TYPES[0][1]:
                self._data_validade = None
            elif self._current_tipo == ITEM_TYPES[1][1]:
                self.tensao_entry = None
                self.potencia_entry = None
            elif tipo == ITEM_TYPES[2][1]:
                self.tamanho_entry = None
                self.tipo_roupa_entry = None
                self.tecido_combo = None
                self.cor_entry = None
                self.estampa_entry = None
                self.genero_entry = None
            elif tipo == ITEM_TYPES[3][1]:
                self.ano_entry = None
                self.marca_entry = None
                self.funcao_entry = None
                self.tipo_eletro_entry = None

        frame = ttk.Frame(self)
        self.current_prod_infos = frame

        if tipo == ITEM_TYPES[0][0]:
            self.validade_entry = Default_input(frame, "Data Validade:", "date")
            self.validade_entry.grid()

        elif tipo == ITEM_TYPES[1][0]:
            self.tensao_entry = Default_input(frame, "Tensão", "int")
            self.potencia_entry = Default_input(frame, "Potência", "int")
            self.tensao_entry.grid()
            self.potencia_entry.grid(row=1)

        elif tipo == ITEM_TYPES[2][0]:
            self.tamanho_entry = Default_input(frame, "Tamanho", "int")
            self.tipo_roupa_entry = Default_input(frame, "Tipo", "int")
            self.tecido_combo = Default_input(
                frame, "Tipo Tecido", "combo", TIPOS_TECIDO
            )
            self.cor_entry = Default_input(frame, "Cor", "color")
            self.estampa_entry = Default_input(frame, "Estampa")
            self.genero_entry = Default_input(
                frame, "Gênero", "combo", ("Homem", "Mulher")
            )

            self.tamanho_entry.grid()
            self.tipo_roupa_entry.grid(row=1)
            self.tecido_combo.grid(row=2)
            self.cor_entry.grid(row=3)
            self.estampa_entry.grid(row=4)
            self.genero_entry.grid(row=5)

        elif tipo == ITEM_TYPES[3][0]:
            self.ano_entry = Default_input(frame, "Ano fabricação:", "int")
            self.marca_entry = Default_input(frame, "Marca:")
            self.funcao_entry = Default_input(frame, "Função:")
            self.tipo_eletro_entry = Default_input(frame, "Tipo:")
            self.ano_entry.grid()
            self.marca_entry.grid(row=1)
            self.funcao_entry.grid(row=2)
            self.tipo_eletro_entry.grid(row=3)

        frame.grid(row=10, columnspan=2)

        self._current_tipo = tipo

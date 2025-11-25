from models.carrinho import Carrinho
from .produto import Produto
class Usuario:
    def __init__(self, nome: str, data_nascimento: int, id_usuario: int = 0):
        self.id_usuario = id_usuario
        self.nome = nome
        self.data_nacimento = data_nascimento

    def cadastrar_usuario(self):
        pass


class Funcionario(Usuario):
    def __init__(self, nome: str, data_nascimento: int, salario: float, cargo: int):
        super().__init__(nome, data_nascimento)
        self.salario = salario
        self.cargo = cargo

    def trabalhar(self):
        pass


class Cliente(Usuario):
    def __init__(self, nome: str, data_nascimento: int, credito: float):
        super().__init__(nome, data_nascimento)
        self.credito = credito
        self.historico_de_compra = []
        self.carrinho = Carrinho()


class Fornecedor(Usuario):
    def __init__(self, nome: str, data_nascimento: int, id_usuario: int = 0):
        super().__init__(nome, data_nascimento, id_usuario)
        self.produtos:list[Produto] = []
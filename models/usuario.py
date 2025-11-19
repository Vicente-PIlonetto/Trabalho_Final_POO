class Usuario:

    def __init__(self, id_usuario: int, nome: str, data_nascimento: int):
        self.id_usuario = id_usuario
        self.nome = nome
        self.data_nacimento = data_nascimento

    def cadastrar_usuario(self):
        pass


class Funcionario(Usuario):
    def __init__(self, id_usuario: int, nome: str, data_nascimento: int, salario: float, cargo: int):
        super().__init__(id_usuario, nome, data_nascimento)
        self.salario = salario
        self.cargo = cargo

    def trabalhar(self):
        pass

class Cliente(Usuario):
    def __init__(self, id_usuario: int, nome: str, data_nascimento: int, credito: float, historico_de_compra: list):
        super().__init__(id_usuario, nome, data_nascimento)
        self.credito = credito
        self.historico_de_compra = historico_de_compra
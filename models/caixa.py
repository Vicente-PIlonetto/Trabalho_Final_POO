from models.usuario import Funcionario

class caixa:
    def __init__(self, id_caixa: int, historico_pedidos: list, funcionario: Funcionario, troco: float):
        self.id_caixa = id_caixa
        self.historico_pedidos = historico_pedidos
        self.funcionario = funcionario 
        self.troco = troco

    def processar_pagamento(self, metodo_pagamento: str, valor: float):
        pass

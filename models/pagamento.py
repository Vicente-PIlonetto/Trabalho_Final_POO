class Pagamento:
    def __init__(self, valor: float, forma: int, agencia: int):
        self.valor = valor
        self.forma = forma
        self.agencia = agencia

    def realizar_pagamento(self) -> bool:
        pass
class Pedido:
    def __init__(self, id_pedido: int, preco:float, carrinho: Carrinho):
        self.id_pedido = id_pedido
        self.preco = preco
        self.carrinho = carrinho
        
    def realizar_pagamento(self, pagamento: Pagamento) -> bool:
        return pagamento.realizar_pagamento()




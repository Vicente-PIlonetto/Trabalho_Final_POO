class Carrinho:
    def __init__(self, quantidade_itens: int):
        self.quantidade_itens = quantidade_itens
        self.produtos = {}

    def adicionar_produto(self, id: int, qnt: int):
        if not self.produtos.get(id):
            self.produtos[id] = qnt
        else:
            self.produtos[id] += qnt
        self.quantidade_itens += qnt
        return True

    def remover_produto(self, id: int, qnt: int):
        if self.produtos[id] > qnt:
            self.produtos[id] -= qnt
        else:
            del self.produtos[id]
        self.quantidade_itens -= qnt

    def limpar_carrinho(self):
        self.quantidade_itens = 0
        self.produtos.clear()

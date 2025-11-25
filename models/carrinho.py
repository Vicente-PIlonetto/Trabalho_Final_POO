from models.produto import Produto


class Carrinho:
    def __init__(self):
        self.quantidade_itens = 0
        self.produtos = {}

    def adicionar_produto(self, id, qnt: int, preco):
        if not self.produtos.get(id):
            self.produtos[id] = [qnt, float(preco)]
        else:
            self.produtos[id][0] += qnt
        self.quantidade_itens += qnt
        return True

    def remover_produto(self, id: int, qnt: int):
        if self.produtos[id] > qnt:
            self.produtos[id][0] -= qnt
        else:
            del self.produtos[id]
        self.quantidade_itens -= qnt

    def limpar_carrinho(self):
        self.quantidade_itens = 0
        self.produtos.clear()

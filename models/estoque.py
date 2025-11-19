class Estoque:
    def __init__(self, quantidade_maxima: int):
        self.produtos = []
        self.quantidade_maxima = quantidade_maxima

    def armazenar(self, item):
        if len(self.produtos) < self.quantidade_maxima:
            self.produtos.append(item)
            return True

    def remover(self, item):
        self.produtos.remove(item)
    
class Fornecedor:
    def __init__(self, nome: str, quantidade: int, quantidade_maxima: int):
        self.nome = nome
        self.quantidade = quantidade
        self.quantidade_maxima = quantidade_maxima
        self.produtos = []
        

    def armazenar(self, estoque, item):
        if self.quantidade < self.quantidade_maxima:
            estoque.append(item)
            self.quantidade += 1
            return True
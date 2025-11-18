class Carrinho:
    def __init__(self, quantidade_itens: int, produtos: list, limite: int):
        self.quantidade_itens = quantidade_itens
        self.produtos = []
        self.limite = limite

    def adicionar_produto(self, produto):
        if self.quantidade_itens < self.limite:
            self.produtos.append(produto)
            self.quantidade_itens += 1
            return True

    def remover_produto(self, produto):
        self.produtos.remove(produto)
        self.quantidade_itens -= 1

    def limpar_carrinho(self):
        self.quantidade_itens = 0
        self.produtos.clear()


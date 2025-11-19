from models.carrinho import Carrinho

carrinho = Carrinho(0, [], 2)
carrinho.adicionar_produto("Produto A")
carrinho.adicionar_produto("Produto B")
carrinho.remover_produto("Produto A")
carrinho.limpar_carrinho()

print(f"Quantidade de itens no carrinho: {carrinho.quantidade_itens}")
print(f"Produtos no carrinho: {carrinho.produtos}")


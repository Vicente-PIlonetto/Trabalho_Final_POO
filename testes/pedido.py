from models.pedido import Pedido
from models.carrinho import Carrinho
from models.produto import Produto


produto1 = Produto(1, "Produto 1", 100.0, 10, 1, 20230101, 1, 1234.56)
produto2 = Produto(2, "Produto 2", 150.0, 5, 2, 20230102, 2, 2345.67)
carrinho = Carrinho(1, [produto1, produto2], 250)
pedido1 = Pedido(1, 250.0, carrinho)

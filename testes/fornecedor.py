from models.fornecedor import Fornecedor
from models.estoque import Estoque
from models.produto import Alimento

Fornecedor1 = Fornecedor("Carlos", 124, 200)
Estoque1 = Estoque(50)
Produto1 = Alimento(1, "Banana", 5, 1, 6.99, 1, 1, 1)

print(f"{Estoque1.produtos}")
Fornecedor1.armazenar(Estoque1, Produto1)
print(f"{Estoque1.produtos}")
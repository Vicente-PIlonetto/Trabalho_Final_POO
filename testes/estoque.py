from models.estoque import Estoque
from models.produto import Alimento

Estoque1 = Estoque(50)
Produto1 = Alimento(1, "Banana", 5, 1, 6.99, 1, 1, 1)

Estoque1.armazenar(Produto1)
print(f"{Estoque1.produtos}")
Estoque1.remove(Produto1)
print(f"{Estoque1.produtos}")

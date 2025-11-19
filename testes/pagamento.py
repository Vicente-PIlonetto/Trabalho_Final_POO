from models.pagamento import Pagamento
from models.produto import Produto


pagamento1 = Pagamento(120.0, 1, None)
pagamento2 = Pagamento(150.0, 2, "Banco do Brasil - Agência 1234")


print(pagamento1.valor)
print(pagamento2.valor)

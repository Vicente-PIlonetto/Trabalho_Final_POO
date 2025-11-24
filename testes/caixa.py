from models.caixa import Caixa
from models.usuario import Funcionario

func = Funcionario(1, "Carlos", 19900101, 2000, 1)
c = Caixa(10, [], func, 0.0)
c.processar_pagamento('cartão', 100.0)

print(f"Caixa operado por: {c.funcionario.nome}")
print(f"Pagamento processado: {c.processar_pagamento('cartão', 100.0)}")
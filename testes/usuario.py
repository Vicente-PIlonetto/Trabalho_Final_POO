from models.usuario import Usuario, Funcionario, Cliente

usuario = Usuario(1, "Carlos", 19900101)
funcionario = Funcionario(2, "Cauan", 19850510, 3000, 1)
cliente = Cliente(3, "Giovani", 19951212, 500.0, ["Compra1", "Compra2"])

print(f"Usuário: {usuario.nome}, Data de Nascimento: {usuario.data_nacimento}")
print(f"Funcionário: {funcionario.nome}, Cargo: {funcionario.cargo}")   
print(f"Cliente: {cliente.nome}, Crédito: {cliente.credito}, Histórico de Compras: {cliente.historico_de_compra}")
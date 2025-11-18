class Produto:
    def __init__(self, id: int, nome: str, quantidade: int, categoria: int, preco: float, data_fabricacao: int, fabricante: int, ncm: float) -> None:
        self.id = id
        self.nome = nome
        self.quantidade = quantidade
        self.categoria = categoria
        self.preco = preco
        self.data_fabricacao = data_fabricacao
        self.fabricante = fabricante
        self.ncm = ncm

    def aplicar_desconto(self, pcnt: float) -> None:
        self.preco -= self.preco * pcnt

    def aplicar_acrescimo(self, pcnt: float) -> None:
        self.preco += self.preco * pcnt


class Alimento(Produto):
    def __init__(self, id: int, nome: str, quantidade: int, categoria: int, preco: float, data_fabricacao: int, fabricante: int, ncm: float, data_validade: int) -> None:
        super().__init__(id, nome, quantidade, categoria, preco, data_fabricacao, fabricante, ncm)
        self.data_validade = data_validade

class Eletronico(Produto):
    def __init__(self, id: int, nome: str, quantidade: int, categoria: int, preco: float, data_fabricacao: int, fabricante: int, ncm: float, tensao: int, potencia: int) -> None:
        super().__init__(id, nome, quantidade, categoria, preco, data_fabricacao, fabricante, ncm)
        self.tensao = tensao
        self.potencia = potencia

class Roupas(Produto):
    def __init__(self, id: int, nome: str, quantidade: int, categoria: int, preco: float, data_fabricacao: int, fabricante: int, ncm: float, tamanho: int, tipo: str, tecido: int, cor: int, estampa: int, genero: int) -> None:
        super().__init__(id, nome, quantidade, categoria, preco, data_fabricacao, fabricante, ncm)
        self.tamanho = tamanho
        self.tipo = tipo
        self.tecido = tecido
        self.cor = cor
        self.estampa = estampa
        self.genero = genero

class Eletrodomestico(Produto):
    def __init__(self, id: int, nome: str, quantidade: int, categoria: int, preco: float, data_fabricacao: int, fabricante: int, ncm: float, ano_lancamento: int, marca: str, funcao: str, tipo: int) -> None:
        super().__init__(id, nome, quantidade, categoria, preco, data_fabricacao, fabricante, ncm)
        self.ano_lancamento = ano_lancamento
        self.marca = marca
        self.funcao = funcao
        self.tipo = tipo

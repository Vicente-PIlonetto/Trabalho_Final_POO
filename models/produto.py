from utils import get_pcnt, get_tipo_descricao


class Produto:
    __slots__ = (
        "id",
        "nome",
        "quantidade",
        "tipo",
        "preco",
        "fabricante",
        "ncm",
    )
    COLUMNS = (("ID", 40), ("Nome", 180), ("Tipo", 100), ("Preço", 80), ("Criador", 120), ("QNT disponível", 115), ("NCM", 55))

    def __init__(
        self,
        id: int,
        nome: str,
        quantidade: int,
        tipo: int,
        preco: float,
        fabricante: int,
        ncm: float,
    ) -> None:
        self.id = id
        self.nome = nome
        self.quantidade = quantidade
        self.tipo = tipo
        self.preco = preco
        self.fabricante = fabricante
        self.ncm = ncm

    @classmethod
    def from_db(cls, row: tuple):
        return cls(row[0], row[1], row[5], row[2], row[3], row[4], row[6])

    @classmethod
    def from_row(cls, row: tuple):
        return cls(row[0], row[1], row[5], row[2], row[3], row[4], row[6])


    def to_tuple(self) -> tuple:
        return (
            self.id,
            self.nome,
            get_tipo_descricao(self.tipo),
            self.preco,
            self.fabricante,
            self.quantidade,
            get_pcnt(self.ncm),
        )

    def aplicar_desconto(self, pcnt: float) -> None:
        self.preco -= self.preco * pcnt

    def aplicar_acrescimo(self, pcnt: float) -> None:
        self.preco += self.preco * pcnt


class Alimento(Produto):
    def __init__(
        self,
        id: int,
        nome: str,
        quantidade: int,
        preco: float,
        fabricante: int,
        ncm: float,
        data_validade: int,
    ) -> None:
        super().__init__(id, nome, quantidade, 1, preco, fabricante, ncm)
        self.data_validade = data_validade


class Eletronico(Produto):
    def __init__(
        self,
        id: int,
        nome: str,
        quantidade: int,
        preco: float,
        fabricante: int,
        ncm: float,
        tensao: int,
        potencia: int,
    ) -> None:
        super().__init__(id, nome, quantidade, 2, preco, fabricante, ncm)
        self.tensao = tensao
        self.potencia = potencia


class Roupas(Produto):
    def __init__(
        self,
        id: int,
        nome: str,
        quantidade: int,
        preco: float,
        fabricante: int,
        ncm: float,
        tamanho: int,
        tipo: str,
        tecido: int,
        cor: int,
        estampa: int,
        genero: int,
    ) -> None:
        super().__init__(id, nome, quantidade, 3, preco, fabricante, ncm)
        self.tamanho = tamanho
        self.tipo = tipo
        self.tecido = tecido
        self.cor = cor
        self.estampa = estampa
        self.genero = genero


class Eletrodomestico(Produto):
    def __init__(
        self,
        id: int,
        nome: str,
        quantidade: int,
        preco: float,
        fabricante: int,
        ncm: float,
        ano_lancamento: int,
        marca: str,
        funcao: str,
        tipo: int,
    ) -> None:
        super().__init__(id, nome, quantidade, 4, preco, fabricante, ncm)
        self.ano_lancamento = ano_lancamento
        self.marca = marca
        self.funcao = funcao
        self.tipo = tipo

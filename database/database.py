from tkinter import INSERT
from typing import Literal
import aiosqlite
from argon2 import PasswordHasher

from globals import FABRICANTES, INFOS_PADAO, ITEM_TYPES, TIPOS_ROUPAS
from models.carrinho import Carrinho
from models.produto import Alimento, Eletrodomestico, Eletronico, Produto, Roupas


class Database:
    def __init__(self) -> None:
        self.__ph = PasswordHasher()

    async def init(self):
        self.conn = await aiosqlite.connect("database/database.db")
        f = open("database/init.sql")
        await self.conn.executescript(f.read())
        f.close()

    async def verificar_primeiro_usuario(self):
        res = await self.conn.execute("select id from users limit 1")
        res = await res.fetchone()

        INFOS_PADAO["primeiro_usuario"] = res == None

    async def varificar_usuario_duplicado(self, name: str, born_date: int):
        res = await self.conn.execute(
            "select id from users where name = ? and born_date = ?", (name, born_date)
        )
        res = await res.fetchone()
        return res is not None

    async def insert_user(
        self,
        name: str,
        password: str,
        born_date: int,
        type: int,
        salario: float | None,
        cargo: int | None,
    ) -> int:
        try:
            hashed_password = self.__ph.hash(password)
            query = """
                INSERT INTO users (name, password, born_date, type, salary, cargo, credito)
                VALUES (?, ?, ?, ?, ?, ?, 0)
            """
            res = await self.conn.execute(
                query, (name, hashed_password, born_date, type, salario, cargo)
            )
            await self.conn.commit()
            return res.lastrowid or -1
        except TimeoutError as e:
            print(f"Database error: {e}")
            return -1

    async def login(
        self, name: str, password: str
    ) -> (
        Literal[False]
        | tuple[int, str, str, int, int, float | None, int | None, float | None, int]
    ):
        cur = await self.conn.execute(
            "SELECT * FROM users WHERE name = ? limit 1", (name,)
        )
        row = await cur.fetchone()

        if row is None:
            return False

        try:
            self.__ph.verify(row[2], password)
            return tuple(row)
        except Exception:
            return False

    async def load_product_types_with_items(self):
        types = []

        res = await self.conn.execute(
            """SELECT pt.*
            FROM product_types pt
            JOIN products p ON pt.id = p.type
            GROUP BY pt.id;
        """
        )

        res = await res.fetchall()

        for i in res:
            types.append(tuple(i))
        return types

    async def load_product_types(self):
        global ITEM_TYPES

        res = await self.conn.execute("SELECT * from product_types;")
        res = await res.fetchall()

        for i in res:
            ITEM_TYPES.append(tuple(i))

    async def load_fabricantes(self):
        global FABRICANTES

        res = await self.conn.execute("SELECT * from fabricante;")
        res = await res.fetchall()

        for i in res:
            FABRICANTES.append(tuple(i))

    async def load_tipos_roupas(self):
        global TIPOS_ROUPAS

        res = await self.conn.execute("SELECT * from tipos_roupas;")
        res = await res.fetchall()

        for i in res:
            TIPOS_ROUPAS.append(tuple(i))

    async def load_products(self, select_filter: int = 0):
        items: list[Produto] = []
        cls = Produto

        _filter = ""
        _join = ""
        if select_filter != 0:
            _filter = f"WHERE p.type = {select_filter}"

            if select_filter == 1:
                _join = "JOIN food_columns fc ON fc.product_id = p.id"
                cls = Alimento
            elif select_filter == 2:
                _join = "JOIN eletronic_columns ec ON ec.product_id = p.id"
                cls = Eletronico
            elif select_filter == 3:
                _join = "JOIN cloath_columns cc ON cc.product_id = p.id"
                cls = Roupas
            elif select_filter == 4:
                _join = "JOIN eletrodomesticos_columns ec ON ec.product_id = p.id"
                cls = Eletronico

        res = await self.conn.execute(
            f"""
            SELECT * FROM products p {_join} {_filter};
        """
        )
        res = await res.fetchall()
        for _product in res:
            items.append(cls.from_db(_product))

        return items

    async def load_products_id(self, ids: list[int]):
        items: list[Produto] = []
        if not len(ids):
            return items

        ids_formatados = ",".join(map(str, ids))

        res = await self.conn.execute(
            f"""
            SELECT * FROM products where id in ({ids_formatados});
        """
        )
        res = await res.fetchall()
        for _product in res:
            items.append(Produto.from_db(_product))

        return items

    async def insert_pedido(self, id_usuario: int, items: Carrinho) -> bool:
        valor = 0
        _items = []

        for item in items.produtos:
            valor += item.preco * item.quantidade
            _items.append([0, item.id, item.quantidade])

        id = await self.conn.execute(
            """
            INSERT INTO pedidos(id_usuario, value)
            VALUES (?, ?)
        """,
            (id_usuario, valor),
        )

        for item in _items:
            item[0] = id

        if not id:
            return False

        await self.conn.execute(
            """
            INSERT INTO items_pedido
            VALUES ?
        """,
            ",".join(map(lambda x: f"({str(x)[1:-1]})", _items)),
        )

        items.limpar_carrinho()
        return True

    async def insert_produto(self, produto: Produto, id_usuario: int = 1) -> bool:
        res = await self.conn.execute(
            """
            INSERT INTO products (name, type, price, creator, qnt_available, NCM)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                produto.nome,
                produto.tipo,
                produto.preco,
                produto.fabricante,
                0,
                produto.ncm,
            ),
        )
        await self.conn.commit()

        cur = await self.conn.execute("SELECT last_insert_rowid()")
        row = await cur.fetchone()
        id_produto = row[0]


        if isinstance(produto, Alimento):
            await self.conn.execute(
                """
                INSERT INTO food_columns (product_id, vality_data)
                VALUES (?, ?)
                """,
                (id_produto, produto.data_validade),
            )


        elif isinstance(produto, Eletronico):
            await self.conn.execute(
                """
                INSERT INTO eletronic_columns (product_id, tension, potency)
                VALUES (?, ?, ?)
                """,
                (id_produto, produto.tensao, produto.potencia),
            )


        elif isinstance(produto, Roupas):
            await self.conn.execute(
                """
                INSERT INTO cloath_columns (product_id, size, type, cloath_type, color, estamp, genre)
                VALUES (?, ?, "Teste", ?, ?, ?, ?)
                """,
                (
                    id_produto,
                    produto.tamanho,
                    produto.tecido,
                    produto.cor,
                    produto.estampa,
                    produto.genero,
                ),
            )


        elif isinstance(produto, Eletrodomestico):
            await self.conn.execute(
                """
                INSERT INTO eletrodomesticos_columns (product_id, launch_year, creator, function, type)
                VALUES (?, ?, ?, ?, "testee")
                """,
                (
                    id_produto,
                    produto.ano_lancamento,
                    produto.fabricante,
                    produto.funcao,
                ),
            )

        res = await self.conn.execute(
            """
            INSERT INTO pedido (id_usuario, tipo, value)
            VALUES (?, ?, ?)
            """,
            (id_usuario, 1, produto.preco * produto.quantidade),
        )
        await self.conn.commit()

        cur = await self.conn.execute("SELECT last_insert_rowid()")
        row = await cur.fetchone()
        id_pedido = row[0]

        await self.conn.execute(
            """
            INSERT INTO items_pedido (pedido_id, item_id, quantity)
            VALUES (?, ?, ?)
            """,
            (id_pedido, id_produto, produto.quantidade),
        )
        await self.conn.commit()

        return True

    async def update_quantidade_by_pedido(self, id_pedido: int) -> bool:
        cur = await self.conn.execute(
            "SELECT tipo FROM pedido WHERE id = ?", (id_pedido,)
        )
        row = await cur.fetchone()

        if row is None:
            raise ValueError(f"Pedido {id_pedido} não encontrado.")

        cur = await self.conn.execute(
            """
            SELECT item_id, quantity
            FROM items_pedido
            WHERE pedido_id = ?
            """,
            (id_pedido,),
        )

        itens = await cur.fetchall()

        if not itens:
            raise ValueError(f"Pedido {id_pedido} não possui itens.")

        for item_id, quantity in itens:
            await self.conn.execute(
                """
                UPDATE products
                SET qnt_available = qnt_available + ?, completo = 1
                WHERE id = ?
                """,
                (quantity, item_id),
            )

        await self.conn.commit()

        return True

    async def listar_pedidos(
        self,
        completo: int | None = None,
        tipo: int = 1
    ):

        filtros = []
        params = []

        if completo is not None:
            filtros.append("p.completo = ?")
            params.append(completo)

        if tipo is not None:
            filtros.append("p.tipo = ?")
            params.append(tipo)

        where_clause = ""
        if filtros:
            where_clause = "WHERE " + " AND ".join(filtros)


        query_pedidos = f"""
            SELECT
                p.id,
                u.name,
                p.tipo,
                p.completo,
                p.value
            FROM pedido p
            join users u on u.id = p.id_usuario
            {where_clause}
            ORDER BY p.id DESC
        """

        cur = await self.conn.execute(query_pedidos, params)
        pedidos_raw = await cur.fetchall()

        if not pedidos_raw:
            return []

        pedidos = []


        for id_pedido, id_usuario, tipo_pedido, completo_pedido, valor in pedidos_raw:
            cur = await self.conn.execute(
                """
                SELECT
                    ip.item_id,
                    ip.quantity,
                    pr.name,
                    pr.price,
                    pr.type
                FROM items_pedido ip
                JOIN products pr ON pr.id = ip.item_id
                WHERE ip.pedido_id = ?
                """,
                (id_pedido,),
            )
            itens = await cur.fetchall()

            itens_formatados = [
                {
                    "id_produto": item_id,
                    "quantidade": qnt,
                    "nome": nome,
                    "preco": preco,
                    "tipo_produto": tipo_produto,
                }
                for (item_id, qnt, nome, preco, tipo_produto) in itens
            ]

            pedidos.append(
                {
                    "id_pedido": id_pedido,
                    "id_usuario": id_usuario,
                    "tipo": "COMPRA" if tipo_pedido == 1 else "VENDA",
                    "completo": bool(completo_pedido),
                    "valor_total": valor,
                    "itens": itens_formatados,
                }
            )

        return pedidos

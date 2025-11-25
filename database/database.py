from typing import Literal
import aiosqlite
from argon2 import PasswordHasher

from constraints import ITEM_TYPES
from models.carrinho import Carrinho
from models.produto import Alimento, Eletronico, Produto, Roupas


class Database:
    def __init__(self) -> None:
        self.__ph = PasswordHasher()

    async def init(self):
        self.conn = await aiosqlite.connect("database/database.db")
        f = open("database/init.sql")
        await self.conn.executescript(f.read())
        f.close()

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


        id = await self.conn.execute("""
            INSERT INTO pedidos(id_usuario, value)
            VALUES (?, ?)
        """, (id_usuario, valor))

        for item in _items:
            item[0] = id

        if not id:
            return False

        await self.conn.execute("""
            INSERT INTO items_pedido
            VALUES ?
        """, ",".join(map(lambda x: f"({str(x)[1:-1]})", _items)))

        items.limpar_carrinho()
        return True

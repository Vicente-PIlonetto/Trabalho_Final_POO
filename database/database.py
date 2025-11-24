from typing import Literal
import aiosqlite
from argon2 import PasswordHasher

from constraints import ITEM_TYPES
from models.produto import Produto


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

        _filter = ""
        if select_filter != 0:
            _filter = f" WHERE type = {select_filter}"

        res = await self.conn.execute(
            f"""
            SELECT * FROM products {_filter};
        """
        )
        res = await res.fetchall()
        for _product in res:
            items.append(Produto.from_db(_product))

        return items

    async def load_products_id(self, ids: list[int]):
        items: list[Produto] = []

        ids_formatados = ",".join(map(lambda x: str(x), ids))

        res = await self.conn.execute(
            f"""
            SELECT * FROM products where id in ({ids_formatados});
        """
        )
        res = await res.fetchall()
        for _product in res:
            items.append(Produto.from_db(_product))

        return items
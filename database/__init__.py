import asyncio
from .database import Database


async def run_init():
    await db.init()
    await asyncio.gather(
        db.load_product_types(),
        db.load_fabricantes(),
        db.load_tipos_roupas(),
        db.verificar_primeiro_usuario(),
    )


db = Database()
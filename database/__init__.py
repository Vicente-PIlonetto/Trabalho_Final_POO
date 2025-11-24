import asyncio
from .database import Database

db = Database()
asyncio.run(db.init())
asyncio.run(db.load_product_types())

CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    password TEXT NOT NULL,
    born_date INTEGER NOT NULL,
    type INTEGER NOT NULL,
    salary REAL,
    cargo INTEGER,
    credito REAL,
    active INTEGER DEFAULT 1
);
CREATE TABLE IF NOT EXISTS products(
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    type INTEGER NOT NULL,
    price REAL NOT NULL,
    creator TEXT NOT NULL,
    qnt_available INT DEFAULT 0,
    NCM REAL NOT NULL
);
CREATE TABLE IF NOT EXISTS product_types(id INTEGER PRIMARY KEY, name TEXT);
INSERT
    OR IGNORE INTO product_types
VALUES (1, 'Alimentos'),
    (2, 'Eletrônicos'),
    (3, 'Roupas'),
    (4, 'Elêtrodomésticos');
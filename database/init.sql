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
CREATE TABLE IF NOT EXISTS food_columns (
    product_id INT NOT NULL,
    vality_data INT NOT NULL
);
CREATE TABLE IF NOT EXISTS eletronic_columns (
    product_id INT NOT NULL,
    tension INT NOT NULL,
    potency INT NOT NULL
);
CREATE TABLE IF NOT EXISTS cloath_columns (
    product_id INT NOT NULL,
    size INT NOT NULL,
    type TEXT NOT NULL,
    cloath_type INT NOT NULL,
    color INT NOT NULL,
    estamp TEXT NOT NULL,
    genre TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS eletrodomesticos_columns (
    product_id INT NOT NULL,
    launch_year INT NOT NULL,
    creator TEXT NOT NULL,
    function TEXT NOT NULL,
    type int INT NOT NULL
);
INSERT
    OR IGNORE INTO product_types
VALUES (1, 'Alimentos'),
    (2, 'Eletrônicos'),
    (3, 'Roupas'),
    (4, 'Elêtrodomésticos');
CREATE TABLE IF NOT EXISTS pedido (
    id INT PRIMARY KEY,
    id_usuario INT NOT NULL,
    value REAL NOT NULL
);
CREATE TABLE IF NOT EXISTS items_pedido(
    pedido_id INT NOT NULL,
    item_id INT NOT NULL,
    quantity INT NOT NULL
);
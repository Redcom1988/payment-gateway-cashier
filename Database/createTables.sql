CREATE TABLE employees (
    employee_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    contact_num TEXT,
    address TEXT,
    password TEXT NOT NULL,
    role TEXT NOT NULL DEFAULT 'employee' CHECK (role IN ('admin', 'employee'))
);

CREATE TABLE products (
    product_id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_name TEXT NOT NULL,
    product_cat TEXT NOT NULL,
    product_subcat TEXT NOT NULL,
    cost_price REAL NOT NULL,
    vendor_stock INTEGER NOT NULL,
    vendor TEXT NOT NULL
);

CREATE TABLE inventory (
    inventory_id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER NOT NULL,
    stock INTEGER NOT NULL,
    sell_price REAL NOT NULL,
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);

CREATE TABLE transactions (
    transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
    date DATETIME DEFAULT CURRENT_TIMESTAMP,
    transaction_details TEXT NOT NULL,
    total REAL NOT NULL,
    transaction_status TEXT NOT NULL DEFAULT 'pending' CHECK (transaction_status IN ('pending', 'completed')),
    employee_id INTEGER NOT NULL,
    FOREIGN KEY (employee_id) REFERENCES employee(employee_id)
);
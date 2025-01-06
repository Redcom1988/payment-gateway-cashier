CREATE TABLE employee (
    employee_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL
    contact_num TEXT
    address TEXT
    password TEXT NOT NULL
    role TEXT NOT NULL DEFAULT 'employee' CHECK (role IN ('admin', 'employee')
);

CREATE TABLE customer (
    customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_name TEXT NOT NULL,
    contact_num TEXT NOT NULL,
);

CREATE TABLE products (
    product_id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_name TEXT NOT NULL,
    product_cat TEXT NOT NULL,
    product_subcat TEXT NOT NULL,
    cost_price REAL NOT NULL,
    max_retail_price REAL NOT NULL,
    stock INTEGER NOT NULL,
    FOREIGN KEY (vendor_id) REFERENCES vendor(vendor_id)
);

CREATE TABLE vendor (
    vendor_id INTEGER PRIMARY KEY AUTOINCREMENT,
    vendor_name TEXT NOT NULL,
    contact_num TEXT NOT NULL,
    address TEXT NOT NULL
);

CREATE TABLE inventory (
    inventory_id INTEGER PRIMARY KEY AUTOINCREMENT,
    FOREIGN KEY (product_id) REFERENCES products(product_id)
    FOREIGN KEY (product_cat) REFERENCES products(product_cat)
    FOREIGN KEY (product_subcat) REFERENCES products(product_subcat)
    stock INTEGER NOT NULL,
    sell_price REAL NOT NULL,
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);

CREATE TABLE bill (
    bill_id INTEGER PRIMARY KEY AUTOINCREMENT,
    date CURRENT_DATE,
    FOREIGN KEY (customer_id) REFERENCES customer(customer_id)
    FOREIGN KEY (employee_id) REFERENCES employee(employee_id)
    bill_details TEXT NOT NULL
);
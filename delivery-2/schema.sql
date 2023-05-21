DROP TABLE IF EXISTS customers;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS sales;
DROP TABLE IF EXISTS pay;
DROP TABLE IF EXISTS employees;
DROP TABLE IF EXISTS process;
DROP TABLE IF EXISTS departments;
DROP TABLE IF EXISTS workplaces;
DROP TABLE IF EXISTS works;
DROP TABLE IF EXISTS offices;
DROP TABLE IF EXISTS warehouses;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS ean_products;
DROP TABLE IF EXISTS suppliers;
DROP TABLE IF EXISTS contains;
DROP TABLE IF EXISTS delivery;

CREATE TABLE customers (
    cust_no SERIAL PRIMARY KEY,
    "name" VARCHAR(50) NOT NULL,
    email VARCHAR(50) UNIQUE NOT NULL,
    phone VARCHAR(20) NOT NULL,
    "address" VARCHAR(100) NOT NULL
);

CREATE TABLE orders (
    order_no SERIAL PRIMARY KEY,
    "date" DATE NOT NULL,
    cust_no INTEGER NOT NULL,
    FOREIGN KEY (cust_no) REFERENCES customers (cust_no)
    -- IC-3: any order_no in Order must exist in contains
);

CREATE TABLE sales (
    order_no INTEGER PRIMARY KEY,
    FOREIGN KEY (order_no) REFERENCES orders (order_no)
);

CREATE TABLE pay (
    order_no INTEGER PRIMARY KEY,
    cust_no INTEGER,
    FOREIGN KEY (order_no) REFERENCES sales (order_no),
    FOREIGN KEY (cust_no) REFERENCES customers (cust_no)
    -- IC-1: Customers can only pay for the Sale of an Order they have placed themselves
);

CREATE TABLE employees (
    ssn CHAR(11) PRIMARY KEY,
    tin CHAR(9) UNIQUE NOT NULL,
    bdate DATE NOT NULL,
    "name" VARCHAR(50) NOT NULL
    -- IC-2: any ssn in Employee must exist in works
);

CREATE TABLE process (
    ssn CHAR(11),
    order_no INTEGER,
    PRIMARY KEY (ssn, order_no),
    FOREIGN KEY (ssn) REFERENCES employees (ssn),
    FOREIGN KEY (order_no) REFERENCES orders (order_no)
);

CREATE TABLE departments (
    "name" VARCHAR(50) PRIMARY KEY
);

CREATE TABLE workplaces (
    "address" VARCHAR(100) PRIMARY KEY,
    lat NUMERIC(10, 7) NOT NULL,
    long NUMERIC(10, 7) NOT NULL,
    UNIQUE(lat, long)
);

CREATE TABLE works (
    ssn CHAR(11),
    "name" VARCHAR(50),
    "address" VARCHAR(100),
    PRIMARY KEY (ssn, name, address),
    FOREIGN KEY (ssn) REFERENCES employees (ssn),
    FOREIGN KEY ("name") REFERENCES departments ("name"),
    FOREIGN KEY ("address") REFERENCES workplaces ("address")
);

CREATE TABLE offices (
    "address" VARCHAR(100) PRIMARY KEY,
    FOREIGN KEY ("address") REFERENCES workplaces ("address")
);

CREATE TABLE warehouses (
    "address" VARCHAR(100) PRIMARY KEY,
    FOREIGN KEY ("address") REFERENCES workplaces ("address")
);

CREATE TABLE products (
    sku VARCHAR(20) PRIMARY KEY,
    "name" VARCHAR(30) NOT NULL,
    "description" TEXT NOT NULL,
    price NUMERIC(10, 2) NOT NULL
    -- IC-4: any sku in Product must exist in Supplier
);

CREATE TABLE ean_products (
    sku VARCHAR(20) PRIMARY KEY,
    ean VARCHAR(14) NOT NULL,
    FOREIGN KEY (sku) REFERENCES products (sku)
);

CREATE TABLE suppliers (
    tin CHAR(9) PRIMARY KEY,
    "name" VARCHAR(50) NOT NULL,
    "address" VARCHAR(100) NOT NULL,
    sku VARCHAR(20) NOT NULL,
    "date" DATE NOT NULL,
    FOREIGN KEY (sku) REFERENCES products (sku)
);

CREATE TABLE contains (
    order_no INTEGER,
    sku VARCHAR(20),
    PRIMARY KEY (order_no, sku),
    qty INTEGER NOT NULL,
    FOREIGN KEY (order_no) REFERENCES orders (order_no),
    FOREIGN KEY (sku) REFERENCES products (sku)
);

CREATE TABLE delivery (
    "address" VARCHAR(100),
    tin CHAR(9),
    PRIMARY KEY ("address", tin),
    FOREIGN KEY ("address") REFERENCES warehouses ("address"),
    FOREIGN KEY (tin) REFERENCES suppliers (tin)
);

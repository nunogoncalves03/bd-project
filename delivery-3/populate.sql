INSERT INTO customer (cust_no, "name", email, phone, "address")
VALUES
    (1, 'Manuel', 'manuel24@gmail.com', '933444555', 'Rua dos Clerigos 14 1Esq 4050-205 Vitoria'),
    (2, 'Joao', 'joao-1@gmail.com', '933423662', 'Rua do Cacto 10 2Dir 1200-234 Alcantara'),
    (3, 'Rui', 'ruiii@gmail.com', '924444333', 'Rua das Rosas 110 2Esq 1000-500 Alvalade'),
    (4, 'Fabio', 'fmata@gmail.com', '933333333', 'Avenida da Liberdade 130 1Dir 1250-142 Santo Antonio'),
    (5, 'Nuno', 'ngfg@gmail.com', '922777777', 'Rua dos Assaltos 25 3000-500 Odivelas'),
    (6, 'Diogo', 'yasuo@gmail.com', '911222333', 'Largo D. Afonso Henriques 60 R/C Esq 3004-500 Ramada'),
    (7, 'Pedro', 'piedro@gmail.com', '934567890', 'Rua D. Sancho I 40 1Dir 2955-500 Almada'),
    (8, 'Ana', 'ana@gmail.com', '933322111', 'Rua Do Grilo 22 3Dir 5000-500 Porto'),
    (9, 'Celia', 'celia23@sapo.com', '921444222', 'Rua das Trigosas 13 2Esq 2005-457 Santarem'),
    (10, 'Sara', 'sara@outlook.com', '933333322', 'Rua da Revolucao 79 2Dir 2330-500 Torres Novas');

INSERT INTO orders (order_no, "date", cust_no)
VALUES
    (1, DATE '2022-01-05', 1),
    (2, DATE '2022-01-10', 2),
    (3, DATE '2022-01-15', 3),
    (4, DATE '2022-04-05', 4),
    (5, DATE '2023-01-02', 5),
    (6, DATE '2023-01-05', 6),
    (7, DATE '2023-01-10', 7),
    (8, DATE '2023-01-15', 8),
    (9, DATE '2023-01-20', 9),
    (10, DATE '2023-01-25', 10),
    (11, DATE '2023-01-30', 7);

-- 2.2
INSERT INTO orders (order_no, "date", cust_no)
SELECT
    generate_series(12, 376),
    generate_series('2022-01-01'::TIMESTAMP, '2022-12-31'::TIMESTAMP, '1 day'),
    1;

-- 2.3
INSERT INTO orders (order_no, "date", cust_no)
SELECT
    generate_series(377, 383),
    generate_series('2022-01-01'::TIMESTAMP, '2022-12-31'::TIMESTAMP, '60 day'),
    1;

INSERT INTO pay (order_no, cust_no)
VALUES
    (1,1),
    (3,3),
    (5,5),
    (7,7),
    (9,9),
    (11,7);

-- 2.2
INSERT INTO pay (order_no, cust_no)
SELECT
    generate_series(12, 376),
    1;

INSERT INTO employee (ssn, tin, bdate, "name")
VALUES
    ('123-45-6789', '987654321', DATE '1990-01-01', 'John Doe'),
    ('987-65-4321', '123456789', DATE '1992-03-15', 'Jane Smith'),
    ('456-78-9012', '654321987', DATE '1988-06-30', 'Michael Johnson'),
    ('789-01-2345', '789456123', DATE '1995-12-10', 'Emily Davis'),
    ('234-56-7890', '321654987', DATE '1991-09-20', 'Daniel Wilson'),
    ('567-89-0123', '987123654', DATE '1987-04-05', 'Sarah Thompson'),
    ('890-12-3456', '456789123', DATE '1993-07-25', 'Christopher Lee'),
    ('345-67-8901', '789123456', DATE '1989-11-18', 'Olivia Martin'),
    ('678-90-1234', '123987456', DATE '1994-02-14', 'Matthew Taylor'),
    ('901-23-4567', '321789654', DATE '1985-08-08', 'Sophia Anderson'),
    ('111-22-3333', '999888777', DATE '1997-05-03', 'Jessica Adams'),
    ('222-33-4444', '777666555', DATE '1984-12-20', 'Andrew Wilson');


INSERT INTO process (ssn, order_no)
VALUES
    ('123-45-6789', 1),
    ('987-65-4321', 2),
    ('456-78-9012', 3),
    ('789-01-2345', 4),
    ('234-56-7890', 5),
    ('567-89-0123', 6),
    ('890-12-3456', 7),
    ('345-67-8901', 8),
    ('678-90-1234', 9),
    ('901-23-4567', 10);

-- 2.2
INSERT INTO process (ssn, order_no)
SELECT
    '123-45-6789',
    generate_series(12, 376);


INSERT INTO department ("name")
VALUES
    ('Marketing'),
    ('Sales'),
    ('Finance'),
    ('Human Resources'),
    ('Operations'),
    ('Productions');

INSERT INTO workplace ("address", lat, long)
VALUES
    ('Avenida da Liberdade 10 1250-142 Santo Antonio', 40.7128, -70.2345),
    ('Rua dos Clerigos 5 4050-205 Vitoria', 38.2228, -80.4454),
    ('D. Afonso Henriques 35 1000-123 Alameda', 30.3344, -69.0003),
    ('Rua das Cruzes 7 2664-255 Cruzadas', 39.3333, -85.2222);


INSERT INTO office ("address")
VALUES
    ('Avenida da Liberdade 10 1250-142 Santo Antonio'),
    ('Rua dos Clerigos 5 4050-205 Vitoria');
    
INSERT INTO warehouse ("address")
VALUES
    ('D. Afonso Henriques 35 1000-123 Alameda'),
    ('Rua das Cruzes 7 2664-255 Cruzadas');

INSERT INTO works (ssn, "name", "address")
VALUES
    ('123-45-6789', 'Marketing', 'Avenida da Liberdade 10 1250-142 Santo Antonio'),
    ('987-65-4321', 'Marketing', 'Avenida da Liberdade 10 1250-142 Santo Antonio'),
    ('456-78-9012', 'Sales', 'D. Afonso Henriques 35 1000-123 Alameda'),
    ('789-01-2345', 'Sales', 'Rua dos Clerigos 5 4050-205 Vitoria'),
    ('234-56-7890', 'Finance', 'Avenida da Liberdade 10 1250-142 Santo Antonio'),
    ('567-89-0123', 'Finance', 'D. Afonso Henriques 35 1000-123 Alameda'),
    ('890-12-3456', 'Human Resources', 'Rua das Cruzes 7 2664-255 Cruzadas'),
    ('345-67-8901', 'Human Resources', 'Avenida da Liberdade 10 1250-142 Santo Antonio'),
    ('678-90-1234', 'Operations', 'Rua das Cruzes 7 2664-255 Cruzadas'),
    ('901-23-4567', 'Operations', 'Rua dos Clerigos 5 4050-205 Vitoria'),
    ('111-22-3333', 'Productions', 'Rua das Cruzes 7 2664-255 Cruzadas'),
    ('222-33-4444', 'Productions', 'Rua das Cruzes 7 2664-255 Cruzadas');


INSERT INTO product (sku, "name", "description", price, ean)
VALUES 
    ('SKU111', 'Product 1', 'This is the description of product 1.', 9.99, 5901234123457),
    ('SKU222', 'Product 2', 'This is the description of product 2.', 24.99, 8712345678901),
    ('SKU333', 'Product 3', 'This is the description of product 3.', 49.99, 1234567890123),
    ('SKU444', 'Product 4', 'This is the description of product 4.', 64.99, NULL),
    ('SKU555', 'Product 5', 'This is the description of product 5.', 89.99, NULL);


INSERT INTO contains (order_no, sku, qty)
VALUES
    (1, 'SKU111', 1),
    (2, 'SKU111', 2),
    (3, 'SKU111', 3),
    (4, 'SKU111', 4),
    -- Mistura
    (5, 'SKU111', 5),
    (5, 'SKU444', 6),
    (6, 'SKU222', 7),
    (6, 'SKU333', 8),
    (6, 'SKU555', 9),
    -- Abaixo
    (7, 'SKU333', 10),
    (7, 'SKU222', 11),
    (8, 'SKU111', 12),
    (8, 'SKU222', 13),
    -- Acima
    (9, 'SKU444', 14),
    (9, 'SKU555', 15),
    (10, 'SKU444', 16),
    (10, 'SKU555', 17),
    (11, 'SKU333', 35);

-- 2.2
INSERT INTO contains (order_no, sku, qty)
SELECT
    generate_series(12, 376),
    'SKU111',
    1;

-- 2.3
INSERT INTO contains (order_no, sku, qty)
SELECT
    generate_series(377, 383),
    'SKU111',
    1;

INSERT INTO supplier (tin, "name", "address", sku, "date")
VALUES
    ('123456789', 'John Doe', 'Rua do Cacto 12 1200-234 Alcantara', 'SKU111', DATE '2023-05-21'),
    ('987654321', 'Jane Smith', 'Rua Do Grilo 22 5000-500 Porto', 'SKU222', DATE '2023-05-21'),
    ('456789123', 'David Johnson', 'Rua D. Sancho I 65 2955-500 Almada', 'SKU333', DATE '2023-05-21'),
    ('321654987', 'Emily Davis', 'Largo D. Afonso Henriques 25 3004-500 Ramada', 'SKU444', DATE '2023-05-21'),
    ('789123456', 'Michael Wilson', 'Rua das Rosas 123 1000-500 Alvalade', 'SKU555', DATE '2023-05-21');
    -- SKU444 e SKU555 acima de 50$
    -- SKU444 mais vendido
    -- SKU555 mais encomendado

INSERT INTO delivery ("address", tin)
VALUES
    ('D. Afonso Henriques 35 1000-123 Alameda', '123456789'),
    ('D. Afonso Henriques 35 1000-123 Alameda', '987654321'),
    ('D. Afonso Henriques 35 1000-123 Alameda', '456789123'),
    ('Rua das Cruzes 7 2664-255 Cruzadas', '321654987'),
    ('Rua das Cruzes 7 2664-255 Cruzadas', '789123456');
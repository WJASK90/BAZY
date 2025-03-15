USE wjaskot

--tworzenie i modyfikacja tabeli

SELECT DB_NAME() --powie w jakim kontekscie bazy danych pracujemy

CREATE TABLE Customers (
    customer_id INT PRIMARY KEY,
    first_name VARCHAR(255) NOT NULL, --ciag znakow z pojemnoscia 255 byte'ow i bez null
    birth_date DATE NOT NULL
) --w nawiesi dajemy kolumny

DROP TABLE Customers

SELECT * FROM Customers

CREATE TABLE Customers (
    customer_id INT PRIMARY KEY,
    first_name VARCHAR(255) NOT NULL, --ciag znakow z pojemnoscia 255 byte'ow i bez null
    birth_date DATE NOT NULL,
    WrongColumnName DATE
)

ALTER TABLE Customers DROP COLUMN WrongColumnName
ALTER TABLE Customers ADD new_column INT NOT NULL

EXEC sp_rename 'Customers.new_column', 'changed_column', 'COLUMN'

ALTER TABLE Customers DROP COLUMN changed_column

-- INSERT
--dodajemy customera
INSERT INTO Customers(customer_id, first_name, birth_date)
VALUES (1, 'Andrzej', '2000-01-01')

INSERT INTO Customers(customer_id, first_name, birth_date)
VALUES (2, 'Michał', '2000-01-01')

DELETE FROM Customers -- WHERE customer_id = 1, DELETE usuwa wiersz po wierszu
TRUNCATE TABLE Customers --usuwanie wszystkiego naraz, usuwa cale strony

CREATE TABLE Test (
    ID INT PRIMARY KEY,
    col_2 INT NULL,
    col_3 INT NOT NULL
)

INSERT INTO Test(ID, col_2, col_3)
VALUES (1, 1 , 1)

CREATE TABLE Test (
    ID INT PRIMARY KEY,
    col_2 INT NULL,
    col_3 INT NOT NULL
)

INSERT INTO Test(ID, col_2, col_3)
VALUES (2, null , 1)

INSERT INTO Test(ID, col_3)
VALUES (3, 1)

INSERT INTO Test(ID, col_3)
VALUES (3, null)

CREATE SCHEMA sqltest

CREATE TABLE sqltest.Test
(
    ID INT PRIMARY KEY,
    col_2 INT NULL,
    col_3 INT NOT NULL
)

DROP TABLE sqltest.Test --usuwamy tabele w sqltest

CREATE TABLE Customers (
    customer_id INT PRIMARY KEY IDENTITY,
    first_name VARCHAR(255) NOT NULL, --ciag znakow z pojemnoscia 255 byte'ow i bez null
    birth_date DATE NOT NULL DEFAULT GETDATE(),
)

ALTER TABLE Customers
    ADD CONSTRAINT DF_birth_date DEFAULT GETDATE() FOR brith_date
ALTER TABLE Customers
    ADD CONSTRAINT

CREATE TABLE Orders
(
    order_id INT PRIMARY KEY IDENTITY,
    order_date DATE NOT NULL,
    order_fk_customer_id INT FOREIGN KEY REFERENCES Customers(customer_id) -- tworzymy na nowo, customer_id to klucz obcy
)--Customers(Customer_id)

ALTER TABLE Orders
    ADD CONSTRAINT FK_Orders_Customers_customer_id FOREIGN KEY(order_fk_customer_id)
    REFERENCES Customers(customer_id)
        ON DELETE SET NULL



DELETE FROM Customers WHERE customer_id = 1

ALTER TABLE Orders DROP CONSTRAINT FK_Orders_Customers_customer_id

INSERT INTO Customers(customer_id, first_name, birth_date)
VALUES (1, 'Andrzej', '2000-01-01')

INSERT INTO Customers(customer_id, first_name, birth_date)
VALUES (2, 'Michał', '2000-01-01')

INSERT INTO Orders(order_date, customer_id)
VALUES ('2000-01-01', 1) --tak jak Andrzej

INSERT INTO Orders(order_date, customer_id)
VALUES (GETDATE(), 10) --GETDATE() to jest aktualna data

DELETE FROM Customers WHERE customer_id = 1

DELETE FROM Customers WHERE customer_id = 2
TRUNCATE TABLE Customers



--jak usuniesz z tabeli z DELETE i potem znowu insert to otrzymasz indeks 3 na michała a nie 2



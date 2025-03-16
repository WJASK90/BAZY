CREATE TABLE accounts
(
    account_id INT PRIMARY KEY IDENTITY, --klucz główny autoinkrementalny
    name       VARCHAR(255) NOT NULL,
    balance    FLOAT        NOT NULL,
)

CREATE TABLE transactions
(
    transaction_id   INT PRIMARY KEY IDENTITY,
    account_id       INT FOREIGN KEY REFERENCES accounts (account_id),
    transaction_time DATETIME,
    amount           FLOAT,
)

CREATE TABLE workers
(
    pesel      VARCHAR(11) PRIMARY KEY,
    first_name VARCHAR(255) NOT NULL,
    last_name  VARCHAR(255) NOT NULL,
    birthday   DATE         NOT NULL CHECK (birthday < GETDATE()) --GETDATE czyli dzisiejsza data
)

ALTER TABLE workers
    ADD address_id INT

INSERT INTO workers (pesel, first_name, last_name, birthday)
VALUES ('333333', 'Martyna', 'Kowalska', '2000-01-01')

CREATE TABLE address
(
    address_id  INT PRIMARY KEY IDENTITY,
    country     VARCHAR(255) NOT NULL,
    city        VARCHAR(255) NOT NULL,
    street      VARCHAR(255) NOT NULL,
    postal_code VARCHAR(25)  NOT NULL
)
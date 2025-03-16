#LABORATORIUM 1 data 16.03.2025

import datetime
from database_one import connection


class Account:
    def __init__(self, name: str, opening_balance: float = 0.0):
        self.name = name
        self.balance = opening_balance

        connection.execute("INSERT INTO accounts(name, balance) VALUES (?, ?)",
                           (self.name, self.balance))
        cursor = connection.execute("SELECT @@IDENTITY AS ID")

        self.id = cursor.fetchval()

        connection.commit()

        print(f'Konto zostało utworzone dla {self.name} z balansem {self.balance}')

    def deposit(self, amount: float, auto_commit:bool = True) -> float: #ustawiamy autocommit
        if amount > 0:
            self.balance += amount
            connection.execute("UPDATE accounts SET balance = ? WHERE account_id = ?", (self.balance, self.id))
            connection.execute("INSERT INTO transactions(account_id, transaction_time, amount) VALUES (?,?,?)",
                               # trzy ? bo mam trzy wartosci
                               (self.id, datetime.datetime.now(), amount))
            if auto_commit:
                connection.commit()
            print(f"Na konto {self.name} zostało dodane {amount} PLN")
        return round(self.balance, 2)

    def withdraw(self, amount: float, auto_commit:bool = True) -> float:
        if 0 < amount <= self.balance:
            self.balance -= amount
            connection.execute("UPDATE accounts SET balance = ? WHERE account_id = ?", (self.balance, self.id))
            connection.execute("INSERT INTO transactions(account_id, transaction_time, amount) VALUES (?,?,?)",
                               # trzy ? bo mam trzy wartosci
                               (self.id, datetime.datetime.now(), -amount))
            if auto_commit:
                connection.commit()
            print(f"Z konta {self.name} zostało wypłacone {amount} PLN")
        else:
            raise ValueError('Nie masz wystarczających środków na koncie')
        return round(self.balance, 2)

    def send_founds(self, amount: float, account):

        try:
            self.withdraw(amount, auto_commit=False)
            account.deposit(amount, auto_commit=False)
            if account.withdraw(amount) > account.balance:
                connection.commit()
        except:
            print("Brak środków, spróbuj ponownie!")
            connection.rollback()

    def show_transaction(self):


if __name__ == '__main__':
    account_jan = Account('Jan', 10)
    account_michal = Account('Michał', 10)
    account_jan.send_founds(7, account_michal)


    # account = Account('Andrzej')
    # account.deposit(10)
    # account.deposit(0.1)
    # balance = account.withdraw(5)
    # print(balance)


    # def send_founds(self, amount: float, account):
    #     self.withdraw(amount, auto_commit=False)
    #     account.deposit(amount, auto_commit=False)
    #     connection.commit()
    #     if account.withdraw(amount) > account.balance:
    #         try:
    #             float(input('Nie masz wystarczających środków, podaj poprawną liczbę środków' + {}))
    #             connection.commit()
    #         except:
    #             print("Podana wartość jest niepoprawna, spróbuj ponownie")
    #             connection.rollback()
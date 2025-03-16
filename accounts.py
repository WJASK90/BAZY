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
        self.withdraw(amount, auto_commit=False)
        account.deposit(amount, auto_commit=False)
        connection.commit()

if __name__ == '__main__':
    # account = Account('Andrzej')
    # account.deposit(10)
    # account.deposit(0.1)
    # balance = account.withdraw(5)
    # print(balance)
    account_jan = Account('Jan', 10)
    account_michal = Account('Michał', 10)
    account_jan.send_founds(7, account_michal)

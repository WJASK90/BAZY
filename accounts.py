from database_one import connection

class Account:
    def __init__(self, name: str, opening_balance: float = 0.0):
        self.name = name
        self._balance = opening_balance

        connection.execute("INSERT INTO accounts(name, balance) VALUES (?, ?)",
                           (self.name, self._balance))
        connection.execute("SELECT @@IDENITY AS ID")

        self.id = cursor.fetchval()

        connection.commit()

        print(f'Konto zostało utworzone dla {self.name} z balansem {self.balance}')

    def deposit(self, amount: float) -> float:
        if amount > 0:
            self.balance += amount
            print(f"Na konto {self.name} zostało dodane {amount} PLN")
        return round(self.balance, 2)

    def withdraw(self, amount: float) -> float:
        if 0 < amount <= self._balance:
            self._balance -= amount
            print(f"Z konta {self.name} zostało wypłacone {amount} PLN")
        return round(self._balance, 2)

    if __name__ == '__main__':
        account = Account('Andrzej')
        account.deposit(10)
        account.deposit(0.1)
        balance = account.withdraw(5)
        print(balance)




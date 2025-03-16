import pyodbc
import os
from dotenv import load_dotenv
#TWORZENIE BAZY DANYCH
load_dotenv()
# print(os.environ.get('DATABASE_PASSWORD')) #plik .env nie moze zostac pushowany na GIT bo ma haslo, nie wolno tak robic!
database_password = os.environ.get('DATABASE_PASSWORD') #bierze z pliku haslo
suszi_login = 'wjaskot'
server = 'morfeusz.wszib.edu.pl'

connection_string = (
    'DRIVER={ODBC Driver 17 for SQL Server};' #musimy pokazac do jakiego serwera sie podlaczymy
    f'SERVER={server};' #piszemy jedno pod drugim dla lepszej skladni
    f'DATABASE={suszi_login};' # database
    f'UID={suszi_login};' # user ID
    f'PWD={database_password};' # password
    'Encrypt=no' # zazwyczaj nie piszemy, bo wtedy defaultowo mamy certyfikaty a tutaj, do nauki, nie potrzebujemy (jak w SQL Microsoft ustawiasz Encryption: Optional)
)
connection= pyodbc.connect(connection_string)

# for d in pyodbc.drivers():
#     print(d)

# Start Tranzakcji
# connection.execute("CREATE TABLE users(id int identity, name varchar(255), age int)") #tworzymy tabele komendami z SQL! Tworz table
#Start tranzakcji 1
# connection.execute("INSERT INTO users(name, age) VALUES ('Andrzej', 28), ('Maciej',30)") #dodaj do Tabeli czyli insert
#Commit tranzakcji 1
# connection.commit() #uwaga trzeba zakomentowac CREATE TABLE po pierwszym stworzeniu bo inaczej program bedzie pisal
#ze jest blad bo juz istnieje o takim imieniu!

#Start tranzakcji 2 która NIE MA COMMITA
# connection.execute("INSERT INTO users(name, age) VALUES ('Jan', 30)")

cursor = connection.cursor() #kursor iteruje bo elementach bazy danych? UWAGA Kursor iteruje do przodu, nie moze sie cofać!

new_name = input('Podaj nowe imię: ')
old_name = input('Podaj stare imię: ')

#PREPARED STATEMENT uzywamy aby bronic sie przed SQL INJECTION
cursor.execute("UPDATE users SET name='?' WHERE name =?", (new_name,))
cursor.commit()

print(f'{cursor.rowcount} wierszy zmienionych')
# cursor.execute("SELECT * FROM users") #select wszystkich kolumn z Tabeli users

# cursor.execute("SELECT name FROM users") # z print(cursor.fetchval()) daje jako wynik ANDRZEJ

# print(cursor.fetchall())

# for row in cursor:
#     print(row) #pokazuje nam Andrzeja i Macieja --> ROW jest krotką! Czyli TUPLE

# for user_id, name, age in cursor:
#     print(user_id, name, age, sep='\n')

# result = cursor.fetchall()
# result = cursor.fetchmany(2)
# print(result)

# print(cursor.fetchval())

# for row in connection.execute("SELECT name FROM users"): # jak to jest zakomentowane # cursor.execute("SELECT name FROM users") to wtedy dziala
#     print(row)

# for now in cursor:
#     print(row[0])

# print(result)
# print(cursor.fetchone())
# print(cursor.fetchone())
# print(cursor.fetchall())

cursor.close() #zamykamy połączenia
connection.close() #zamykamy połączenia

# for row in result:
#     print(row)
#
# for row in result:
#     print(row)

# cursor = connection.cursor() #kursor iteruje bo elementach bazy danych? UWAGA Kursor iteruje do przodu, nie moze sie cofać!
#
# new_name = input('Podaj nowe imię: ')
#
# cursor.execute("UPDATE users SET name='{new_name}' WHERE name = 'Andrzej'")
# cursor.commit()
#
# print(f'{cursor.rowcount} wierszy zmienionych')



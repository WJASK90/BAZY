import os

from dotenv import load_dotenv
from sqlalchemy import *
from sqlalchemy import create_engine

load_dotenv()

database_password = os.environ.get('DATABASE_PASSWORD')
suszi_login = 'wjaskot'
server = 'morfeusz.wszib.edu.pl'
driver = 'ODBC+Driver+17+for+SQL+Server'

# dialect+driver://username:password@host:port/database?dodtkowe_opcje_klucz_wartość
engine = create_engine(
    f'mssql+pyodbc://{suszi_login}:{database_password}@{server}/{suszi_login}?driver={driver}&Encrypt=no',
    echo=False
)

metadata = MetaData()

worker_table = Table('workers', metadata, #nazwa, metadane
                     Column('pesel', String(11), primary_key=True), #klucz glowny
                     Column('first_name', String(255), nullable=False),
                     Column('last_name', String(255), nullable=False),
                     Column('birthday', Date, nullable=False),
                     Column('address_id', Integer, ForeignKey('address.address_id')) #klucz obcy
                     )

address_table = Table('address', metadata, #nazwa, metadane
                      Column('address_id', Integer, primary_key=True, autoincrement=True), #klucz glowny
                      Column('country', String(255), nullable=False),
                      Column('city', String(255), nullable=False),
                      Column('street', String(255), nullable=False),
                      Column('postal_code', String(255), nullable=False),
                      )

connection = engine.connect()

#laczenie tabel jest proste kiedy mamy oznaczone w kodzie klucze glowne i obce

#ZŁĄCZENIE INNER
if __name__ == '__main__':
    query = select(worker_table.join(address_table)) #metoda JOIN przekuzujesz co chcesz laczyc czyli address_table
    result = connection.execute(query)
    print(worker_table.join(address_table))
    print(result.fetchall()) #mozna tez print(result.all())

#ZŁĄCZENIE + konkretne kolumny
    query = select(worker_table.c.pesel, address_table.c.country) \
        .select_from(worker_table.join(address_table)) #metodata SELECT FROM
    result = connection.execute(query)
    print(result.all()) #tylko PESEL i tylko PANSTWO

#ZŁĄCZENIE + konkretne kolumny - 2
    query = select(worker_table.c.pesel, address_table.c.country) \
        .join_from(worker_table, address_table) #metoda JOIN
    result = connection.execute(query)
    print(result.all()) #tylko PESEL i tylko PANSTWO

#ZŁĄCZENIE + konkretne kolumny - 3
    query = select(worker_table.c.pesel, address_table.c.country) \
        .join(address_table) #metoda JOIN gdzie sql dedukuje ze laczymy worker i address, sam sie tego "domyslil", musza byc tylko 2 do wyboru
    result = connection.execute(query)
    print(result.all()) #tylko PESEL i tylko PANSTWO

# ZŁĄCZENIE + konkretne kolumny + ON
    query = select(worker_table, address_table.c.country) \
        .join(worker_table, worker_table.c.address_id == address_table.c.address_id)
    result = connection.execute(query)
    print(result.all())  #

# Potwierdzenie ze zlaczenie jest INNER
    query = select(worker_table, address_table.c.country) \
        .join(worker_table).where(worker_table.c.last_name == 'Kozłowski')
    result = connection.execute(query)
    print(result.all())  #szukamy wszystkie wyniki z nazwiskiem KOZŁOWSKI, wynik: nie znaleziony

#ALIAS tabeli
    w = worker_table.alias()
    a = address_table.alias()

    query = select(w, a.c.country) \
        .join(w)
    result = connection.execute(query)
    print(result.all())

# Left join ze zmienna ISOUTER=TRUE
    query = select(worker_table, address_table.c.country) \
        .join(address_table, isouter=True) \
        .where(worker_table.c.last_name == 'Kozłowski')
    result = connection.execute(query)
    print(result.all())  #

#Full combo (wszystkie metody?)
    query = select(func.year(worker_table.c.birthday), func.count().label("Liczba urodzonych w danym roku w Krakowie")) \
    .join(address_table) \
    .where(address_table.c.city == 'Kraków') \
    .group_by(func.year(worker_table.c.birthday)) \
    .order_by(Column('Liczba urodzonych w danym roku w Krakowie').desc()) \
    .having(func.count() > 1)

result = connection.execute(query)
print(result.all())

#INSERT
# insert_sql = insert(address_table) \
#     .values(country='Polska', city='Kraków', street='Aleja Kijowska 15', postal_code='30-387')
# connection.execute(insert_sql)
# connection.commit() #musi być COMMIT aby zaktualizować, dodalismy nowy adres do tabeli

# insert_many = insert(worker_table)
# connection.execute(insert_many, [
#     {'pesel': '1111111111', 'first_name': 'Nowy', 'last_name': 'Jeden', 'birthday': '2000-01-01', 'address_id': 1002},
#     {'pesel': '2222222222', 'first_name': 'Nowy', 'last_name': 'Dwa', 'birthday': '2000-01-01', 'address_id': 1002},
# ])
# connection.commit() #dodajemy wiecej niz jeden wiersz do naszej tabeli

#insert skomentowany poniewaz kolejne odswiezenia beda duplikatami i beda bledy

#UPDATE
update_sql = update(worker_table).values(first_name='Zmienione').where(worker_table.c.address_id == 1002)
connection.execute(update_sql)
connection.commit()

# Delete #delete(tabela).gdzie(co takiego)
delete_sql = delete(worker_table).where(worker_table.c.address_id == 1002)
connection.execute(update_sql)
connection.commit()

#INSERT - 2
insert_sql = insert(address_table) \
    .values(country='Polska', city='Kraków', street='Aleja Kijowska 15', postal_code='30-387')
result = connection.execute(insert_sql)

new_address_id = result.inserted_primary_key[0]

insert_many = insert(worker_table)
connection.execute(insert_many, [
    {'pesel': '1111111111', 'first_name': 'Nowy', 'last_name': 'Jeden', 'birthday': '2000-01-01', 'address_id': new_address_id},
    {'pesel': '2222222222', 'first_name': 'Nowy', 'last_name': 'Dwa', 'birthday': '2000-01-01', 'address_id': new_address_id},
])
connection.commit()
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
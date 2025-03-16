# for driver in pyodbc.drivers(): #sprawdzamy jakie mamy drivery
#     print(driver)
#https://docs.sqlalchemy.org/en/20/core/ INFORMACJE O SQL ALCHEMY CORE!!!!!!!!!

import os
from sqlalchemy import create_engine
import sqlalchemy

from dotenv import load_dotenv

load_dotenv()

database_password = os.environ.get('DATABASE_PASSWORD')  # bierze z pliku haslo
suszi_login = 'wjaskot'
server = 'morfeusz.wszib.edu.pl'
driver = 'ODBC+Driver+17+for+SQL+Server'

# dialect+driver://username:password@host:port/database?dodatkowe_opcje_klucz_wartość
engine = create_engine(
    f'mssql+pyodbc://{suszi_login}:{database_password}@{server}/{suszi_login}?driver={driver}&Encrypt=no',
    echo=False #dzieki temu widzimy co SQLAlchemy robi aby dojsc do wyniku
)

# connection = engine.connect()

# query = sqlalchemy.text("SELECT * FROM workers WHERE pesel=:filter_pesel")
# result = connection.execute(query, {"filter_pesel": '111111'})
# print(result.fetchall())

# connection.close()


metadata = sqlalchemy.MetaData()

worker_table = sqlalchemy.Table('workers', metadata,  # deklarujemy jak tabela wyglada
                                sqlalchemy.Column('pesel', sqlalchemy.String(11), primary_key=True),
                                sqlalchemy.Column('first_name', sqlalchemy.String(255), nullable=False),
                                sqlalchemy.Column('last_name', sqlalchemy.String(255), nullable=False),
                                sqlalchemy.Column('birthday', sqlalchemy.Date, nullable=False),
                                sqlalchemy.Column('address_id', sqlalchemy.Integer),
                                )


connection = engine.connect()

# query = sqlalchemy.text("SELECT * FROM workers WHERE pesel=:filter_pesel")
query = sqlalchemy.select(worker_table)
result = connection.execute(query)
print(result.fetchall())

# perpared statement?
expression = worker_table.columns.first_name == 'Andrzej'
print(type(expression))
print(expression.compile().params)
print(worker_table.columns.first_name == 'Andrzej')

query = sqlalchemy.select(
    worker_table.c.first_name, #c. to column
    worker_table.c.last_name
)

#inny sposob zapisania tego co jest na gorze
# query = sqlalchemy.select(
#     worker_table.c['first_name', 'last_name']
# )

result = connection.execute(query)
print(result.fetchall())

# Limit/Top
query = sqlalchemy.select(worker_table).limit(2)
result = connection.execute(query)
print(result.fetchall())

# print('Andrzej' == 'Janek')

#Sortowanie, też może mieć limit(2)
query = (sqlalchemy.select(worker_table) \
         .order_by(worker_table.c.first_name.desc(),
                   worker_table.c.last_name.desc()
                   ))
result = connection.execute(query)
print(result.fetchall())

#Sortowanie 2
query = sqlalchemy.select(worker_table) \
         .order_by(worker_table.c.first_name.desc()) \
         .order_by(worker_table.c.last_name) \
         .limit(2) \
         .offset(1)

result = connection.execute(query)
print(result.fetchall())

# Filtrowanie
query = sqlalchemy.select(worker_table) \
    .where(worker_table.c.pesel == '11111')
result = connection.execute(query)
print(result.fetchall())

# print(type(query))
# print(query)
# print(query.compile().params)

#AND
query = sqlalchemy.select(worker_table) \
    .where((worker_table.c.address_id > 1) & (worker_table.c.address_id < 4))
result = connection.execute(query)
print(result.fetchall())

#AND 2
query = sqlalchemy.select(worker_table) \
    .where(worker_table.c.address_id > 1) \
    .where(worker_table.c.address_id < 4)
result = connection.execute(query)
print(result.fetchall())

#AND 3
query = sqlalchemy.select(worker_table) \
    .where(sqlalchemy.and_(worker_table.c.address_id > 1, worker_table.c.address_id < 4))
result = connection.execute(query)
print(result.fetchall())

# OR  uzywamy pipe |
query = sqlalchemy.select(worker_table) \
    .where((worker_table.c.address_id > 1) | (worker_table.c.address_id < 4))
result = connection.execute(query)
print(result.fetchall())

#OR 2
query = sqlalchemy.select(worker_table) \
    .where(sqlalchemy.or_(worker_table.c.address_id > 1, worker_table.c.address_id < 4))
result = connection.execute(query)
print(result.fetchall())

#imie Andrzej lub Martyna i Adres Id > 2
query = sqlalchemy.select(worker_table) \
    .where(
    (worker_table.c.first_name == 'Andrzej') |
    (worker_table.c.first_name == 'Martyna') &
    (worker_table.c.address_id > 1)
)
result = connection.execute(query)
print(result.fetchall())

# query = sqlalchemy.select(worker_table) \
#     .where(
#     sqlalchemy.and_(
#         sqlalchemy.or_(worker_table.c.first_name == 'Andrzej', worker_table.c.first_name == 'Martyna'),
#         worker_table.c.address_id > 1),
#     )
# )
# result = connection.execute(query)
# print(result.fetchall())

query = sqlalchemy.select(worker_table) \
    .where(
    sqlalchemy.and_(
        worker_table.c.first_name.in_(['Andrzej', 'Martyna']),
        worker_table.c.address_id > 1
    )
)
result = connection.execute(query)
print(result.fetchall())

#LIKE
query = sqlalchemy.select(worker_table) \
    .where(worker_table.c.first_name.like('And%')) #najpierw musi byc where a reszta nie jest tak wazna, jesli chodzi o porzadek
result = connection.execute(query)
print(result.fetchall())


#Agregacja, mozemy tez filtrowac z WHERE
query = sqlalchemy.select(sqlalchemy.func.count()).select_from(worker_table)
result = connection.execute(query)
print(result.scalar()) #wynik ktory rozpakowuje pierwsza kolumen ktora dostajemy w wyniku, zwraca 1 kolumne z 1 wiersza

# Min/Max, mozemy tez filtrowac z WHERE
query = sqlalchemy.select(sqlalchemy.func.min(worker_table.c.birthday))
result = connection.execute(query)
print(result.scalar())

#grupowanie
query = sqlalchemy.select(sqlalchemy.func.year(worker_table.c.birthday), sqlalchemy.func.count()) \
    .group_by(sqlalchemy.func.year(worker_table.c.birthday))
result = connection.execute(query)
print(result.fetchall())

connection.close()
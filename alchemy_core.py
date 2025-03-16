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

# print('Andrzej' == 'Janek')

connection.close()
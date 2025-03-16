# for driver in pyodbc.drivers(): #sprawdzamy jakie mamy drivery
#     print(driver)

import os
import pyodbc
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
)

connection = engine.connect()

result = connection.execute(sqlalchemy.text("SELECT * FROM workers"))
print(result.fetchall())

connection.close()
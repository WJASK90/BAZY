import os

from dotenv import load_dotenv
from sqlalchemy import *
from sqlalchemy import create_engine

load_dotenv()

database_password = os.environ.get('DATABASE_PASSWORD')
suszi_login = 'chudzick'
server = 'morfeusz.wszib.edu.pl'
driver = 'ODBC+Driver+17+for+SQL+Server'

# dialect+driver://username:password@host:port/database?dodtkowe_opcje_klucz_wartość
engine = create_engine(
    f'mssql+pyodbc://{suszi_login}:{database_password}@{server}/{suszi_login}?driver={driver}&Encrypt=no',
    echo=False
)

metadata = MetaData()

worker_table = Table('workers', metadata, #nazwa, metadane
                     Column('pesel', String(11), primary_key=True),
                     Column('first_name', String(255), nullable=False),
                     Column('last_name', String(255), nullable=False),
                     Column('birthday', Date, nullable=False),
                     Column('address_id', Integer)
                     )

address_table = Table('address', metadata, #nazwa, metadane
                      Column('address_id', Integer, primary_key=True, autoincrement=True),
                      Column('country', String(255), nullable=False),
                      Column('city', String(255), nullable=False),
                      Column('street', String(255), nullable=False),
                      Column('postal_code', String(255), nullable=False),
                      )

connection = engine.connect()
import os
from sqlalchemy import create_engine
import sqlalchemy
from dotenv import load_dotenv
from sqlalchemy.orm import sessionmaker
from sqlalchemy.schema import CreateSchema
from alchemy_orm import Base

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

Session = sessionmaker(engine)

if __name__ == '__main__':
    # session = Session()
    # session.execute(CreateSchema('Library_orm')) #schemat
    # session.commit() #schemat
    Base.metadata.create_all(engine)
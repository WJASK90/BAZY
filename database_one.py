import os

import pyodbc

# for driver in pyodbc.drivers(): #sprawdzamy jakie mamy drivery
#     print(driver)

from dotenv import load_dotenv
load_dotenv()

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




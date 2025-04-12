from orm_connection import Session
from sqlalchemy import *
from alchemy_orm import Author

session = Session()


select_authors = select(Author) #referencja do klasy Author
all_authors = session.execute(select_authors).scalars().all()
print(all_authors)

for a in all_authors:
    print(f'Autor {a.name} napisał {len(a.books)} książek i mieszka w {a.address.country} {a.address.city}')
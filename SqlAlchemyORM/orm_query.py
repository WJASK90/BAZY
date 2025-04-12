from orm_connection import Session
from sqlalchemy import *
from sqlalchemy.orm import joinedload
from alchemy_orm import Author, Address, Book
import datetime

session = Session()

#jeden autor - 1
select_authors = select(Author).options(joinedload(Author.books), joinedload(Author.address)).filter_by(id=1) #referencja do klasy Author / w options podajem tabele ktore chcemy dociagnac / metoda filter_by po id filter_by(id=1) albo .where(Author.id > 1)
a = session.execute(select_authors).unique().scalar_one() #.all() #dodajemy metode unique() przed all() #z filter_by(id=1) i scalar_one() zamiast scalars bedziemy mieli w wyniku 1 autora

print(f'Autor {a.name} napisał {len(a.books)} książek i mieszka w {a.address.country} {a.address.city}')

#jeden autor - 2
a = session.get(Author, 9999)
print(a)

# Insert #(autor = konstruktor)
# author = Author(name='Andrzej', email='email', login='login', middle_name='middle')
# author.address = Address(country='Litwa', city='Wilno')
# author.books = [
#     Book(title='Jeden', publication_date=datetime.date.today()),
#     Book(title='Dwa', publication_date=datetime.date.today()),
# ]
#
# session.add(author)
# session.commit()

# UPDATE - cascade delete-orphan
author = session.get(Author, 7)
author.middle_name = 'Jan'
for b in author.books[:1]:
    if b.title == 'Jeden':
        b.description = 'To jest pierwsza książka!'

session.add(author)
session.commit()

#DELETE
author = session.get(Author, 7)
session.delete(author)
session.commit()




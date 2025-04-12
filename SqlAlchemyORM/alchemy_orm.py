from typing import Optional, Annotated, List
from sqlalchemy import *
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped, relationship #Mapped jest klasą generyczną można w [] podawać typ danych
import datetime


str255 = Annotated[str, mapped_column(String(255))]
intpk = Annotated[int, mapped_column(Integer, primary_key=True, autoincrement=True)]

library_metadata = MetaData(schema = 'library_orm')

Base = DeclarativeBase()

class Base(DeclarativeBase):
    metadata = library_metadata #wszystkie klasy beda rejestrowane pod nasze Metadaty

events_authors = Table(
    'events_authors',
    Base.metadata,
    Column('author_id', ForeignKey('author.id')),
    Column('event_id', ForeignKey('event.id')),
)

# class Base(DeclarativeBase):
    # type_annotation_map = {
    #     str255: String(255)
    # }

class Author(Base): #klasa o naszych Użytkownikach, którzy mają odpowiedniki w tabeli
    __tablename__ = 'author'
    
    id: Mapped[intpk] #było = mapped_column(primary_key=True, autoincrement=True) ale dajemy intpk #definiujemy zmienna na naszej Klasie i kolumne INTEGER, Klucz Glowny i autoinkrementalna
    name: Mapped[str] = mapped_column(String()) #odpowiednik VARCHAR(MAX)
    email: Mapped[str255] #było = mapped_column(String(255)) ale dzieki Annotated nie musze tego pisac #string o rozmiarze 255 bite'ow
    login: Mapped[str] = mapped_column(String(100), default='No Login')
    middle_name: Mapped[Optional[str]] #było tak = mapped_column(String(255), nullable=True) ale dzięki optional (import na gorze) możemy usunąć

    books: Mapped[List['Book']] = relationship(back_populates='author', cascade='all, delete, delete-orphan') #połączenie z relationship(back_populates='books')
    address: Mapped['Address'] = relationship(back_populates='author', cascade='all, delete, delete-orphan')

    def __str__(self):
        return f'{self.name} {self.middle_name}'

    def __repr__(self):
        return f'{self.name} {self.middle_name}'

class Event(Base):
    __tablename__ = 'event'

    id: Mapped[intpk]
    name: Mapped[str255]

    participants: Mapped[List['Author']] = relationship(secondary=events_authors)

class Address(Base):
    __tablename__ = 'address'

    id: Mapped[intpk]
    country: Mapped[str255]
    city: Mapped[str255]
    author_id: Mapped[int] = mapped_column(ForeignKey('author.id'))
    author: Mapped['Author'] = relationship(back_populates='address')

class Book(Base):
    __tablename__ = 'book'

    id: Mapped[intpk]
    title: Mapped[str255] #to samo co VARCHAR(255)
    description: Mapped[Optional[str]] #oznacza VARCHAR(MAX)
    publication_date: Mapped[datetime.date] #mamy zdefiniowaną tabele
    author_id: Mapped[int] = mapped_column(ForeignKey('author.id')) #author id = tabela i do czego sie odnosi
    author: Mapped['Author'] = relationship(back_populates='books') #połączenie z relationship(back_populates='author')
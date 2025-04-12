from typing import Optional, Annotated
from sqlalchemy import *
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped #Mapped jest klasą generyczną można w [] podawać typ danych


str255 = Annotated[str, mapped_column(String(255))]
intpk = Annotated[int, mapped_column(Integer, primary_key=True, autoincrement=True)]

Base = DeclarativeBase()

class Base(DeclarativeBase):
    pass

# class Base(DeclarativeBase):
    # type_annotation_map = {
    #     str255: String(255)
    # }

class User(Base): #klasa o naszych Użytkownikach, którzy mają odpowiedniki w tabeli
    __tablename__ = 'user'
    
    id: Mapped[intpk] #było = mapped_column(primary_key=True, autoincrement=True) ale dajemy intpk #definiujemy zmienna na naszej Klasie i kolumne INTEGER, Klucz Glowny i autoinkrementalna
    name: Mapped[str] = mapped_column(String()) #odpowiednik VARCHAR(MAX)
    email: Mapped[str255] #było = mapped_column(String(255)) ale dzieki Annotated nie musze tego pisac #string o rozmiarze 255 bite'ow
    login: Mapped[str] = mapped_column(String(100), default='No Login')
    middle_name: Mapped[Optional[str]] #było tak = mapped_column(String(255), nullable=True) ale dzięki optional (import na gorze) możemy usunąć



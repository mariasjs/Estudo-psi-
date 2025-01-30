from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import mapped_column, Mapped



class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

class User(db.Model):
    __tablename__ = 'users'
    id : Mapped[int] = mapped_column(primary_key = True)
    nome: Mapped[str]

class Livro(db.Model):
    __tablename__ = "livros"
    id : Mapped[int] = mapped_column(primary_key = True)
    titulo: Mapped[str]

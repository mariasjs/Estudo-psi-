#Esta pasta será usada para definir as estruturas das tabelas 

from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import String


#mapeamento declarativo
class Base(DeclarativeBase):
    pass

class User(Base): #Está herdando da classe Base 
    __tablename__ = 'users'
    id:Mapped[int] = mapped_column(primary_key=True)
    email:Mapped[str] = mapped_column(String(50), unique=True)
    senha:Mapped[str] = mapped_column(String(50), unique=True)

    def __repr__(self) -> str:
        return f"(email: {self.email} | senha: {self.senha})"
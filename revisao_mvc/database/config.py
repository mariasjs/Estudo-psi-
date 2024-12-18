#Arquivo usado para conectar com o  banco de dados 
#utilizado como base para o banco de dados

from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from database.models import Base


engine = create_engine("sqlite:///test.db")
session = Session(bind=engine)

def start_db():
    # criando o banco
    Base.metadata.create_all(bind=engine)
    

    session.commit ()

def destroy_db(): # destroi o banco 
    Base.metadata.drop_all(bind=engine)
    
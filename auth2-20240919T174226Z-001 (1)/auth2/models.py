#Este arquivo serve apenas como uma biblioteca, não deve ser executado 

from flask_login import UserMixin #UserMixin que implementa metodos uteis para gerenciar sessão de usuarios
import sqlite3

BANCO = 'database.db'
def obter_conexao():
    conn = sqlite3.connect(BANCO)
    conn.row_factory = sqlite3.Row
    return conn

# classe python - Modelo (acessa o banco)
class User(UserMixin):
    id : str
    def __init__(self, email, senha): #Inicia a classe user 
        self.email = email #O self informa as caracteristicas desta classe user 
        self.senha = senha #O self é um método de classe, self refere-se ao objeto específico da classe sobre o qual o método está operando. É uma referência ao próprio objeto que chamou o método.
    
    @classmethod
    def get(cls, id): #Busca usuário no banco de dados usando id
        conexao = obter_conexao()
        SELECT = 'SELECT * FROM usuarios WHERE id=?'
        dados = conexao.execute(SELECT, (id,)).fetchone()
        user = User(dados['email'], dados['senha'])
        user.id = dados['id']
        return user

    @classmethod
    def get_by_email(cls, email): #Busca usuario por email
        conexao = obter_conexao()
        SELECT = 'SELECT * FROM usuarios WHERE email=?'
        dados = conexao.execute(SELECT, (email,)).fetchone()
        if dados:    
            user = User(dados['email'], dados['senha'])
            user.id = dados['id']
            return user
        return None
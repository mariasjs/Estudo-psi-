from flask_login import UserMixin
import sqlite3

from werkzeug.security import generate_password_hash

BANCO = 'database.db'
def obter_conexao():
    conn = sqlite3.connect(BANCO)
    conn.row_factory = sqlite3.Row
    return conn

class User(UserMixin):
    id : str
    def __init__(self, matricula, email, senha):
        self.matricula = matricula
        self.email = email
        self.senha = senha

    @classmethod
    def get(cls, id):
        conexao = obter_conexao()
        SELECT = 'SELECT * FROM users WHERE id=?'
        dados = conexao.execute(SELECT, (id,)).fetchone()
        
        if dados:  
            user = User(dados['matricula'], dados['email'], dados['senha'])
            user.id = dados['id']
            return user
        else:
            return None
    @classmethod 
    def get_by_mat(cls, matricula):

        conexao = obter_conexao()
        SELECT = 'SELECT * FROM users WHERE matricula=?'
        dados = conexao.execute(SELECT, (matricula,)).fetchone()
        if dados != None:
            user = User(dados['matricula'],dados['email'], dados['senha'])
            user.id = dados['id']
            return user
        else:
            return None
        
    
    @classmethod
    def insert_user(cls, matricula, email, senha):
        hash_email = generate_password_hash(email)
        hash_senha = generate_password_hash(senha)

        conexao = obter_conexao()
        INSERT = 'INSERT INTO users(matricula,email,senha) VALUES (?,?,?)'
        conexao.execute(INSERT,  (matricula, hash_email, hash_senha))
        conexao.commit()
        conexao.close()

    @classmethod
    def insert_exercicios(cls, nome, comentario, usuario):
        conexao = obter_conexao()
        INSERT = 'INSERT INTO exercicios(nome,comentario, usuario) VALUES (?,?,?)'
        conexao.execute(INSERT,  (nome, comentario, usuario))
        conexao.commit()
        conexao.close()
    
   
        




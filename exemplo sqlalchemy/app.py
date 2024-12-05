from flask import Flask, request, render_template, \
    redirect, url_for, flash
from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.orm import sessionmaker, declarative_base

app = Flask(__name__)

db = create_engine("sqlite:///meubanco.db")
Session = sessionmaker(bind=db)
session = Session()

Base = declarative_base()

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    email = Column("email", String)
    senha = Column("senha", String)

    def __init__(self,email, senha):
        self.email = email
        self.senha = senha

Base.metadata.create_all(bind=db)
      

@app.route('/')
def index():
    usuarios = session.query(Usuario).all()

    return render_template('pages/index.html', usuarios = usuarios)

@app.route('/create', methods=['POST', 'GET'])
def create():
    if request.method == 'POST':
        email = request.form['email']
        senha= request.form['password']
        usuario = Usuario(email, senha)

        session.add(usuario)
        session.commit()
    
    
        if not email:
            flash('Email é obrigatório')
        else:
            return redirect(url_for('index'))
    
    return render_template('pages/create.html')

@app.route('/<int:id>/edit', methods=['POST', 'GET'])
def edit(id):
    usuario = session.query(Usuario).filter_by(id=id).first()

    if not usuario:
        return redirect(url_for('error', message="Usuário não encontrado"))

    if request.method == 'POST':
        email = request.form['email']
        usuario.email = email
        session.commit()
        return redirect(url_for('index'))

        
        
    return render_template('pages/edit.html', usuario = usuario)

@app.route('/error')
def error():
    error = request.args.get('message')
    return render_template('errors/error.html', message=error)
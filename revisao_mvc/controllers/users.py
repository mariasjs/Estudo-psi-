# rotas para inserir dados dos usuários 

from flask import render_template, Blueprint, url_for, request, flash, redirect
from sqlalchemy import select

from database.models import User, Base
from database.config import start_db

from database.config import session

bp = Blueprint('users', __name__, url_prefix='/users')

@bp.route('/')
def index():

    return render_template('index.html', users = User.all())

@bp.route('/cadastro', methods=['POST', 'GET'])
def cadastro():
    start_db()
    if request.method == 'POST':
        resposta_email = request.form['email']
        resposta_senha= request.form['senha']

        if not resposta_email:
            flash('Email é obrigatório')
        else:
            user = User(email=resposta_email, senha=resposta_senha) #Cria um novo usuario com os dados fornecidos no form
            session.add(user)
            session.commit()

            consulta = select(User)
            usuarios = session.scalars(consulta).all()

            return f"{usuarios}"
    return render_template('cadastro.html')
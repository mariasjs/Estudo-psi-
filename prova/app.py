from flask import Flask, request, redirect, render_template, url_for
import sqlite3
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import User

login_manager = LoginManager()
app = Flask(__name__)
app.config['SECRET_KEY'] = 'SUPERMEGADIFICIL'
login_manager.init_app(app)



def obter_conexao():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn



@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

@app.route('/', methods=["POST", "GET"])
def login():
    if request.method == "POST":
        matricula = request.form["matricula"]
        senha = request.form["senha"]

        conn = obter_conexao()
        dados = conn.execute("SELECT * FROM usuarios WHERE matricula=(?)", (matricula,)).fetchone()
        conn.commit()
        conn.close()
        if dados:
            user = User(dados["matricula"],dados["email"], dados["senha"])
            user.id = dados["id"]
        else: 
            user = None

        if user and check_password_hash(user.senha, senha):
            login_user(user)
            return redirect(url_for("dash"))
    return render_template ("login.html")

@app.route('/cadastro', methods = ["POST", "GET"])
def cadastro():
    if request.method == "POST":
        matricula = request.form["matricula"]
        senha = request.form["senha"]
        email = request.form["email"]

        sen_hash = generate_password_hash(senha)
        ema_hash = generate_password_hash(email)

        conn = obter_conexao()
        conn.execute("INSERT INTO usuarios(matricula, email, senha) VALUES(?,?,?)", (matricula,ema_hash, sen_hash))
        conn.commit()
        conn.close()

        conn = obter_conexao()
        dados = conn.execute("SELECT * FROM usuarios WHERE matricula=(?)", (matricula,)).fetchone()
        conn.commit()
        conn.close()    
        if dados:
            user = User(dados["matricula"],dados["email"], dados["senha"])
            user.id = dados["id"]
        else: 
            user = None
        

        login_user(user)
        return redirect(url_for("dash"))

    return render_template ("cadastro.html")

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

@app.route('/dash', methods = ["POST", "GET"])
@login_required
def dash():
    if request.method == "POST":
        nome = request.form["nome"]
        desc = request.form["desc"]
        id = current_user.id
        conn = obter_conexao()
        conn.execute("INSERT INTO exercicios(nome, descricao, usuario) VALUES(?,?,?)", (nome,desc,id))
        conn.commit()
        conn.close()
    return render_template ("dash.html")
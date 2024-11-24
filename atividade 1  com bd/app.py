from flask import Flask, request, render_template, url_for, \
    session, redirect
import sqlite3 

app = Flask(__name__)

def obter_conexao():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

bancodados = {}

app.config['SECRET_KEY'] = 'superdificil'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
def dash():    
    if 'user' in session:
        return render_template('dashboard.html')
    else:
        return redirect(url_for('login'))

@app.route('/login', methods=['POST', 'GET'])
def login():

    if 'user' in session:
        return redirect(url_for('dash'))

    if request.method == 'POST':
        nome = request.form['nome']
        senha = request.form['senha']

        if nome in bancodados and bancodados[nome] == senha:
            session['user'] = nome
            return redirect(url_for('dash'))
        else:
            return "Usuário não detectado no banco de dados! Caso não tenha seu cadastro ainda, realize-o" + render_template ('register.html')


    return render_template('login.html')

@app.route('/register', methods=['POST', 'GET'])
def register():

    ## esse bloco tanto para register quanto para login
    if 'user' in session:
        return redirect(url_for('dash'))

    if request.method == 'POST':
        nome = request.form['nome']
        senha = request.form['senha']
        conn = obter_conexao()
        conn.execute ("INSERT INTO tb_usuarios(nome, senha) VALUES (?,?)", (nome, senha))
        conn.commit()
        conn.close()

        if nome not in bancodados:
            bancodados[nome] = senha
            session['user'] = nome
            return redirect(url_for('dash'))
        else:
            return "Ja estas cadastrado" + render_template('dash.html')

    return render_template('register.html')

@app.route('/logout', methods=['POST', 'GET'])
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))
from flask import Flask, redirect, url_for, render_template, request
from database.models import User, Livro, db 

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///projeto.db'

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template ('index.html')

@app.route('/cad_user', methods=['POST', 'GET'])
def cad_user():
    if request.method == "POST":
        nome = request.form['nome']
        user = User(nome = nome)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('cad_liv'))
    return render_template ('cad_user.html')

@app.route('/cad_liv', methods=['POST', 'GET'])
def cad_liv():
    if request.method == "POST":
        titulo = request.form['titulo']
        livro = Livro(titulo = titulo)
        db.session.add(livro)
        db.session.commit()
        resultado = db.session.query(Livro).all()
        return render_template('index.html', resultado = resultado )
    return render_template ('cad_liv.html') 
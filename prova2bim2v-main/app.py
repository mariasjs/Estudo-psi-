from flask import Flask, render_template, url_for,request,redirect

from flask_login import LoginManager, login_required,login_user, logout_user, current_user

from werkzeug.security import check_password_hash

from models import User, obter_conexao

login_manager = LoginManager()
app = Flask(__name__)
app.config['SECRET_KEY'] = 'SUPERDIFICIL'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login',methods=['POST','GET'])
def login():
    if request.method == 'POST':
        matricula = request.form['matricula']
        email = request.form['email']
        senha = request.form['senha']

        user = User.get_by_mat(matricula)

        if user and check_password_hash(user.senha,senha):
            login_user(user)

            return redirect(url_for('dash'))
        else:
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/registro', methods=['GET','POST'])
def registro():
    if request.method == 'POST':
        matricula =  request.form['matricula']
        email = request.form['email']
        senha = request.form['senha']

        User.insert_user(matricula, email, senha)

        
        return redirect(url_for('login'))
    
    return render_template('register.html')


@app.route('/dash')
@login_required
def dash():
    return render_template('dash.html')



@app.route('/exercicios',methods=['GET','POST'])
def exercicios():
    if request.method=='POST':
        nome = request.form['nome']
        comentario = request.form['comentario']
        id = current_user.id

        User.insert_exercicios(nome, comentario, id)



        return render_template('exercicios.html', nome=nome, comentario=comentario)

    return render_template('exercicios.html')


@app.route('/logout', methods=['POST'])
def logout():
    logout_user()
    return redirect(url_for('index'))



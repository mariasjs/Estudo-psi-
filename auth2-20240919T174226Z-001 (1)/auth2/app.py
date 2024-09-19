from flask import Flask, render_template \
    , url_for, request, redirect

from flask_login import LoginManager \
    , login_required, login_user, logout_user

from models import User, obter_conexao

login_manager = LoginManager() #Gerenciador de login que será usada para gerenciar o estado de autenticação do usuário
app = Flask(__name__)
app.config['SECRET_KEY'] = 'SUPERMEGADIFICIL' #Chave secreta usada para proteger cookies de sessão e garantir segurança dos dad
login_manager.init_app(app) #Permite que o flask-login gerencie sessões e autenticações do app

# quando precisar saber qual o usuario conecato
# temos como consultar ele no banco
@login_manager.user_loader #Decorador que permite carregar um usuário com base no ID
def load_user(user_id):
    return User.get(user_id) # Recupera usuário do banco de dados por meio do ID

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['pass']
        
        user = User.get_by_email(email) #Busca usuário no banco de dados por meio do email fornecido

        if user and user.senha == senha: #Verifica se usuário foi encontrado e se senha fornecida corresponde à armazenada
            
            login_user(user) #Registra usuário na sessão

            return redirect(url_for('dash'))

    return render_template('login.html')


@app.route('/register', methods=['POST', 'GET'])
def register():

    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['pass']
        conexao = obter_conexao()#Estabelece conexão com banco de dados 
        INSERT = 'INSERT INTO usuarios(email,senha) VALUES (?,?)' #Define espaço para inserir email e senha no banco de dados 
        conexao.execute(INSERT, (email, senha))
        conexao.commit() #Confirma operação de iserção no banco
        conexao.close() #Fecha conexão
        return redirect(url_for('dash'))

    return render_template('register.html')


@app.route('/dash')
@login_required
def dash():
    return render_template('dash.html')



@app.route('/logout', methods=['POST']) #Rota para usuário sair do sistema
def logout():
    logout_user() #Ela remove o usuário da sessão atual, o que significa que, após isso, o Flask-Login não o considerará mais logado.
    return redirect(url_for('index'))



from flask import Flask, render_template
from controllers import users
from database.config import start_db  # Importa a função para criar o banco

app = Flask(__name__)

# Inicializa o banco de dados
start_db()

# Registra o blueprint de users
app.register_blueprint(users.bp)

@app.route('/')
def index():
    return render_template('index.html')

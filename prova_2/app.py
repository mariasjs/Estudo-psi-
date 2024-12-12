from flask import Flask, request, render_template, url_for, redirect, make_response, session

app = Flask(__name__)
app.secret_key = 'chave-secreta'  # Chave necessária para usar sessões

# Rota inicial
@app.route('/')
def index():
    return render_template('index.html')

# Rota para resultados
@app.route('/resultados', methods=['POST', 'GET'])
def resultados():
    if 'usuario' not in session:  # Verifica se o usuário está logado
        return redirect(url_for('login'))

    # Inicializa o espaço de resultados na sessão se não existir
    if 'resultados' not in session:
        session['resultados'] = []

    if request.method == 'POST':
        tempo = request.form['tempo']
        distancia = request.form['distancia']

        # Adiciona apenas se não existir a mesma combinação
        novo_resultado = {'tempo': tempo, 'distancia': distancia}
        if novo_resultado not in session['resultados']:
            session['resultados'].append(novo_resultado)
            session.modified = True  # Indica que a sessão foi alterada

    return render_template('resultados.html', result=session['resultados'])

# Rota para login
@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        nome = request.form['nome']
        session['usuario'] = nome  # Salva o usuário na sessão
        session['resultados'] = []  # Inicializa resultados do usuário
        return redirect(url_for('resultados'))
    return render_template('login.html')

# Rota para logout
@app.route('/logout')
def logout():
    session.clear()  # Limpa a sessão
    return redirect(url_for('login'))


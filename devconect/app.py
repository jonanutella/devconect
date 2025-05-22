from flask import Flask, render_template, request, redirect, url_for, flash, session
import json
import os

app = Flask(__name__)
app.secret_key = 'devconect_secret_key'

# Caminho do arquivo JSON
USER_DATA_FILE = 'users.json'

# Garante que o arquivo JSON exista
def init_user_data():
    if not os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, 'w') as f:
            json.dump({}, f)

# Carrega dados dos usuários
def load_users():
    with open(USER_DATA_FILE, 'r') as f:
        return json.load(f)

# Salva dados dos usuários
def save_users(users):
    with open(USER_DATA_FILE, 'w') as f:
        json.dump(users, f, indent=4)

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']

        users = load_users()
        if email in users and users[email]['senha'] == senha:
            session['user'] = email
            return redirect(url_for('cursos'))
        else:
            flash('Email ou senha incorretos.')

    return render_template('login.html')

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']
        confirmar = request.form['confirmar']

        if senha != confirmar:
            flash('As senhas não coincidem.')
            return render_template('cadastro.html')

        users = load_users()
        if email in users:
            flash('Usuário já cadastrado.')
        else:
            users[email] = {'nome': nome, 'senha': senha}
            save_users(users)
            flash('Cadastro realizado com sucesso!')
            return redirect(url_for('login'))

    return render_template('cadastro.html')

@app.route('/cursos')
def cursos():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('cursos.html')

@app.route('/softskills')
def softskills():
    return render_template('softskills.html')

@app.route('/desenvolvimento')
def desenvolvimento():
    return render_template('desenvolvimento.html')

@app.route('/materia/<area>/<nome>')
def materia(area, nome):
    conteudos = {
        'softskills': {
            'gestao_de_tempo': 'Material sobre Gestão de Tempo: Técnicas como Pomodoro, listas de tarefas e priorização.',
            'trabalho_em_equipe': 'Material sobre Trabalho em Equipe: Comunicação, colaboração e divisão de tarefas.',
            'comunicacao_eficaz': 'Material sobre Comunicação Eficaz: Escuta ativa, feedbacks e clareza na fala.'
        },
        'desenvolvimento': {
            'bancos_de_dados': 'Material sobre Bancos de Dados: Conceitos de SQL, tabelas, relacionamentos e CRUD.',
            'apis': 'Material sobre APIs: O que são, como funcionam, exemplos com Flask e consumo via requests.',
            'frameworks': 'Material sobre Frameworks: Introdução a Flask, Django e estrutura de aplicações.'
        }
    }
    area_data = conteudos.get(area, {})
    texto = area_data.get(nome, 'Conteúdo não encontrado.')
    return render_template('materia.html', titulo=nome.replace('_', ' ').title(), conteudo=texto)

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    init_user_data()
    app.run(debug=True)

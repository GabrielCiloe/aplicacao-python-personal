from flask import Flask, render_template, request, redirect, url_for, send_file, flash
from lib.aluno import cadastrar_aluno, carregar_alunos, remover_aluno, atualizar_aluno
from lib.exercicio import (
    adicionar_exercicio, carregar_exercicios, buscar_exercicio,
    atualizar_exercicio, remover_exercicio, buscar_exercicios_por_grupo, obter_grupos_musculares
)
from lib.treino import (
    criar_treino, listar_treinos, buscar_treino, atualizar_dados_treino,
    remover_treino, gerar_relatorio_treino
)
import os

app = Flask(__name__)
app.secret_key = 'chave_secreta' 

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/alunos')
def alunos():
    alunos = carregar_alunos()
    return render_template('alunos.html', alunos=alunos)

@app.route('/aluno/adicionar', methods=['GET', 'POST'])
def adicionar_aluno():
    if request.method == 'POST':
        nome = request.form['nome']
        idade = int(request.form['idade'])
        peso = float(request.form['peso'])
        altura = float(request.form['altura'])
        sexo = request.form['sexo']
        cadastrar_aluno(nome, idade, peso, altura, sexo)
        flash("Aluno cadastrado com sucesso!")
        return redirect(url_for('alunos'))
    return render_template('adicionar_aluno.html')

@app.route('/aluno/editar/<nome>', methods=['GET', 'POST'])
def editar_aluno(nome):
    alunos = carregar_alunos()
    aluno = next((a for a in alunos if a['nome'].lower() == nome.lower()), None)
    if not aluno:
        flash("Aluno não encontrado.")
        return redirect(url_for('alunos'))
    
    if request.method == 'POST':
        novo_nome = request.form['nome']
        idade = int(request.form['idade'])
        peso = float(request.form['peso'])
        altura = float(request.form['altura'])
        sexo = request.form['sexo']
        atualizar_aluno(nome, novo_nome, idade, peso, altura, sexo)
        flash("Aluno atualizado com sucesso!")
        return redirect(url_for('alunos'))
    return render_template('editar_aluno.html', aluno=aluno)

@app.route('/aluno/remover/<nome>', methods=['POST'])
def remover_aluno_route(nome):
    remover_aluno(nome)
    flash("Aluno removido com sucesso!")
    return redirect(url_for('alunos'))

@app.route('/exercicios', methods=['GET', 'POST'])
def exercicios():
    grupos_musculares = obter_grupos_musculares()
    if request.method == 'POST':
        grupo_muscular = request.form['grupo_muscular']
        if grupo_muscular:
            exercicios = buscar_exercicios_por_grupo(grupo_muscular)
        else:
            exercicios = carregar_exercicios()
    else:
        exercicios = carregar_exercicios()
    return render_template('exercicios.html', exercicios=exercicios, grupos_musculares=grupos_musculares)

@app.route('/exercicio/adicionar', methods=['GET', 'POST'])
def adicionar_exercicio_route():
    if request.method == 'POST':
        nome = request.form['nome']
        grupo_muscular = request.form['grupo_muscular']
        repeticoes = request.form['repeticoes']
        intervalos = request.form['intervalos']
        adicionar_exercicio(nome, grupo_muscular, repeticoes, intervalos)
        flash("Exercício adicionado com sucesso!")
        return redirect(url_for('exercicios'))
    return render_template('adicionar_exercicio.html')

@app.route('/exercicio/buscar', methods=['POST'])
def buscar_exercicio_route():
    nome = request.form['nome']
    exercicio = buscar_exercicio(nome)
    return render_template('exercicio_busca.html', exercicio=exercicio)

@app.route('/exercicio/atualizar/<nome>', methods=['GET', 'POST'])
def atualizar_exercicio_route(nome):
    exercicio = buscar_exercicio(nome)
    if not exercicio:
        flash("Exercício não encontrado.")
        return redirect(url_for('exercicios'))
    
    if request.method == 'POST':
        novo_nome = request.form['nome']
        grupo_muscular = request.form['grupo_muscular']
        repeticoes = request.form['repeticoes']
        intervalos = request.form['intervalos']
        atualizar_exercicio(nome, novo_nome, grupo_muscular, repeticoes, intervalos)
        flash("Exercício atualizado com sucesso!")
        return redirect(url_for('exercicios'))
    return render_template('atualizar_exercicio.html', exercicio=exercicio)

@app.route('/exercicio/remover/<nome>', methods=['POST'])
def remover_exercicio_route(nome):
    remover_exercicio(nome)
    flash("Exercício removido com sucesso!")
    return redirect(url_for('exercicios'))

@app.route('/treinos')
def treinos():
    treinos = listar_treinos()
    return render_template('treinos.html', treinos=treinos)

@app.route('/treino/adicionar', methods=['GET', 'POST'])
def adicionar_treino():
    if request.method == 'POST':
        nome_treino = request.form['nome']
        aluno_nome = request.form['aluno']
        exercicios_selecionados = []
        exercicios = request.form.getlist('exercicios')
        repeticoes = request.form.getlist('repeticoes')
        intervalos = request.form.getlist('intervalos')
        
        if not exercicios or not repeticoes or not intervalos:
            flash("Por favor, preencha todos os campos.")
            return redirect(url_for('adicionar_treino'))

        for i, ex_nome in enumerate(exercicios):
            exercicio = buscar_exercicio(ex_nome)
            if exercicio:
                exercicios_selecionados.append({
                    "nome": exercicio['nome'],
                    "grupo_muscular": exercicio['grupo_muscular'],
                    "repeticoes": repeticoes[i],
                    "intervalos": intervalos[i]
                })
                
        criar_treino(nome_treino, exercicios=exercicios_selecionados, aluno_nome=aluno_nome)
        flash("Treino criado com sucesso!")
        return redirect(url_for('treinos'))
    
    alunos = carregar_alunos()
    exercicios = carregar_exercicios()
    grupos_musculares = obter_grupos_musculares()
    return render_template('adicionar_treino.html', exercicios=exercicios, alunos=alunos, grupos_musculares=grupos_musculares)

@app.route('/treino/buscar', methods=['POST'])
def buscar_treino_route():
    nome = request.form['nome']
    treino = next((t for t in listar_treinos() if t['aluno_nome'].lower() == nome.lower()), None)
    if treino is None:
        flash("Treino não encontrado.")
        return redirect(url_for('treinos'))
    return render_template('treino_busca.html', treino=treino)

@app.route('/treino/atualizar/<nome>', methods=['GET', 'POST'])
def atualizar_treino(nome):
    treino = buscar_treino(nome)
    if not treino:
        flash("Treino não encontrado.")
        return redirect(url_for('treinos'))
    
    if request.method == 'POST':
        novo_nome = request.form['nome']
        aluno_nome = request.form['aluno']
        exercicios_selecionados = []
        exercicios = request.form.getlist('exercicios')
        repeticoes = request.form.getlist('repeticoes')
        intervalos = request.form.getlist('intervalos')

        for i, ex_nome in enumerate(exercicios):
            exercicio = buscar_exercicio(ex_nome)
            if exercicio:
                exercicios_selecionados.append({
                    "nome": exercicio['nome'],
                    "grupo_muscular": exercicio['grupo_muscular'],
                    "repeticoes": repeticoes[i],
                    "intervalos": intervalos[i]
                })
        
        atualizar_dados_treino(nome, novo_nome, exercicios=exercicios_selecionados, aluno_nome=aluno_nome)
        flash("Treino atualizado com sucesso!")
        return redirect(url_for('treinos'))
    
    alunos = carregar_alunos()
    exercicios = carregar_exercicios()
    grupos_musculares = obter_grupos_musculares()
    return render_template('atualizar_treino.html', treino=treino, alunos=alunos, exercicios=exercicios, grupos_musculares=grupos_musculares)

@app.route('/treino/remover/<nome>', methods=['POST'])
def remover_treino_route(nome):
    remover_treino(nome)
    flash("Treino removido com sucesso!")
    return redirect(url_for('treinos'))

@app.route('/treino/relatorio/<nome>')
def gerar_relatorio_treino_route(nome):
    file_path = gerar_relatorio_treino(nome)
    if file_path and os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    else:
        flash("Relatório não encontrado.")
        return redirect(url_for('treinos'))

if __name__ == '__main__':
    app.run(debug=True)

import json
import os
from fpdf import FPDF

DATAPATH = "database/treinos.json"

def listar_treinos():
    try:
        with open(DATAPATH, 'r', encoding='utf-8') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def salvar_treinos(treinos):
    os.makedirs(os.path.dirname(DATAPATH), exist_ok=True)
    with open(DATAPATH, 'w', encoding='utf-8') as file:
        json.dump(treinos, file, ensure_ascii=False, indent=4)

def criar_treino(nome, exercicios, aluno_nome=None):
    treino = {
        "nome": nome,
        "exercicios": exercicios,
        "aluno_nome": aluno_nome  
    }
    treinos = listar_treinos()
    treinos.append(treino)
    salvar_treinos(treinos)

def buscar_treino(nome):
    treinos = listar_treinos()
    for treino in treinos:
        if treino['nome'].lower() == nome.lower():
            return treino
    return None
def atualizar_dados_treino(nome_original, novo_nome, exercicios, aluno_nome):
    treinos = listar_treinos()
    for treino in treinos:
        if treino['nome'].lower() == nome_original.lower():
            treino['nome'] = novo_nome
            treino['exercicios'] = exercicios
            treino['aluno_nome'] = aluno_nome 
            break
    salvar_treinos(treinos)

def remover_treino(nome):
    treinos = listar_treinos()
    treinos = [tr for tr in treinos if tr['nome'].lower() != nome.lower()]
    salvar_treinos(treinos)

def gerar_relatorio_treino(nome):
    treino = buscar_treino(nome)
    if not treino:
        return None

    aluno_nome = treino.get("aluno_nome", "Aluno não associado")
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"Relatório do Treino: {nome}", ln=True, align='C')
    pdf.cell(200, 10, txt=f"Aluno: {aluno_nome}", ln=True, align='C')  
    pdf.ln(10)

    for ex in treino['exercicios']:
        exercicio_nome = ex['nome']
        grupo_muscular = ex.get('grupo_muscular', 'N/A')
        repeticoes = ex.get('repeticoes', 'N/A')
        intervalos = ex.get('intervalos', 'N/A')
        pdf.cell(0, 10, f"Exercício: {exercicio_nome}, Grupo: {grupo_muscular}, Repetições: {repeticoes}, Intervalos: {intervalos}", ln=True)

    file_path = f"database/relatorio_treino_{nome}.pdf"
    pdf.output(file_path)
    return file_path

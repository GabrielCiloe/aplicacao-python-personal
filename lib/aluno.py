import json
import os
from .treino import buscar_treino

DATAPATH = "database/alunos.json"

def calcular_imc(peso, altura):
    if altura <= 0:
        return 0
    return peso / (altura ** 2)

def classificar_imc(imc):
    if imc < 18.5:
        return "Abaixo do peso"
    elif 18.5 <= imc < 24.9:
        return "Peso normal"
    elif 25 <= imc < 29.9:
        return "Sobrepeso"
    else:
        return "Obesidade"

def cadastrar_aluno(nome, idade, peso, altura, sexo, treino_nome=None):
    imc = calcular_imc(peso, altura)
    classificacao = classificar_imc(imc)
    treino = buscar_treino(treino_nome) if treino_nome else None
    aluno = {
        "nome": nome,
        "idade": idade,
        "sexo": sexo,
        "peso": peso,
        "altura": altura,
        "imc": round(imc, 2),
        "classificacao": classificacao,
        "treino": treino
    }
    salvar_aluno(aluno)

def salvar_aluno(aluno):
    os.makedirs(os.path.dirname(DATAPATH), exist_ok=True)
    alunos = carregar_alunos()
    alunos.append(aluno)
    with open(DATAPATH, 'w', encoding='utf-8') as file:
        json.dump(alunos, file, ensure_ascii=False, indent=4)

def carregar_alunos():
    try:
        with open(DATAPATH, 'r', encoding='utf-8') as file:
            alunos = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        alunos = []
    return alunos

def listar_alunos():
    return carregar_alunos()

def buscar_exercicio(nome):
    alunos = carregar_alunos()
    for aluno in alunos:
        if aluno['nome'].lower() == nome.lower():
            return aluno
    return None

def remover_aluno(nome):
    alunos = carregar_alunos()
    alunos = [aluno for aluno in alunos if aluno['nome'].lower() != nome.lower()]
    salvar_alunos(alunos)

def salvar_alunos(alunos):
    os.makedirs(os.path.dirname(DATAPATH), exist_ok=True)
    with open(DATAPATH, 'w', encoding='utf-8') as file:
        json.dump(alunos, file, ensure_ascii=False, indent=4)

def atualizar_aluno(nome_original, novo_nome, idade, peso, altura, sexo, treino_nome=None):
    alunos = carregar_alunos()
    for aluno in alunos:
        if aluno['nome'].lower() == nome_original.lower():
            aluno['nome'] = novo_nome
            aluno['idade'] = idade
            aluno['peso'] = peso
            aluno['altura'] = altura
            aluno['sexo'] = sexo
            aluno['imc'] = round(calcular_imc(peso, altura), 2)
            aluno['classificacao'] = classificar_imc(aluno['imc'])
            aluno['treino'] = buscar_treino(treino_nome) if treino_nome else None
            break
    salvar_alunos(alunos)
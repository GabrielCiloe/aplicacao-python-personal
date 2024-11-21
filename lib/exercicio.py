import json
import os

DATAPATH = "database/exercicios.json"

def adicionar_exercicio(nome, grupo_muscular, repeticoes, intervalos):
    exercicio = {
        "nome": nome,
        "grupo_muscular": grupo_muscular,
        "repeticoes": repeticoes,
        "intervalos": intervalos
    }
    exercicios = carregar_exercicios()
    exercicios.append(exercicio)
    salvar_exercicios(exercicios)

def salvar_exercicios(exercicios):
    os.makedirs(os.path.dirname(DATAPATH), exist_ok=True)
    with open(DATAPATH, 'w', encoding='utf-8') as file:
        json.dump(exercicios, file, ensure_ascii=False, indent=4)

def carregar_exercicios():
    try:
        with open(DATAPATH, 'r', encoding='utf-8') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def buscar_exercicio(nome):
    exercicios = carregar_exercicios()
    for exercicio in exercicios:
        if exercicio['nome'].lower() == nome.lower():
            return exercicio
    return None

def atualizar_exercicio(nome_original, novo_nome, grupo_muscular, repeticoes, intervalos):
    exercicios = carregar_exercicios()
    for exercicio in exercicios:
        if exercicio['nome'].lower() == nome_original.lower():
            exercicio['nome'] = novo_nome
            exercicio['grupo_muscular'] = grupo_muscular
            exercicio['repeticoes'] = repeticoes
            exercicio['intervalos'] = intervalos
            break
    salvar_exercicios(exercicios)

def remover_exercicio(nome):
    exercicios = carregar_exercicios()
    exercicios = [ex for ex in exercicios if ex['nome'].lower() != nome.lower()]
    salvar_exercicios(exercicios)

def buscar_exercicios_por_grupo(grupo_muscular):
    exercicios = carregar_exercicios()
    return [ex for ex in exercicios if ex['grupo_muscular'].lower() == grupo_muscular.lower()]

def obter_grupos_musculares():
    exercicios = carregar_exercicios()
    return sorted(list(set(ex['grupo_muscular'] for ex in exercicios)))
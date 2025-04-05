from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

import random
import json
import os

app = FastAPI()

#MODELO DO PROFESSOR
#  http://127.0.0.1:8000/
@app.get("/helloworld")
async def root():
    return {"message": "Hello World"}

#  http://127.0.0.1:8000/teste1

@app.get("/funcaoteste")
async def funcaoteste():
    return {"teste": True, "num_aleatório: ": random.randint(0, 1000)}
#=====================================================

DB_PATH = "lancamentos_despesas_receitas.json"

# Carregar os dados do arquivo JSON ou criar novo
if os.path.exists(DB_PATH):
    with open(DB_PATH, "r", encoding="utf-8") as f:
        lancamentos = json.load(f)
else:
    lancamentos = []


#  http://127.0.0.1:8000/lancamentos
@app.get("/lancamentos")
def listar_lancamentos():
    return lancamentos

#  http://127.0.0.1:8000/lancamentos/{id}
@app.get("/lancamentos/{id}")
def buscar_por_id(id: int):
    for item in lancamentos:
        if item["id"] == id:
            return item
    raise HTTPException(status_code=404, detail="Lançamento não encontrado")

#  http://127.0.0.1:8000/lancamentos/tipo/{tipo}
@app.get("/lancamentos/tipo/{tipo}")
def filtrar_por_tipo(tipo: str):
    tipo = tipo.lower()
    if tipo not in ["despesa", "receita"]:
        raise HTTPException(status_code=400, detail="Tipo deve ser 'despesa' ou 'receita'")
    return [l for l in lancamentos if l["tipo"] == tipo]

#  http://127.0.0.1:8000/lancamentos/categoria/{categoria}
@app.get("/lancamentos/categoria/{categoria}")
def filtrar_por_categoria(categoria: str):
    return [l for l in lancamentos if l["categoria"].lower() == categoria.lower()]

#  http://127.0.0.1:8000/resumo
@app.get("/resumo")
def resumo():
    total_despesas = sum(l["valor"] for l in lancamentos if l["tipo"] == "despesa")
    total_receitas = sum(l["valor"] for l in lancamentos if l["tipo"] == "receita")
    saldo = total_receitas - total_despesas
    return {
        "total_despesas": round(total_despesas, 2),
        "total_receitas": round(total_receitas, 2),
        "saldo": round(saldo, 2)
    }


#Testando um metodo POST
# Modelo para criação de novos lançamentos
class LancamentoInput(BaseModel):
    tipo: str  # 'despesa' ou 'receita'
    data: str  # formato 'YYYY-MM-DD'
    categoria: str
    descricao: str
    valor: float
    forma_pagamento: Optional[str] = None
    forma_recebimento: Optional[str] = None
    efetivado: bool


# Função auxiliar para salvar no JSON
def salvar_dados():
    with open(DB_PATH, "w", encoding="utf-8") as f:
        json.dump(lancamentos, f, indent=4, ensure_ascii=False)


@app.post("/lancamentos")
def criar_lancamento(dados: LancamentoInput):
    novo_id = max([l["id"] for l in lancamentos], default=0) + 1

    novo_lancamento = {
        "id": novo_id,
        **dados.dict()
    }

    lancamentos.append(novo_lancamento)
    salvar_dados()
    return {"mensagem": "Lançamento criado com sucesso!", "lancamento": novo_lancamento}
import random
import json

from fastapi import FastAPI

app = FastAPI()

#  http://127.0.0.1:8000/
@app.get("/")
async def root():
    return {"message": "Hello World"}

#  http://127.0.0.1:8000/teste1
@app.get("/teste")
async def funcaoteste():
    return {"teste": True, "num_aleatório: ": random.randint(0, 1000)}

# Carregar os dados do arquivo JSON
with open("lancamentos_despesas_receitas.json", "r", encoding="utf-8") as f:
    lancamentos = json.load(f)


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

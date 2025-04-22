import pytest
from fastapi import HTTPException

from src.main import *

# Carregar os dados do arquivo JSON ou criar novo
if os.path.exists(DB_PATH):
    with open(DB_PATH, "r", encoding="utf-8") as f:
        lancamentos = json.load(f)
else:
    lancamentos = []


def test_listar_lancamentos():
    resultado = listar_lancamentos()
    assert isinstance(resultado, list) #verifica se o retorno é mesmo uma lista
    assert len(resultado) > 0 #verifica se está retornando algo


def test_buscar_por_id_existente():
    resultado = buscar_por_id(1)
    assert resultado["id"] == 1
    assert "tipo" in resultado
    assert "valor" in resultado


def test_buscar_por_id_inexistente():
    with pytest.raises(HTTPException) as exc_info:
        buscar_por_id(999)  # id que não existe

        # Verifica se a exceção retorn o código correto
        assert exc_info.value.status_code == 404
        assert exc_info.value.detail == "Lançamento não encontrado"


def test_filtrar_por_tipo_receita():
    resultado = filtrar_por_tipo("receita")
    assert isinstance(resultado, list) # Verifica se o retorno é uma lista
    assert all(l["tipo"] == "receita" for l in resultado)  # Se houver algum resultado, verifique se todos são do tipo 'receita'


def test_filtrar_por_tipo_despesa():
    resultado = filtrar_por_tipo("despesa")
    assert isinstance(resultado, list)
    assert all(l["tipo"] == "despesa" for l in resultado)


def test_filtrar_por_tipo_invalido():
    with pytest.raises(HTTPException) as exc_info:
        filtrar_por_tipo("investimento")  # tipo inválido

    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "Tipo deve ser 'despesa' ou 'receita'"


def test_filtrar_categoria():
    resultado = filtrar_por_categoria("Transporte")
    assert all(l["categoria"].lower() == "transporte" for l in resultado)


def test_resumo():
    resultado = resumo()

    # Verifica se é um dicionário
    assert isinstance(resultado, dict)

    # Verifica se as chaves esperadas estão presentes
    assert "total_despesas" in resultado
    assert "total_receitas" in resultado
    assert "saldo" in resultado

"""
FUNÇÕES NÃO TESTADAS:

# Função auxiliar para salvar no JSON
def salvar_dados():
    with open(DB_PATH, "w", encoding="utf-8") as f:
        json.dump(lancamentos, f, indent=4, ensure_ascii=False)


def criar_lancamento(dados: LancamentoInput):
    novo_id = max([l["id"] for l in lancamentos], default=0) + 1

    novo_lancamento = {
        "id": novo_id,
        **dados.dict()
    }

    lancamentos.append(novo_lancamento)
    salvar_dados()
    return {"mensagem": "Lançamento criado com sucesso!", "lancamento": novo_lancamento}

class LancamentoInput(BaseModel):
    tipo: str  # 'despesa' ou 'receita'
    data: str  # formato 'YYYY-MM-DD'
    categoria: str
    descricao: str
    valor: float
    forma_pagamento: Optional[str] = None
    forma_recebimento: Optional[str] = None
    efetivado: bool

"""
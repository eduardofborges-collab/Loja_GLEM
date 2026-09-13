import json

from pydantic import BaseModel
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


# =====================================================
# FASTAPI
# =====================================================

app = FastAPI()


# =====================================================
# CORS
# =====================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =====================================================
# GET - LISTAR PRODUTOS
# =====================================================

@app.get("/produtos")
def listar_produtos(categoria: str | None = None):

    with open(
        "database/produtos.json",
        "r",
        encoding="utf-8"
    ) as arquivo:

        dados = json.load(arquivo)


    produtos = dados["Produtos"]


    # =================================================
    # FILTRO POR CATEGORIA
    # =================================================

    if categoria:

        produtos = [
            produto
            for produto in produtos
            if produto.get("categoria", "").lower()
            == categoria.lower()
        ]


    return produtos


# =====================================================
# MODELO DO PRODUTO
# =====================================================

class Produto(BaseModel):

    id: int
    preco: float


# =====================================================
# MODELO DO PEDIDO
# =====================================================

class ItemPedido(BaseModel):

    produtos: list[Produto]


# =====================================================
# POST - CRIAR PEDIDO
# =====================================================

@app.post("/pedidos")
def criar_pedido(dados: ItemPedido):

    # =================================================
    # ABRIR BANCO DE PEDIDOS
    # =================================================

    with open(
        "database/pedidos.json",
        "r",
        encoding="utf-8"
    ) as arquivo:

        banco = json.load(arquivo)


    pedidos = banco["Pedidos"]


    # =================================================
    # CRIAR ID
    # =================================================

    novo_id = len(pedidos) + 1


    # =================================================
    # CALCULAR TOTAL
    # =================================================

    total = 0.0


    for item in dados.produtos:

        total += item.preco


    # =================================================
    # CRIAR PEDIDO
    # =================================================

    novo_pedido = {

        "id": novo_id,

        "produtos": [

            {
                "id": item.id,
                "preco": item.preco
            }

            for item in dados.produtos

        ],

        "total": total,

        "status": "pendente"

    }


    # =================================================
    # ADICIONAR PEDIDO
    # =================================================

    pedidos.append(novo_pedido)


    # =================================================
    # SALVAR JSON
    # =================================================

    with open(
        "database/pedidos.json",
        "w",
        encoding="utf-8"
    ) as arquivo:

        json.dump(
            banco,
            arquivo,
            indent=4,
            ensure_ascii=False
        )


    return novo_pedido


@app.post("/pedidos")
def criar_pedidos(dados: ItemPedido):

    # Abre o arquivo de pedidos
    with open("database/pedidos.json", "r", encoding="utf-8") as arquivo:
        banco = json.load(arquivo)

    pedidos = banco["Pedidos"]

    # Cria o ID
    novo_id = len(pedidos) + 1

    # Calcula o total
    total = 0.0

    for item in dados.produtos:
        total += item.preco

    # Cria o pedido depois do FOR
    novo_pedido = {
        "id": novo_id,
        "produtos": [
            {
                "id": item.id,
                "preco": item.preco
            }
            for item in dados.produtos
        ],
        "total": total,
        "status": "pendente"
    }

    # Adiciona o pedido à lista
    pedidos.append(novo_pedido)

    # Salva no JSON
    with open("database/pedidos.json", "w", encoding="utf-8") as arquivo:
        json.dump(
            banco,
            arquivo,
            indent=4,
            ensure_ascii=False
        )

    return novo_pedido

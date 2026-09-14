import json

from pydantic import BaseModel
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/produtos")
def listar_produtos(categoria: str | None = None):

    with open(
        "database/produtos.json",
        "r",
        encoding="utf-8"
    ) as arquivo:

        dados = json.load(arquivo)


    produtos = dados["Produtos"]

    if categoria:

        produtos = [
            produto
            for produto in produtos
            if produto.get("categoria", "").lower()
            == categoria.lower()
        ]


    return produtos

class Produto(BaseModel):

    id: int
    preco: float

class ItemPedido(BaseModel):

    produtos: list[Produto]

@app.post("/pedidos")
def criar_pedido(dados: ItemPedido):

    with open(
        "database/pedidos.json",
        "r",
        encoding="utf-8"
    ) as arquivo:

        banco = json.load(arquivo)


    pedidos = banco["Pedidos"]

    novo_id = len(pedidos) + 1

    total = 0.0


    for item in dados.produtos:

        total += item.preco

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

    pedidos.append(novo_pedido)

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

    with open("database/pedidos.json", "r", encoding="utf-8") as arquivo:
        banco = json.load(arquivo)

    pedidos = banco["Pedidos"]

    novo_id = len(pedidos) + 1

    total = 0.0

    for item in dados.produtos:
        total += item.preco

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

    pedidos.append(novo_pedido)

    with open("database/pedidos.json", "w", encoding="utf-8") as arquivo:
        json.dump(
            banco,
            arquivo,
            indent=4,
            ensure_ascii=False
        )

    return novo_pedido

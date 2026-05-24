from flask import jsonify, request

from src.repositories.product_repository import ProductRepository
from src.services.product_service import ProductService


product_service = ProductService(ProductRepository())


def listar_produtos():
    return jsonify({"dados": product_service.list_products(), "sucesso": True}), 200


def buscar_produto(product_id):
    return jsonify({"dados": product_service.get_product(product_id), "sucesso": True}), 200


def criar_produto():
    resultado = product_service.create_product(request.get_json())
    return jsonify({"dados": resultado, "sucesso": True, "mensagem": "Produto criado"}), 201


def atualizar_produto(product_id):
    product_service.update_product(product_id, request.get_json())
    return jsonify({"sucesso": True, "mensagem": "Produto atualizado"}), 200


def deletar_produto(product_id):
    product_service.delete_product(product_id)
    return jsonify({"sucesso": True, "mensagem": "Produto deletado"}), 200


def buscar_produtos():
    termo = request.args.get("q", "")
    categoria = request.args.get("categoria")
    preco_min = request.args.get("preco_min")
    preco_max = request.args.get("preco_max")
    produtos = product_service.search_products(
        termo,
        categoria,
        float(preco_min) if preco_min else None,
        float(preco_max) if preco_max else None,
    )
    return jsonify({"dados": produtos, "total": len(produtos), "sucesso": True}), 200

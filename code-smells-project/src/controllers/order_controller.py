from flask import jsonify, request

from src.repositories.order_repository import OrderRepository
from src.repositories.product_repository import ProductRepository
from src.repositories.user_repository import UserRepository
from src.services.order_service import OrderService


order_service = OrderService(OrderRepository(), ProductRepository(), UserRepository())


def criar_pedido():
    resultado = order_service.create_order(request.get_json())
    return jsonify({"dados": resultado, "sucesso": True, "mensagem": "Pedido criado com sucesso"}), 201


def listar_todos_pedidos():
    return jsonify({"dados": order_service.list_orders(), "sucesso": True}), 200


def listar_pedidos_usuario(usuario_id):
    return jsonify({"dados": order_service.list_user_orders(usuario_id), "sucesso": True}), 200


def atualizar_status_pedido(pedido_id):
    payload = request.get_json() or {}
    order_service.update_status(pedido_id, payload.get("status", ""))
    return jsonify({"sucesso": True, "mensagem": "Status atualizado"}), 200


def relatorio_vendas():
    return jsonify({"dados": order_service.sales_report(), "sucesso": True}), 200

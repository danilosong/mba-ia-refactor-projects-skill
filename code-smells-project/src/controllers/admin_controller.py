from flask import jsonify, request

from src.services.admin_service import AdminService


admin_service = AdminService()


def health_check():
    return jsonify(admin_service.health()), 200


def reset_database():
    return jsonify(admin_service.reset_database()), 200


def executar_query():
    body, status = admin_service.safe_query(request.get_json())
    return jsonify(body), status


def index():
    return jsonify(
        {
            "mensagem": "Bem-vindo a API da Loja",
            "versao": "2.0.0",
            "endpoints": {
                "produtos": "/produtos",
                "usuarios": "/usuarios",
                "pedidos": "/pedidos",
                "login": "/login",
                "relatorios": "/relatorios/vendas",
                "health": "/health",
            },
        }
    )

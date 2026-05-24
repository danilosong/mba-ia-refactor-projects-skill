from flask import jsonify, request

from src.repositories.user_repository import UserRepository
from src.services.user_service import UserService


user_service = UserService(UserRepository())


def listar_usuarios():
    return jsonify({"dados": user_service.list_users(), "sucesso": True}), 200


def buscar_usuario(user_id):
    return jsonify({"dados": user_service.get_user(user_id), "sucesso": True}), 200


def criar_usuario():
    resultado = user_service.create_user(request.get_json())
    return jsonify({"dados": resultado, "sucesso": True}), 201


def login():
    usuario = user_service.login(request.get_json())
    return jsonify({"dados": usuario, "sucesso": True, "mensagem": "Login OK"}), 200

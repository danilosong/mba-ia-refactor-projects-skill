from flask import jsonify

from src.errors import AppError


def register_error_handlers(app):
    @app.errorhandler(AppError)
    def handle_app_error(error):
        return jsonify({"erro": error.message, "sucesso": False}), error.status_code

    @app.errorhandler(Exception)
    def handle_unexpected_error(error):
        return jsonify({"erro": "Erro interno do servidor", "sucesso": False}), 500

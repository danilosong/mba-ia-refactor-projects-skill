from flask import Blueprint

from src.controllers import admin_controller, order_controller, product_controller, user_controller


bp = Blueprint("store", __name__)

bp.add_url_rule("/", "index", admin_controller.index, methods=["GET"])
bp.add_url_rule("/health", "health_check", admin_controller.health_check, methods=["GET"])
bp.add_url_rule("/admin/reset-db", "reset_database", admin_controller.reset_database, methods=["POST"])
bp.add_url_rule("/admin/query", "executar_query", admin_controller.executar_query, methods=["POST"])

bp.add_url_rule("/produtos", "listar_produtos", product_controller.listar_produtos, methods=["GET"])
bp.add_url_rule("/produtos/busca", "buscar_produtos", product_controller.buscar_produtos, methods=["GET"])
bp.add_url_rule("/produtos/<int:product_id>", "buscar_produto", product_controller.buscar_produto, methods=["GET"])
bp.add_url_rule("/produtos", "criar_produto", product_controller.criar_produto, methods=["POST"])
bp.add_url_rule("/produtos/<int:product_id>", "atualizar_produto", product_controller.atualizar_produto, methods=["PUT"])
bp.add_url_rule("/produtos/<int:product_id>", "deletar_produto", product_controller.deletar_produto, methods=["DELETE"])

bp.add_url_rule("/usuarios", "listar_usuarios", user_controller.listar_usuarios, methods=["GET"])
bp.add_url_rule("/usuarios/<int:user_id>", "buscar_usuario", user_controller.buscar_usuario, methods=["GET"])
bp.add_url_rule("/usuarios", "criar_usuario", user_controller.criar_usuario, methods=["POST"])
bp.add_url_rule("/login", "login", user_controller.login, methods=["POST"])

bp.add_url_rule("/pedidos", "criar_pedido", order_controller.criar_pedido, methods=["POST"])
bp.add_url_rule("/pedidos", "listar_todos_pedidos", order_controller.listar_todos_pedidos, methods=["GET"])
bp.add_url_rule("/pedidos/usuario/<int:usuario_id>", "listar_pedidos_usuario", order_controller.listar_pedidos_usuario, methods=["GET"])
bp.add_url_rule("/pedidos/<int:pedido_id>/status", "atualizar_status_pedido", order_controller.atualizar_status_pedido, methods=["PUT"])
bp.add_url_rule("/relatorios/vendas", "relatorio_vendas", order_controller.relatorio_vendas, methods=["GET"])

from src.repositories.order_repository import OrderRepository
from src.repositories.product_repository import ProductRepository
from src.repositories.user_repository import UserRepository
from src.services.order_service import OrderService


_product_repository = ProductRepository()
_user_repository = UserRepository()
_order_service = OrderService(OrderRepository(), _product_repository, _user_repository)


def get_todos_produtos():
    return _product_repository.list_all()


def get_produto_por_id(product_id):
    return _product_repository.get_by_id(product_id)


def criar_produto(nome, descricao, preco, estoque, categoria):
    return _product_repository.create(nome, descricao, preco, estoque, categoria)


def atualizar_produto(product_id, nome, descricao, preco, estoque, categoria):
    _product_repository.update(product_id, nome, descricao, preco, estoque, categoria)
    return True


def deletar_produto(product_id):
    _product_repository.delete(product_id)
    return True


def get_todos_usuarios():
    return _user_repository.list_all()


def get_usuario_por_id(user_id):
    return _user_repository.get_by_id(user_id)


def login_usuario(email, senha):
    return _user_repository.authenticate(email, senha)


def criar_usuario(nome, email, senha, tipo="cliente"):
    return _user_repository.create(nome, email, senha, tipo)


def criar_pedido(usuario_id, itens):
    return _order_service.create_order({"usuario_id": usuario_id, "itens": itens})


def get_pedidos_usuario(usuario_id):
    return _order_service.list_user_orders(usuario_id)


def get_todos_pedidos():
    return _order_service.list_orders()


def relatorio_vendas():
    return _order_service.sales_report()


def atualizar_status_pedido(pedido_id, novo_status):
    _order_service.update_status(pedido_id, novo_status)
    return True


def buscar_produtos(termo, categoria=None, preco_min=None, preco_max=None):
    return _product_repository.search(termo, categoria, preco_min, preco_max)

from src.controllers.admin_controller import health_check
from src.controllers.order_controller import (
    atualizar_status_pedido,
    criar_pedido,
    listar_pedidos_usuario,
    listar_todos_pedidos,
    relatorio_vendas,
)
from src.controllers.product_controller import (
    atualizar_produto,
    buscar_produto,
    buscar_produtos,
    criar_produto,
    deletar_produto,
    listar_produtos,
)
from src.controllers.user_controller import (
    buscar_usuario,
    criar_usuario,
    listar_usuarios,
    login,
)

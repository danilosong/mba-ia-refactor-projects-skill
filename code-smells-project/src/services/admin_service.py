from src.database.connection import database_metadata, get_db, reset_database
from src.repositories.order_repository import OrderRepository
from src.repositories.product_repository import ProductRepository
from src.repositories.user_repository import UserRepository


class AdminService:
    ALLOWED_TABLES = {"produtos", "usuarios", "pedidos", "itens_pedido"}

    def __init__(self):
        self.product_repository = ProductRepository()
        self.user_repository = UserRepository()
        self.order_repository = OrderRepository()

    def health(self):
        metadata = database_metadata()
        return {
            "status": "ok",
            "database": "connected",
            "counts": {
                "produtos": self.product_repository.count(),
                "usuarios": self.user_repository.count(),
                "pedidos": self.order_repository.count(),
            },
            "versao": "2.0.0",
            "ambiente": "development",
            "db_path": metadata["path"],
        }

    def reset_database(self):
        reset_database()
        return {"mensagem": "Banco de dados resetado", "sucesso": True}

    def safe_query(self, payload):
        sql = (payload or {}).get("sql", "").strip()
        if not sql:
            return {"erro": "Query nao informada"}, 400
        normalized = " ".join(sql.split()).lower()
        if not normalized.startswith("select"):
            return {"erro": "Apenas consultas SELECT sao permitidas"}, 400
        if not any(f" from {table}" in normalized for table in self.ALLOWED_TABLES):
            return {"erro": "Consulta fora das tabelas permitidas"}, 400

        cursor = get_db().cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        return {"dados": [dict(row) for row in rows], "sucesso": True}, 200

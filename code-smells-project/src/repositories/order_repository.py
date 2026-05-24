from src.database.connection import get_db


class OrderRepository:
    def create_order(self, usuario_id, total, items):
        connection = get_db()
        cursor = connection.cursor()
        cursor.execute("BEGIN")
        try:
            cursor.execute(
                "INSERT INTO pedidos (usuario_id, status, total) VALUES (?, 'pendente', ?)",
                (usuario_id, total),
            )
            pedido_id = cursor.lastrowid
            for item in items:
                cursor.execute(
                    """
                    INSERT INTO itens_pedido (pedido_id, produto_id, quantidade, preco_unitario)
                    VALUES (?, ?, ?, ?)
                    """,
                    (
                        pedido_id,
                        item["produto_id"],
                        item["quantidade"],
                        item["preco_unitario"],
                    ),
                )
                cursor.execute(
                    "UPDATE produtos SET estoque = estoque - ? WHERE id = ?",
                    (item["quantidade"], item["produto_id"]),
                )
            connection.commit()
            return pedido_id
        except Exception:
            connection.rollback()
            raise

    def list_all(self):
        cursor = get_db().cursor()
        cursor.execute("SELECT * FROM pedidos ORDER BY id")
        return cursor.fetchall()

    def list_by_user(self, usuario_id):
        cursor = get_db().cursor()
        cursor.execute("SELECT * FROM pedidos WHERE usuario_id = ? ORDER BY id", (usuario_id,))
        return cursor.fetchall()

    def get_items_by_order_ids(self, order_ids):
        if not order_ids:
            return {}
        placeholders = ",".join(["?"] * len(order_ids))
        cursor = get_db().cursor()
        cursor.execute(
            f"SELECT * FROM itens_pedido WHERE pedido_id IN ({placeholders}) ORDER BY pedido_id, id",
            order_ids,
        )
        grouped = {}
        for row in cursor.fetchall():
            grouped.setdefault(row["pedido_id"], []).append(
                {
                    "produto_id": row["produto_id"],
                    "quantidade": row["quantidade"],
                    "preco_unitario": row["preco_unitario"],
                }
            )
        return grouped

    def update_status(self, pedido_id, novo_status):
        connection = get_db()
        cursor = connection.cursor()
        cursor.execute("UPDATE pedidos SET status = ? WHERE id = ?", (novo_status, pedido_id))
        connection.commit()

    def count(self):
        cursor = get_db().cursor()
        cursor.execute("SELECT COUNT(*) FROM pedidos")
        return cursor.fetchone()[0]

    def sales_summary(self):
        cursor = get_db().cursor()
        cursor.execute("SELECT COUNT(*) FROM pedidos")
        total_pedidos = cursor.fetchone()[0]
        cursor.execute("SELECT COALESCE(SUM(total), 0) FROM pedidos")
        faturamento = cursor.fetchone()[0]
        status_counts = {}
        for status in ["pendente", "aprovado", "cancelado"]:
            cursor.execute("SELECT COUNT(*) FROM pedidos WHERE status = ?", (status,))
            status_counts[status] = cursor.fetchone()[0]
        return {
            "total_pedidos": total_pedidos,
            "faturamento_bruto": faturamento,
            "pedidos_pendentes": status_counts["pendente"],
            "pedidos_aprovados": status_counts["aprovado"],
            "pedidos_cancelados": status_counts["cancelado"],
        }

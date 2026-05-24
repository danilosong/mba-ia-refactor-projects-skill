from src.database.connection import get_db


class ProductRepository:
    def list_all(self):
        cursor = get_db().cursor()
        cursor.execute("SELECT * FROM produtos ORDER BY id")
        return [self._to_dict(row) for row in cursor.fetchall()]

    def search(self, termo="", categoria=None, preco_min=None, preco_max=None):
        cursor = get_db().cursor()
        query = ["SELECT * FROM produtos WHERE 1=1"]
        params = []

        if termo:
            query.append("AND (nome LIKE ? OR descricao LIKE ?)")
            like = f"%{termo}%"
            params.extend([like, like])
        if categoria:
            query.append("AND categoria = ?")
            params.append(categoria)
        if preco_min is not None:
            query.append("AND preco >= ?")
            params.append(preco_min)
        if preco_max is not None:
            query.append("AND preco <= ?")
            params.append(preco_max)

        cursor.execute(" ".join(query), params)
        return [self._to_dict(row) for row in cursor.fetchall()]

    def get_by_id(self, product_id):
        cursor = get_db().cursor()
        cursor.execute("SELECT * FROM produtos WHERE id = ?", (product_id,))
        row = cursor.fetchone()
        return self._to_dict(row) if row else None

    def get_by_ids(self, product_ids):
        if not product_ids:
            return {}
        placeholders = ",".join(["?"] * len(product_ids))
        cursor = get_db().cursor()
        cursor.execute(f"SELECT * FROM produtos WHERE id IN ({placeholders})", product_ids)
        return {row["id"]: self._to_dict(row) for row in cursor.fetchall()}

    def create(self, nome, descricao, preco, estoque, categoria):
        connection = get_db()
        cursor = connection.cursor()
        cursor.execute(
            """
            INSERT INTO produtos (nome, descricao, preco, estoque, categoria)
            VALUES (?, ?, ?, ?, ?)
            """,
            (nome, descricao, preco, estoque, categoria),
        )
        connection.commit()
        return cursor.lastrowid

    def update(self, product_id, nome, descricao, preco, estoque, categoria):
        connection = get_db()
        cursor = connection.cursor()
        cursor.execute(
            """
            UPDATE produtos
            SET nome = ?, descricao = ?, preco = ?, estoque = ?, categoria = ?
            WHERE id = ?
            """,
            (nome, descricao, preco, estoque, categoria, product_id),
        )
        connection.commit()

    def delete(self, product_id):
        connection = get_db()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM produtos WHERE id = ?", (product_id,))
        connection.commit()

    def decrement_stock(self, product_id, quantidade, cursor):
        cursor.execute(
            "UPDATE produtos SET estoque = estoque - ? WHERE id = ?",
            (quantidade, product_id),
        )

    def count(self):
        cursor = get_db().cursor()
        cursor.execute("SELECT COUNT(*) FROM produtos")
        return cursor.fetchone()[0]

    @staticmethod
    def _to_dict(row):
        return {
            "id": row["id"],
            "nome": row["nome"],
            "descricao": row["descricao"],
            "preco": row["preco"],
            "estoque": row["estoque"],
            "categoria": row["categoria"],
            "ativo": row["ativo"],
            "criado_em": row["criado_em"],
        }

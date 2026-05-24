from src.database.connection import get_db


class UserRepository:
    def list_all(self):
        cursor = get_db().cursor()
        cursor.execute("SELECT * FROM usuarios ORDER BY id")
        return [self._to_public_dict(row, include_password=True) for row in cursor.fetchall()]

    def get_by_id(self, user_id):
        cursor = get_db().cursor()
        cursor.execute("SELECT * FROM usuarios WHERE id = ?", (user_id,))
        row = cursor.fetchone()
        return self._to_public_dict(row, include_password=True) if row else None

    def get_by_email(self, email):
        cursor = get_db().cursor()
        cursor.execute("SELECT * FROM usuarios WHERE email = ?", (email,))
        row = cursor.fetchone()
        return self._to_public_dict(row, include_password=True) if row else None

    def create(self, nome, email, senha, tipo="cliente"):
        connection = get_db()
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO usuarios (nome, email, senha, tipo) VALUES (?, ?, ?, ?)",
            (nome, email, senha, tipo),
        )
        connection.commit()
        return cursor.lastrowid

    def authenticate(self, email, senha):
        cursor = get_db().cursor()
        cursor.execute(
            "SELECT * FROM usuarios WHERE email = ? AND senha = ?",
            (email, senha),
        )
        row = cursor.fetchone()
        return self._to_public_dict(row, include_password=False) if row else None

    def count(self):
        cursor = get_db().cursor()
        cursor.execute("SELECT COUNT(*) FROM usuarios")
        return cursor.fetchone()[0]

    @staticmethod
    def _to_public_dict(row, include_password=False):
        data = {
            "id": row["id"],
            "nome": row["nome"],
            "email": row["email"],
            "tipo": row["tipo"],
            "criado_em": row["criado_em"],
        }
        if include_password:
            data["senha"] = row["senha"]
        return data

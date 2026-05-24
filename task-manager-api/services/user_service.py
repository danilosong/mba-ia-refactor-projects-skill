from errors import ConflictError, NotFoundError, ValidationError
from database import db
from models.user import User
from repositories.user_repository import UserRepository


class UserService:
    VALID_ROLES = ["user", "admin", "manager"]

    def __init__(self):
        self.user_repository = UserRepository()

    def list_users(self):
        return [user.to_dict(include_tasks=True) for user in self.user_repository.list_all()]

    def get_user(self, user_id):
        user = self.user_repository.get_by_id(user_id)
        if not user:
            raise NotFoundError("Usuario nao encontrado")
        return user.to_dict(include_tasks=True)

    def create_user(self, payload):
        if not payload:
            raise ValidationError("Dados invalidos")
        name = payload.get("name", "").strip()
        email = payload.get("email", "").strip()
        password = payload.get("password", "")
        role = payload.get("role", "user")
        if not name:
            raise ValidationError("Nome e obrigatorio")
        if not email:
            raise ValidationError("Email e obrigatorio")
        if len(password) < 4:
            raise ValidationError("Senha deve ter no minimo 4 caracteres")
        if role not in self.VALID_ROLES:
            raise ValidationError("Role invalido")
        if self.user_repository.get_by_email(email):
            raise ConflictError("Email ja cadastrado")

        user = User()
        user.name = name
        user.email = email
        user.role = role
        user.set_password(password)
        created = self.user_repository.create(user)
        return created.to_dict()

    def update_user(self, user_id, payload):
        user = self.user_repository.get_by_id(user_id)
        if not user:
            raise NotFoundError("Usuario nao encontrado")
        if not payload:
            raise ValidationError("Dados invalidos")

        if "name" in payload:
            user.name = payload["name"]
        if "email" in payload:
            existing = self.user_repository.get_by_email(payload["email"])
            if existing and existing.id != user_id:
                raise ConflictError("Email ja cadastrado")
            user.email = payload["email"]
        if "password" in payload:
            if len(payload["password"]) < 4:
                raise ValidationError("Senha muito curta")
            user.set_password(payload["password"])
        if "role" in payload:
            if payload["role"] not in self.VALID_ROLES:
                raise ValidationError("Role invalido")
            user.role = payload["role"]
        if "active" in payload:
            user.active = payload["active"]

        self.user_repository.update()
        return user.to_dict()

    def delete_user(self, user_id):
        user = self.user_repository.get_by_id(user_id)
        if not user:
            raise NotFoundError("Usuario nao encontrado")
        for task in list(user.tasks):
            db.session.delete(task)
        db.session.flush()
        self.user_repository.delete(user)

    def list_user_tasks(self, user_id):
        user = self.user_repository.get_by_id(user_id)
        if not user:
            raise NotFoundError("Usuario nao encontrado")
        return [task.to_dict(include_relations=True) for task in user.tasks]

    def login(self, payload):
        if not payload:
            raise ValidationError("Dados invalidos")
        email = payload.get("email", "").strip()
        password = payload.get("password", "")
        if not email or not password:
            raise ValidationError("Email e senha sao obrigatorios")
        user = self.user_repository.get_by_email(email)
        if not user or not user.check_password(password):
            raise ValidationError("Credenciais invalidas", status_code=401)
        if not user.active:
            raise ValidationError("Usuario inativo", status_code=403)
        return {
            "message": "Login realizado com sucesso",
            "user": user.to_dict(),
            "token": f"fake-jwt-token-{user.id}",
        }

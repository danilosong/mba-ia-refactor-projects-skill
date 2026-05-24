from src.errors import ConflictError, NotFoundError, ValidationError


class UserService:
    def __init__(self, user_repository):
        self.user_repository = user_repository

    def list_users(self):
        return self.user_repository.list_all()

    def get_user(self, user_id):
        user = self.user_repository.get_by_id(user_id)
        if not user:
            raise NotFoundError("Usuario nao encontrado")
        return user

    def create_user(self, payload):
        if not payload:
            raise ValidationError("Dados invalidos")
        nome = payload.get("nome", "").strip()
        email = payload.get("email", "").strip()
        senha = payload.get("senha", "").strip()
        if not nome or not email or not senha:
            raise ValidationError("Nome, email e senha sao obrigatorios")
        if self.user_repository.get_by_email(email):
            raise ConflictError("Email ja cadastrado")
        return {"id": self.user_repository.create(nome, email, senha)}

    def login(self, payload):
        if not payload:
            raise ValidationError("Dados invalidos")
        email = payload.get("email", "").strip()
        senha = payload.get("senha", "").strip()
        if not email or not senha:
            raise ValidationError("Email e senha sao obrigatorios")
        user = self.user_repository.authenticate(email, senha)
        if not user:
            raise ValidationError("Email ou senha invalidos", status_code=401)
        return user

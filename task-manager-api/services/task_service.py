from datetime import datetime

from errors import NotFoundError, ValidationError
from models.task import Task
from repositories.category_repository import CategoryRepository
from repositories.task_repository import TaskRepository
from repositories.user_repository import UserRepository
from utils.helpers import process_task_data


class TaskService:
    def __init__(self):
        self.task_repository = TaskRepository()
        self.user_repository = UserRepository()
        self.category_repository = CategoryRepository()

    def list_tasks(self):
        return [task.to_dict(include_relations=True) for task in self.task_repository.list_all()]

    def get_task(self, task_id):
        task = self.task_repository.get_by_id(task_id)
        if not task:
            raise NotFoundError("Task nao encontrada")
        return task.to_dict(include_relations=True)

    def create_task(self, payload):
        if not payload:
            raise ValidationError("Dados invalidos")

        normalized, error = process_task_data(payload)
        if error:
            raise ValidationError(error)
        if "title" not in normalized:
            raise ValidationError("Titulo e obrigatorio")

        self._validate_relations(payload.get("user_id"), payload.get("category_id"))

        task = Task()
        task.title = normalized["title"]
        task.description = normalized.get("description", "")
        task.status = normalized.get("status", "pending")
        task.priority = normalized.get("priority", 3)
        task.user_id = payload.get("user_id")
        task.category_id = payload.get("category_id")
        task.due_date = normalized.get("due_date")
        task.tags = normalized.get("tags")

        created = self.task_repository.create(task)
        return created.to_dict(include_relations=True)

    def update_task(self, task_id, payload):
        task = self.task_repository.get_by_id(task_id)
        if not task:
            raise NotFoundError("Task nao encontrada")
        if not payload:
            raise ValidationError("Dados invalidos")

        normalized, error = process_task_data(payload, existing_task=task)
        if error:
            raise ValidationError(error)

        self._validate_relations(payload.get("user_id"), payload.get("category_id"))

        for field, value in normalized.items():
            setattr(task, field, value)
        if "user_id" in payload:
            task.user_id = payload.get("user_id")
        if "category_id" in payload:
            task.category_id = payload.get("category_id")
        task.updated_at = datetime.utcnow()
        self.task_repository.update()
        return task.to_dict(include_relations=True)

    def delete_task(self, task_id):
        task = self.task_repository.get_by_id(task_id)
        if not task:
            raise NotFoundError("Task nao encontrada")
        self.task_repository.delete(task)

    def search_tasks(self, params):
        tasks = self.task_repository.search(
            params.get("q", ""),
            params.get("status", ""),
            params.get("priority", ""),
            params.get("user_id", ""),
        )
        return [task.to_dict(include_relations=True) for task in tasks]

    def stats(self):
        return self.task_repository.stats()

    def _validate_relations(self, user_id, category_id):
        if user_id and not self.user_repository.get_by_id(user_id):
            raise NotFoundError("Usuario nao encontrado")
        if category_id and not self.category_repository.get_by_id(category_id):
            raise NotFoundError("Categoria nao encontrada")

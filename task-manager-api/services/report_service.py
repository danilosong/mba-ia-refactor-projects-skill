from datetime import datetime, timedelta

from errors import NotFoundError, ValidationError
from models.task import Task
from repositories.category_repository import CategoryRepository
from repositories.user_repository import UserRepository


class ReportService:
    def __init__(self):
        self.user_repository = UserRepository()
        self.category_repository = CategoryRepository()

    def summary_report(self):
        total_tasks = Task.query.count()
        total_users = len(self.user_repository.list_all())
        total_categories = len(self.category_repository.list_all())
        pending = Task.query.filter_by(status="pending").count()
        in_progress = Task.query.filter_by(status="in_progress").count()
        done = Task.query.filter_by(status="done").count()
        cancelled = Task.query.filter_by(status="cancelled").count()

        priority_counts = {priority: Task.query.filter_by(priority=priority).count() for priority in range(1, 6)}
        all_tasks = Task.query.all()
        overdue_list = [
            {
                "id": task.id,
                "title": task.title,
                "due_date": str(task.due_date),
                "days_overdue": (datetime.utcnow() - task.due_date).days,
            }
            for task in all_tasks
            if task.is_overdue()
        ]

        seven_days_ago = datetime.utcnow() - timedelta(days=7)
        recent_tasks = Task.query.filter(Task.created_at >= seven_days_ago).count()
        recent_done = Task.query.filter(Task.status == "done", Task.updated_at >= seven_days_ago).count()

        user_stats = []
        for user in self.user_repository.list_all():
            total = len(user.tasks)
            completed = sum(1 for task in user.tasks if task.status == "done")
            user_stats.append(
                {
                    "user_id": user.id,
                    "user_name": user.name,
                    "total_tasks": total,
                    "completed_tasks": completed,
                    "completion_rate": round((completed / total) * 100, 2) if total > 0 else 0,
                }
            )

        return {
            "generated_at": str(datetime.utcnow()),
            "overview": {
                "total_tasks": total_tasks,
                "total_users": total_users,
                "total_categories": total_categories,
            },
            "tasks_by_status": {
                "pending": pending,
                "in_progress": in_progress,
                "done": done,
                "cancelled": cancelled,
            },
            "tasks_by_priority": {
                "critical": priority_counts[1],
                "high": priority_counts[2],
                "medium": priority_counts[3],
                "low": priority_counts[4],
                "minimal": priority_counts[5],
            },
            "overdue": {
                "count": len(overdue_list),
                "tasks": overdue_list,
            },
            "recent_activity": {
                "tasks_created_last_7_days": recent_tasks,
                "tasks_completed_last_7_days": recent_done,
            },
            "user_productivity": user_stats,
        }

    def user_report(self, user_id):
        user = self.user_repository.get_by_id(user_id)
        if not user:
            raise NotFoundError("Usuario nao encontrado")
        tasks = user.tasks
        total = len(tasks)
        done = sum(1 for task in tasks if task.status == "done")
        pending = sum(1 for task in tasks if task.status == "pending")
        in_progress = sum(1 for task in tasks if task.status == "in_progress")
        cancelled = sum(1 for task in tasks if task.status == "cancelled")
        overdue = sum(1 for task in tasks if task.is_overdue())
        high_priority = sum(1 for task in tasks if task.priority <= 2)
        return {
            "user": {"id": user.id, "name": user.name, "email": user.email},
            "statistics": {
                "total_tasks": total,
                "done": done,
                "pending": pending,
                "in_progress": in_progress,
                "cancelled": cancelled,
                "overdue": overdue,
                "high_priority": high_priority,
                "completion_rate": round((done / total) * 100, 2) if total > 0 else 0,
            },
        }

    def list_categories(self):
        return [category.to_dict(include_task_count=True) for category in self.category_repository.list_all()]

    def create_category(self, payload):
        if not payload:
            raise ValidationError("Dados invalidos")
        from models.category import Category

        name = payload.get("name", "").strip()
        if not name:
            raise ValidationError("Nome e obrigatorio")
        category = Category()
        category.name = name
        category.description = payload.get("description", "")
        category.color = payload.get("color", "#000000")
        return self.category_repository.create(category).to_dict(include_task_count=True)

    def update_category(self, category_id, payload):
        category = self.category_repository.get_by_id(category_id)
        if not category:
            raise NotFoundError("Categoria nao encontrada")
        if "name" in payload:
            category.name = payload["name"]
        if "description" in payload:
            category.description = payload["description"]
        if "color" in payload:
            category.color = payload["color"]
        self.category_repository.update()
        return category.to_dict(include_task_count=True)

    def delete_category(self, category_id):
        category = self.category_repository.get_by_id(category_id)
        if not category:
            raise NotFoundError("Categoria nao encontrada")
        self.category_repository.delete(category)

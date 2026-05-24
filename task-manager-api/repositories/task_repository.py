from sqlalchemy.orm import joinedload

from database import db
from models.task import Task


class TaskRepository:
    def list_all(self):
        return (
            Task.query.options(joinedload(Task.user), joinedload(Task.category))
            .order_by(Task.id)
            .all()
        )

    def get_by_id(self, task_id):
        return (
            Task.query.options(joinedload(Task.user), joinedload(Task.category))
            .filter_by(id=task_id)
            .first()
        )

    def create(self, task):
        db.session.add(task)
        db.session.commit()
        return task

    def update(self):
        db.session.commit()

    def delete(self, task):
        db.session.delete(task)
        db.session.commit()

    def search(self, query_text="", status="", priority="", user_id=""):
        query = Task.query.options(joinedload(Task.user), joinedload(Task.category))
        if query_text:
            query = query.filter(
                db.or_(
                    Task.title.like(f"%{query_text}%"),
                    Task.description.like(f"%{query_text}%"),
                )
            )
        if status:
            query = query.filter(Task.status == status)
        if priority:
            query = query.filter(Task.priority == int(priority))
        if user_id:
            query = query.filter(Task.user_id == int(user_id))
        return query.order_by(Task.id).all()

    def stats(self):
        total = Task.query.count()
        pending = Task.query.filter_by(status="pending").count()
        in_progress = Task.query.filter_by(status="in_progress").count()
        done = Task.query.filter_by(status="done").count()
        cancelled = Task.query.filter_by(status="cancelled").count()
        overdue = sum(1 for task in Task.query.all() if task.is_overdue())
        return {
            "total": total,
            "pending": pending,
            "in_progress": in_progress,
            "done": done,
            "cancelled": cancelled,
            "overdue": overdue,
            "completion_rate": round((done / total) * 100, 2) if total > 0 else 0,
        }

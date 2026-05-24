from sqlalchemy.orm import joinedload

from database import db
from models.user import User


class UserRepository:
    def list_all(self):
        return User.query.options(joinedload(User.tasks)).order_by(User.id).all()

    def get_by_id(self, user_id):
        return User.query.options(joinedload(User.tasks)).filter_by(id=user_id).first()

    def get_by_email(self, email):
        return User.query.filter_by(email=email).first()

    def create(self, user):
        db.session.add(user)
        db.session.commit()
        return user

    def update(self):
        db.session.commit()

    def delete(self, user):
        db.session.delete(user)
        db.session.commit()

from sqlalchemy.orm import joinedload

from database import db
from models.category import Category


class CategoryRepository:
    def list_all(self):
        return Category.query.options(joinedload(Category.tasks)).order_by(Category.id).all()

    def get_by_id(self, category_id):
        return Category.query.options(joinedload(Category.tasks)).filter_by(id=category_id).first()

    def create(self, category):
        db.session.add(category)
        db.session.commit()
        return category

    def update(self):
        db.session.commit()

    def delete(self, category):
        db.session.delete(category)
        db.session.commit()

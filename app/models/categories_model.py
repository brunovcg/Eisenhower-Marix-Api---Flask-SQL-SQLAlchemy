from app.configs.database import db
from app.models.tasks_categories_table import tasks_categories
from dataclasses import dataclass
from flask import current_app
import psycopg2
from sqlalchemy.exc import IntegrityError

@dataclass
class CategoriesModel(db.Model):
    __tablename__ = "categories"
            
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text)
            
    # tasks = db.relationship("TasksModel", secondary=tasks_categories, cascade="all, delete",passive_deletes=True,backref="categories")

    tasks = db.relationship("TasksModel", secondary=tasks_categories, back_populates="categories", passive_deletes=True)

    @staticmethod
    def create_one(data):
        session = current_app.db.session
        categories = CategoriesModel(**data)

        try:    

            session.add(categories)
            session.commit()

        except IntegrityError as e:

            if type(e.orig) == psycopg2.errors.UniqueViolation:

                return "category exists"

        return {
        "id": categories.id,
        "name": categories.name,
        "description": categories.description,
         }


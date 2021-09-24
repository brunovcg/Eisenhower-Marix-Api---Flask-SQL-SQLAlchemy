from app.configs.database import db
from app.models.tasks_categories_table import tasks_categories
from dataclasses import dataclass

@dataclass
class CategoriesModel(db.Model):
    __tablename__ = "categories"
            
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text)
            
    tasks = db.relationship("TasksModel", secondary=tasks_categories, backref="categories")


from app.configs.database import db
from app.models.tasks_categories_table import tasks_categories
from dataclasses import dataclass
from app.models.eisenhowers_model import EisenhowersModel as EM
from app.models.categories_model import CategoriesModel as CM
from flask import current_app
import psycopg2
from sqlalchemy.exc import IntegrityError

@dataclass
class TasksModel(db.Model):
    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    description = db.Column(db.Text)
    duration = db.Column(db.Integer)
    importance = db.Column(db.Integer)
    urgency = db.Column(db.Integer)  
    eisenhower_id = db.Column(db.Integer, db.ForeignKey('eisenhowers.id'), nullable=False)

    categories = db.relationship("CategoriesModel", secondary=tasks_categories, back_populates="tasks",cascade="all, delete")

    @staticmethod
    def create_one(data):

        for item in data["categories"]:

            if not CM.query.filter_by(name = item["name"]).first():
                CM.create_one({"name" : item["name"],
                    "description" : "Automatically Created"})

        eisenhower_type = EM.get_type(data["importance"], data["urgency"])

        eisenhower_qualification = EM.query.get(eisenhower_type)
   
        new_entry = {
            "name" : data["name"], 
            "description" : data["description"],
            "duration" : data["duration"],
            "importance" : data["importance"], 
            "urgency" : data["urgency"],
            "eisenhower_id" : eisenhower_type
        }

        session = current_app.db.session
        task = TasksModel(**new_entry)

        try:    
            session.add(task)
            session.commit()

        except IntegrityError as e:

            if type(e.orig) == psycopg2.errors.UniqueViolation:

                return "task exists"

        #  Preenchendo automatico a tabela PIVOT----------------------------------------------------------------

        categories_ids = []
        for category in data['categories']:
            
            cat_id = CM.query.filter_by(name=category["name"]).first()
            categories_ids.append(cat_id.id)

        for category_id in categories_ids:

            task: TasksModel = TasksModel.query.get(task.id)
            category : CM = CM.query.get(category_id)
            category.tasks.append(task)
            session.commit()

        return {
            "id" : task.id,
            "name" : task.name,
            "description" : task.description,
            "duration" : task.duration,
            "eisenhower_classification" : eisenhower_qualification.type,
            "category": data["categories"]
        }

    @staticmethod
    def update_one(data, task_id):
        
        task = TasksModel.query.get(task_id)
        if not task:
            return "task not found"   

        try:
            new_importance = data['importance']
        except KeyError:
            new_importance = task.importance

        try:
            new_urgency = data['urgency']
        except KeyError:
            new_urgency = task.urgency
           
        eisenhower_type = EM.get_type(new_importance, new_urgency)
        
        new_classification= EM.query.get(eisenhower_type)

        TasksModel.query.filter(TasksModel.id == task_id).update(data)
        current_app.db.session.commit()

        return {
            "id": task.id,
            "name" : task.name,
            "description" : task.description,
            "duration" : task.duration,
            "eisenhower_classification" : new_classification.type
        }

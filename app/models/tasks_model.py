from app.configs.database import db
from dataclasses import dataclass
from app.models.eisenhowers_model import EisenhowersModel as EM
from app.models.categories_model import CategoriesModel as CM
from flask import current_app

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


    @staticmethod
    def create_one(data):
        

        for item in data["categories"]:

            if not CM.query.filter_by(name = item["name"]).first():
                CM.create_one({"name" : item["name"],
                    "description" : "Automatically Created"})

        eisenhower_type = EM.get_type(data["importance"], data["urgency"])

        eisenhower_qualification = EM.query.get(eisenhower_type)
   

        task = TasksModel({"name" : data["name"], 
            "description" : data["description",
            "duration" : data["duration"],
            "importance" : data["importance"], 
            "urgency" : data["urgency"],
            "eisenhower_id" : eisenhower_type       
        ]})

        return {
            "id" : task.id,
            "name" : task.name,
            "description" : task.description,
            "duration" : task.duration,
            "eisenhower_classification" : eisenhower_qualification,
            "category": data["categories"]
        }

    
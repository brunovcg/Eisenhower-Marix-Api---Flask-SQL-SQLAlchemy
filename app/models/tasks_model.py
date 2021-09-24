from app.configs.database import db

class TasksModel(db.Model):
    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    description = db.Column(db.Text)
    duration = db.Column(db.Integer)
    importance = db.Column(db.Integer)
    urgency = db.Column(db.Integer)  
    eisenhower_id = db.Column(db.Integer, db.ForeignKey('eisenhower.id'), nullable=False)

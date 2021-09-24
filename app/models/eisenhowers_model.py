from app.configs.database import db

class EisenhowersModel(db.Model):
    __tablename__ = 'eisenhower'

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(100))
    
    tasks = db.relationship("TasksModel", backref="eisenhowers")
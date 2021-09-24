from app.configs.database import db

class EisenhowersModel(db.Model):
    __tablename__ = 'eisenhowers'

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(100))
    
    tasks = db.relationship("TasksModel", backref="eisenhowers")

    @staticmethod
    def get_type(importance, urgency):
        if importance == 1 and urgency == 1:
            return 1
        elif importance == 1 and urgency == 2:
            return 2
        elif importance == 2 and urgency == 1:
            return 3
        elif importance == 2 and urgency == 2:
            return 4
from app.configs.database import db

tasks_categories = db.Table('tasks_categories',
    db.Column('id', db.Integer, primary_key=True),
    db.Column('task_id', db.Integer, db.ForeignKey('tasks.id', ondelete="CASCADE", onupdate="CASCADE")),
    db.Column('category_id', db.Integer, db.ForeignKey('categories.id', ondelete="CASCADE", onupdate="CASCADE")),
) 

from flask import Blueprint
from app.configs.database import db
from flask import jsonify
from app.models.categories_model import CategoriesModel as CM
from app.models.tasks_model import TasksModel as TM
from app.models.eisenhowers_model import EisenhowersModel as EM
from app.models.tasks_categories_table import tasks_categories as TC

          
bp_view_root = Blueprint("bp_view_root", __name__)
          
@bp_view_root.get("/")
def get_all_categories_with_tasks():
    
    get_pivot = db.session.query(TM,CM,EM).select_from(TM).join(TC).join(CM).join(EM).all()

    query_categories = CM.query.all()

    list_categories = [{
        "id" : categories.id,
        "name" : categories.name,
        "description" : categories.description,
        "tasks" : [{
            "id":line[0].id,
            "name": line[0].name,
            "description": line[0].description,
            "priority" : line[2].type
        } for line in get_pivot if line[1].id == categories.id]
    } for categories in query_categories]

    return jsonify(list_categories), 200

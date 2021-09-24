from flask import Blueprint, request, current_app, jsonify
from app.models.tasks_model import TasksModel as TM
import psycopg2
from sqlalchemy.exc import IntegrityError


bp_view_tasks = Blueprint("bp_view_tasks", __name__)

@bp_view_tasks.post("/task")
def create_task():
    
    data = request.get_json()

    if (data["importance"] < 0 or data["importance"] > 2 ) or (data["urgency"] < 0 or data["urgency"] > 2 ):
        return jsonify({
            "error" : {
                "valid_options" : {
                    "importance" : [1,2],
                    "urgency": [1,2]

            },
                "received_options" : {
                    "importance" : data["importance"],
                    "urgency": data["urgency"]
                }
            }
        }), 404

    task = TM.create_one(data)

    if task == "task exists":
        return {"msg" : "Task already exixts"}, 409


    return jsonify(task), 201


@bp_view_tasks.patch("/task/<id>")
def update_tasks(id):
    data = request.json

    TM.query.filter(TM.id==id).update(data)
    current_app.db.session.commit()
    task = TM.query.get(id)

    return "",200 


    ...

@bp_view_tasks.delete("/task/<id>")
def delete_tasks(id):
    task = TM.query.get(id)
    if not task:
        return {"msg" : "task not found"}, 404

    TM.query.filter(TM.id==id).delete()
    current_app.db.session.commit()

    # try:

    #     TM.query.filter(TM.id==id).delete()
    #     current_app.db.session.commit()

    # except IntegrityError as e:
    
    #     if type(e.orig) == psycopg2.errors.ForeignKeyViolation:
            
        
    #         return "This task is been used on other ", 400

   
    return "", 204
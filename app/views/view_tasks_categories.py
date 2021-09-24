from flask import Blueprint, request, current_app


          
bp_create_tasks_categories = Blueprint("bp_create_tasks_categories", __name__)
          
# @bp_create_tasks_categories.route("/task_category", methods=["POST"])
# def create_tasks_categories():
#     session = current_app.db.session
          
#     data = request.get_json()
          
#     task: TM = TM.query.filter_by(id=data["task_id"]).first()
#     category: CM = CM.query.filter_by(id=data["category_id"]).first()

#     task.categories.append(category)
    
#     session.commit()
          
#     return {
#       "task_id": task.id,
#       "category_id": category.id,
#     }, 201




@bp_create_tasks_categories.delete("/task_category/<id>")
def delete_tasks_categories(id):
    query =  current_app.db.tasks_category.query.get(id)

    if not query:
        return {"msg" : "task not found"}, 404
    
    current_app.db.session.delete(query)
    current_app.db.session.commit()
  

    return "", 204
    
from flask import Blueprint, request, current_app, jsonify
from app.models.categories_model import CategoriesModel as CM

bp_view_categories= Blueprint("bp_view_categories", __name__)

@bp_view_categories.post("/category")
def create_category():

    data = request.get_json()

    category = CM.create_one(data)

    if category == "category exists":
        return {"msg" : "Category already exixts"}, 409

    return jsonify(category), 201


@bp_view_categories.patch("/category/<id>")
def update_category(id):
    data = request.json

    CM.query.filter(CM.id==id).update(data)
    current_app.db.session.commit()
    category = CM.query.get(id)

    if not category:
        return {"msg" : "Category not found"}, 404
        
    return jsonify({"id" : category.id, "name": category.name, "description": category.description}), 200


@bp_view_categories.delete("/category/<id>")
def delete_category(id):

    category = CM.query.get(id)
    if not category:
        return {"msg" : "Category not found"}, 404

    CM.query.filter(CM.id==id).delete()
    current_app.db.session.commit()
   
    return "", 204


@bp_view_categories.get("/category/<id>")
def get_one_category(id):

    category = CM.query.get(id)

    if not category:
        return {"msg" : "Category not found"}, 404
   
    return jsonify({"id" : category.id, "name": category.name, "description": category.description}), 200

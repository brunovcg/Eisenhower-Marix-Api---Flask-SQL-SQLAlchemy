from flask import Blueprint, request, current_app, jsonify
from app.models.categories_model import CategoriesModel as CM
from sqlalchemy.exc import IntegrityError
import psycopg2

bp_create_categories= Blueprint("bp_create_categories", __name__)


@bp_create_categories.post("/category")
def create_categories():
    session = current_app.db.session
    
    data = request.get_json()
          
    categories = CM(**data)

    try:

        session.add(categories)
        session.commit()

    except IntegrityError as e:

        if type(e.orig) == psycopg2.errors.UniqueViolation:

            return {"msg" : "Category already exixts"}, 400
          
    return {
        "id": categories.id,
        "name": categories.name,
        "description": categories.description,
    }, 201



@bp_create_categories.patch("/category/<id>")
def update(id):
    data = request.json


    CM.query.filter(CM.id==id).update(data)
    current_app.db.session.commit()
    category = CM.query.get(id)

    if not category:
        return {"msg" : "Category not found"}, 404
        

    return jsonify({"id" : category.id, "name": category.name, "description": category.description}), 200



@bp_create_categories.delete("/category/<id>")
def delete_one(id):


    category = CM.query.get(id)
    if not category:
        return {"msg" : "Category not found"}, 404

    CM.query.filter(CM.id==id).delete()
    current_app.db.session.commit()


   
    return "", 204


@bp_create_categories.get("/category/<id>")
def get_one_category(id):

    category = CM.query.get(id)

    if not category:
        return {"msg" : "Category not found"}, 404
   
    return jsonify({"id" : category.id, "name": category.name, "description": category.description}), 200

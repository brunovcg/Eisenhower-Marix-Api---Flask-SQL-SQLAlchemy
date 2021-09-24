from flask import Blueprint, request, current_app
from app.models.categories_model import CategoriesModel as CM

bp_create_categories= Blueprint("bp_create_categories", __name__)

@bp_create_categories.post("/bacia_hidrografica")
def create_categories():
    session = current_app.db.session
          
    data = request.get_json()
          
    categories = CM(**data)
          
    session.add(categories)
    session.commit()
          
    return {
        "id": categories.id,
        "name": categories.name,
        "description": categories.description,
    }, 201
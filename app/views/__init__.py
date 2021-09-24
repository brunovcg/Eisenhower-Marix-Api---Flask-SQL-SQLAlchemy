from flask import Flask

def init_app(app: Flask) -> None:
    from .create_categories import bp_create_categories

    app.register_blueprint(bp_create_categories)

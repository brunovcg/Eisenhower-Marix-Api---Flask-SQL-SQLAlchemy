from flask import Flask

def init_app(app: Flask) -> None:
    from .view_categories import bp_view_categories
    app.register_blueprint(bp_view_categories)

    from .view_tasks import bp_view_tasks
    app.register_blueprint(bp_view_tasks)

    from .view_root import bp_view_root
    app.register_blueprint(bp_view_root)

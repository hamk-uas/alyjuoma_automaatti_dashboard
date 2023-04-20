import os

from flask import Flask


def create_app():
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_pyfile('config.py')

    @app.route("/hello")
    def hello():
        return 'Hello, World!'
    
    @app.route("/admin")
    def admin():
        return f"db: {app.config['DATABASE_HOST']} {app.config['DATABASE_NAME']} {app.config['DATABASE_USER']} {app.config['DATABASE_PASSWORD']}"
    

    from . import db
    db.init_app(app)

    from . import data
    app.register_blueprint(data.bp)

    return app
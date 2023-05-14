import os

from flask import Flask
from flask_cors import CORS


def create_app(test_config=False):
    app = Flask(__name__, instance_relative_config=True)
    CORS(app)

    if test_config is False:
        app.config.from_pyfile('config.py')
    else:
        app.config.from_pyfile('config_test.py')

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

    from . import download
    app.register_blueprint(download.bp)

    return app
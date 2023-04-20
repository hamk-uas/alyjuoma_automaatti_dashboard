import mysql.connector

from flask import current_app, g


def init_app(app):
    app.teardown_appcontext(close_db)

def get_db():
    if 'db' not in g:
        g.db = mysql.connector.connect(
            host=current_app.config["DATABASE_HOST"],
            database=current_app.config["DATABASE_NAME"],
            user=current_app.config["DATABASE_USER"],
            password=current_app.config["DATABASE_PASSWORD"]
        )
    
    return g.db


def close_db():
    db = g.pop('db', None)

    if db is not None:
        db.close()
import psycopg2

from flask import current_app, g

def get_db():
    if 'db' not in g:
        g.db = psycopg2.connect(
            host=current_app.config["DATABASE_HOST"],
            database=current_app.config["DATABASE_NAME"],
            user=current_app.config["DATABASE_USER"],
            password=current_app.config["DATABASE_PASSWORD"]
        )
    
    return g.db

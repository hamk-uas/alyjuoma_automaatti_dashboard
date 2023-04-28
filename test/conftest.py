import pytest
import mysql.connector

from alyjuoma_automaatti_dashboard import create_app

@pytest.fixture
def app():
    app = create_app(test_config=True)

    conn = mysql.connector.connect(
        host=app.config['DATABASE_HOST'],
        user=app.config['DATABASE_USER'],
        password=app.config['DATABASE_PASSWORD'])
    
    cur = conn.cursor()

    cur.execute(f'DROP DATABASE IF EXISTS {app.config["DATABASE_NAME"]}')
    conn.commit()

    cur.execute(f'CREATE DATABASE {app.config["DATABASE_NAME"]}')
    conn.commit()

    cur.execute(f'USE {app.config["DATABASE_NAME"]}')


    cur.execute('CREATE TABLE sensor_data (id serial PRIMARY KEY,'
                                 'dtime DATETIME(6) NOT NULL,'
                                 'farm_id TEXT NOT NULL,'
                                 'station_id TEXT NOT NULL,'
                                 'parameter_type TEXT NOT NULL,'
                                 'parameter_value DOUBLE PRECISION NOT NULL)'
                                 )
    conn.commit()

    yield app

    cur.execute(f'DROP DATABASE IF EXISTS {app.config["DATABASE_NAME"]}')
    conn.commit()


@pytest.fixture
def client(app):
    return app.test_client()

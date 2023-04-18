import os
import mysql.connector

conn = mysql.connector.connect(
        host="localhost",
        database="aja_dash_db",
        user=os.environ['DATABASE_USER'],
        password=os.environ['DATABASE_PASSWORD'])

cur = conn.cursor()

cur.execute('DROP TABLE IF EXISTS sensor_data;')

cur.execute('CREATE TABLE sensor_data (id serial PRIMARY KEY,'
                                 'dtime TIMESTAMP NOT NULL,'
                                 'farm_id TEXT NOT NULL,'
                                 'station_id TEXT NOT NULL,'
                                 'parameter_type TEXT NOT NULL,'
                                 'parameter_value DOUBLE PRECISION NOT NULL);'
                                 )



conn.commit()

cur.close()
conn.close()
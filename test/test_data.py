import pytest
import datetime
import json

from alyjuoma_automaatti_dashboard.db import get_db


def test_all(client, app):
    date_one_obj = datetime.datetime.strptime("2023-04-11 14:04:02.140000", '%Y-%m-%d %H:%M:%S.%f')
    date_two_obj = datetime.datetime.strptime("2023-04-12 12:54:33.920000", '%Y-%m-%d %H:%M:%S.%f')

    with app.app_context():
        conn = get_db()
        cur = conn.cursor()
        cur.execute("INSERT INTO sensor_data (dtime, farm_id, station_id, parameter_type, parameter_value) VALUES (%s, %s, %s, %s, %s)",
            (date_one_obj, "ÄÄJ", "ST1", "Temp3", 22.453))
        conn.commit()
        cur.execute("INSERT INTO sensor_data (dtime, farm_id, station_id, parameter_type, parameter_value) VALUES (%s, %s, %s, %s, %s)",
            (date_two_obj, "ÄÄJ", "ST1", "Temp3", 12.009))
        conn.commit()

        response = client.get('/data/all')
        r_data = json.loads(response.data)

        r_data_sample_one = r_data["result"][0]
        r_data_sample_two = r_data["result"][1]

        assert response.status_code == 200
        print("Response OK")

        assert len(r_data['result']) == 2
        print("Number of data entries correct")

        assert r_data_sample_one == {
            "id": 1,
            "dtime": "2023-04-11 14:04:02.140000",
            "farm_id": "ÄÄJ",
            "station_id": "ST1",
            "parameter_type": "Temp3",
            "parameter_value": 22.453
        }
        print("First data entry is correct.")

        assert r_data_sample_two == {
            "id": 2,
            "dtime": "2023-04-12 12:54:33.920000",
            "farm_id": "ÄÄJ",
            "station_id": "ST1",
            "parameter_type": "Temp3",
            "parameter_value": 12.009
        }
        print("Second data entry is correct.")

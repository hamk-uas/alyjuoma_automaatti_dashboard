import datetime
import json
from freezegun import freeze_time

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

        assert len(r_data['result']) == 2

        assert r_data_sample_one == {
            "id": 1,
            "dtime": "2023-04-11 14:04:02.140000",
            "farm_id": "ÄÄJ",
            "station_id": "ST1",
            "parameter_type": "Temp3",
            "parameter_value": 22.453
        }

        assert r_data_sample_two == {
            "id": 2,
            "dtime": "2023-04-12 12:54:33.920000",
            "farm_id": "ÄÄJ",
            "station_id": "ST1",
            "parameter_type": "Temp3",
            "parameter_value": 12.009
        }


@freeze_time("2023-05-01 12:34:56.789012")
def test_write(client, app):
    with app.app_context():
        response = client.post('/data/write', data='ÄÄJ;ST1;Temp3;22.453')

        assert response.status_code == 200

        conn = get_db()
        cur = conn.cursor()
        cur.execute('SELECT * FROM sensor_data')
        data = cur.fetchall()

        assert len(data) == 1

        data = list(data[0])
        data[1] = datetime.datetime.strftime(data[1], '%Y-%m-%d %H:%M:%S.%f')

        assert data == [1, "2023-05-01 12:34:56.789012", "ÄÄJ", "ST1", "Temp3", 22.453]
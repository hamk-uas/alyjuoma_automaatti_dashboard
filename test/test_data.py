import datetime
import json
from freezegun import freeze_time

from alyjuoma_automaatti_dashboard.db import get_db


def test_data_all(client, app):
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
def test_data_write(client, app):
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


def test_data_slice(client, app):
    date_one_obj = datetime.datetime.strptime("2023-04-11 14:04:02.140000", '%Y-%m-%d %H:%M:%S.%f')
    date_two_obj = datetime.datetime.strptime("2023-04-12 15:32:33.020000", '%Y-%m-%d %H:%M:%S.%f')
    date_three_obj = datetime.datetime.strptime("2023-04-13 14:04:02.340000", '%Y-%m-%d %H:%M:%S.%f')
    date_four_obj = datetime.datetime.strptime("2023-04-14 12:54:33.920000", '%Y-%m-%d %H:%M:%S.%f')
    date_five_obj = datetime.datetime.strptime("2023-04-14 12:55:33.920000", '%Y-%m-%d %H:%M:%S.%f')
    date_six_obj = datetime.datetime.strptime("2023-04-15 10:12:33.920000", '%Y-%m-%d %H:%M:%S.%f')
    date_seven_obj = datetime.datetime.strptime("2023-04-16 02:53:33.920000", '%Y-%m-%d %H:%M:%S.%f')
    date_eight_obj = datetime.datetime.strptime("2023-04-17 17:23:33.920000", '%Y-%m-%d %H:%M:%S.%f')
    date_nine_obj = datetime.datetime.strptime("2023-04-17 17:24:33.920000", '%Y-%m-%d %H:%M:%S.%f')
    date_ten_obj = datetime.datetime.strptime("2023-04-17 17:25:33.920000", '%Y-%m-%d %H:%M:%S.%f')


    with app.app_context():
        conn = get_db()
        cur = conn.cursor()

        query = "INSERT INTO sensor_data(dtime, farm_id, station_id, parameter_type, parameter_value) VALUES (%s, %s, %s, %s, %s)"
        values = [
            (date_one_obj, "MUS", "ST1", "Temp1", 23.003),
            (date_two_obj, "MUS", "ST2", "RGTPress", 346.32),
            (date_three_obj, "ÄÄJ", "ST3", "Temp3", 13.231),
            (date_four_obj, "ÄÄJ", "ST1", "Temp3", 20.09),
            (date_five_obj, "ÄÄJ", "ST1", "Temp1", 20.0),
            (date_six_obj, "MUS", "ST2", "RGTPress", 11.23),
            (date_seven_obj, "ÄÄJ", "ST1", "RGTPress", 122.1233),
            (date_eight_obj, "ÄÄJ", "ST3", "Temp1", 27.233),
            (date_nine_obj, "MUS", "ST2", "RFID", 121.242),
            (date_ten_obj, "ÄÄJ", "ST3", "PumpStat", 1)
        ]

        cur.executemany(query, values)
        conn.commit()


        test_params = {
            "dtime": ["2023-04-13 00:00:00.000000", "2023-04-17 17:24:00.000000"],
            "station_id": ["ST2", "ST3"]
        }

        response = client.post("/data/slice", json=test_params)
        res = response.get_json()['result']

        assert response.status_code == 200

        assert len(res) == 3

        assert res == [
            {
                'id': 3,
                'dtime': "2023-04-13 14:04:02.340000",
                'farm_id': "ÄÄJ",
                'station_id': "ST3",
                'parameter_type': "Temp3",
                'parameter_value': 13.231    
            }, 
            {
                'id': 6,
                'dtime': "2023-04-15 10:12:33.920000",
                'farm_id': "MUS",
                'station_id': "ST2",
                'parameter_type': "RGTPress",
                'parameter_value': 11.23   
            }, 
            {
                'id': 8,
                'dtime': "2023-04-17 17:23:33.920000",
                'farm_id': "ÄÄJ",
                'station_id': "ST3",
                'parameter_type': "Temp1",
                'parameter_value': 27.233    
            }
        ]




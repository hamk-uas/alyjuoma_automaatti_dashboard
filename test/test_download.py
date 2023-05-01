import datetime

from alyjuoma_automaatti_dashboard.db import get_db


def test_download_all(app, client):
    date_one_obj = datetime.datetime.strptime("2023-04-11 14:04:02.140000", '%Y-%m-%d %H:%M:%S.%f')
    date_two_obj = datetime.datetime.strptime("2023-04-12 15:32:33.020000", '%Y-%m-%d %H:%M:%S.%f')
    date_three_obj = datetime.datetime.strptime("2023-04-13 14:04:02.340000", '%Y-%m-%d %H:%M:%S.%f')
    date_four_obj = datetime.datetime.strptime("2023-04-14 12:54:33.920000", '%Y-%m-%d %H:%M:%S.%f')

    with app.app_context():
        conn = get_db()
        cur = conn.cursor()

        query = "INSERT INTO sensor_data(dtime, farm_id, station_id, parameter_type, parameter_value) VALUES (%s, %s, %s, %s, %s)"
        values = [
            (date_one_obj, "MUS", "ST1", "Temp1", 23.003),
            (date_two_obj, "MUS", "ST2", "RGTPress", 346.32),
            (date_three_obj, "ÄÄJ", "ST3", "Temp3", 13.231),
            (date_four_obj, "ÄÄJ", "ST1", "Temp3", 20.09)
        ]

        cur.executemany(query, values)
        conn.commit()

        res = client.get('/download/all')
        res = res.get_data().decode('UTF-8')
        
        print(res)

        row0 = "id,dtime,farm_id,station_id,parameter_type,parameter_value\n"
        row1 = "1,2023-04-11 14:04:02.140000,MUS,ST1,Temp1,23.003\n"
        row2 = "2,2023-04-12 15:32:33.020000,MUS,ST2,RGTPress,346.32\n"
        row3 = "3,2023-04-13 14:04:02.340000,ÄÄJ,ST3,Temp3,13.231\n"
        row4 = "4,2023-04-14 12:54:33.920000,ÄÄJ,ST1,Temp3,20.09\n"

        assert res == row0 + row1 + row2 + row3 + row4


def test_download_slice(app, client):
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

        response = client.post("/download/slice", json=test_params)
        res = response.get_data().decode('UTF-8')

        row0 = "id,dtime,farm_id,station_id,parameter_type,parameter_value\n"
        row1 = "3,2023-04-13 14:04:02.340000,ÄÄJ,ST3,Temp3,13.231\n"
        row2 = "6,2023-04-15 10:12:33.920000,MUS,ST2,RGTPress,11.23\n"
        row3 = "8,2023-04-17 17:23:33.920000,ÄÄJ,ST3,Temp1,27.233\n"
        assert res == row0 + row1 + row2 + row3
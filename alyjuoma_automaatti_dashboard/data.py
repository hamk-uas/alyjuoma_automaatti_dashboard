import functools
import datetime

from flask import (
    Blueprint, g, request, jsonify
)


from alyjuoma_automaatti_dashboard.db import get_db

bp = Blueprint('data', __name__, url_prefix='/data')


@bp.route('/write', methods=['POST'])
def write():
    db = get_db()

    data_string = request.data.decode('utf8')
    dtime, farm_id, station_id, parameter_type, parameter_value = data_string.split(';')
    print(dtime, farm_id, station_id, parameter_type, parameter_value)

    dtime = datetime.datetime.strptime(dtime, '%d.%m.%Y %H.%M.%S%f')
    parameter_value = float(parameter_value)

    print(dtime, farm_id, station_id, parameter_type, parameter_value)


    cur = db.cursor()

    cur.execute(
        "INSERT INTO sensor_data (dtime, farm_id, station_id, parameter_type, parameter_value) VALUES (%s, %s, %s, %s, %s)",
        (dtime, farm_id, station_id, parameter_type, parameter_value)
    )

    db.commit()

    return jsonify(
        success=True,
        inserted=[
        dtime,
        farm_id,
        station_id,
        parameter_type,
        parameter_value
        ])


@bp.route('/all', methods=['GET'])
def all():
    db = get_db()
    cur = db.cursor()    

    cur.execute("SELECT * FROM sensor_data")

    result = cur.fetchall()
    data = []

    for line in result:
        data.append({
            "id": line[0],
            "dtime": line[1],
            "farm_id": line[2],
            "station_id": line[3],
            "parameter_type": line[4],
            "parameter_value": line[5]
        })
    
    return jsonify(success=True, result=data)


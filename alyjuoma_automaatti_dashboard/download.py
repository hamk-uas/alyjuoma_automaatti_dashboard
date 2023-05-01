import os
from flask import (
    Blueprint, request, make_response
)

from alyjuoma_automaatti_dashboard.data import (
    data_all, data_slice
)

from alyjuoma_automaatti_dashboard.util import downloadable


bp = Blueprint('download', __name__, url_prefix='/download')

@bp.route('/all', methods=['GET'])
def download_all():
    data = data_all().get_json()
    data = data["result"]

    downloadable(data)
    response = make_response(open('data.csv').read())
    response.headers['Content-Disposition'] = 'attachment; filename=data.csv'
    response.mimetype = 'text/csv'

    os.remove('data.csv')

    return response


@bp.route('/slice', methods=['POST'])
def download_slice():
    req = request.get_json()
    data = data_slice(req).get_json()
    data = data["result"]

    downloadable(data)
    response = make_response(open('data.csv').read())
    response.headers['Content-Disposition'] = 'attachment; filename=data.csv'
    response.mimetype = 'text/csv'

    os.remove('data.csv')

    return response
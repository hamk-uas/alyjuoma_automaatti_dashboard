import os
from flask import (
    Blueprint, request, make_response
)

from alyjuoma_automaatti_dashboard.data import (
    data_all, data_slice
)

from alyjuoma_automaatti_dashboard.util import downloadable

import gzip
import shutil


bp = Blueprint('download', __name__, url_prefix='/download')

@bp.route('/all', methods=['GET'])
def download_all():
    data = data_all().get_json()
    data = data["result"]

    downloadable(data)
    with open('data.csv', 'rb') as f_in, gzip.open('data.csv.gz', 'wb') as f_out:
        shutil.copyfileobj(f_in, f_out)

    response = make_response(open('data.csv.gz', 'rb').read())
    response.headers['Content-Encoding'] = 'gzip'
    response.headers['Content-Disposition'] = 'attachment; filename=data.csv.gz'
    response.mimetype = 'text/csv'

    os.remove('data.csv')

    return response


@bp.route('/slice', methods=['POST'])
def download_slice():
    req = request.get_json()
    data = data_slice(req).get_json()
    data = data["result"]

    downloadable(data)
    with open('data.csv', 'rb') as f_in, gzip.open('data.csv.gz', 'wb') as f_out:
        shutil.copyfileobj(f_in, f_out)

    response = make_response(open('data.csv.gz', 'rb').read())
    response.headers['Content-Encoding'] = 'gzip'
    response.headers['Content-Disposition'] = 'attachment; filename=data.csv.gz'
    response.mimetype = 'text/csv'

    os.remove('data.csv')

    return response
import json
import requests
from flask import Blueprint, request, abort, jsonify

bp = Blueprint('pipelines',
               __name__,
               url_prefix='/pipelines')


def register_pipeline(endpoint, pl):
    """
    Register a pipeline at the specified endpoint.
    It will be available at `/pipelines/<endpoint>`.

    Pipelines must be registered _before_ the app is created!
    """
    def handler():
        data = request.get_json()
        if 'data' not in data:
            abort(400)

        # jsonifying will be a problem, how to coerce into json reliably?
        results = pl(data['data'])
        payload = {
            'results': results
        }
        if 'callback' not in data:
            return jsonify(payload)
        else:
            # TODO to be truly asynchronous, this needs to send the job to a
            # worker
            requests.post(data['callback'], data=json.dumps(payload))
            return '', 202
    bp.add_url_rule(endpoint, pl.name, handler, methods=['POST'])
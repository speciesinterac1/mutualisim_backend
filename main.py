from datetime import datetime
import time
from flask import Flask, json, request, jsonify, Response, make_response
from flask_restful import Api, reqparse
import indisim_mutual as sim
from indisim_mutual import realtime_data
from flask_cors import CORS
import numpy as np
from json import JSONEncoder
from helper import run_simulator, REALTIME_DATA
import os
import shutil


app = Flask(__name__)
api = Api(app)
CORS(app, resources={r"/*": {"origins": "*"}})


@app.route('/run/<sessionid>', methods=['GET', 'POST'])
def run(sessionid):
    path = f'realtime/{sessionid}'
    if os.path.exists(path):
        shutil.rmtree(path)
        os.mkdir(path)
    else:
        os.mkdir(path)

    data = run_simulator(sessionid)
    return data


@app.route('/<sessionid>/stream')
def stream(sessionid):

    def get_data():
        path = os.path.abspath(f'realtime/{sessionid}/realtime_updated.json')
        while path:
            time.sleep(1)
            with open(path, "r") as realtime:
                yield f'data: {realtime.read()}  \n\n'
    resp = Response(get_data(), mimetype='text/event-stream')

    return resp


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000)

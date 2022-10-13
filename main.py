from datetime import datetime
import time
from flask import Flask, json, request, jsonify, Response
from flask_restful import Api, reqparse
import indisim_mutual as sim
from indisim_mutual import realtime_data
from flask_cors import CORS
import numpy as np
from json import JSONEncoder
from helper import run_simulator, REALTIME_DATA

app = Flask(__name__)
api = Api(app)
CORS(app, resources={r"/*": {"origins": "*"}})


@app.route('/run', methods=['GET', 'POST'])
def run():
    data = run_simulator()
    return data


@app.route('/stream')
def stream():

    def get_data():
        while True:
            time.sleep(0.5)
            yield f'data: {realtime_data.currentStatus.return_data()}  \n\n'
    resp = Response(get_data(), mimetype='text/event-stream')

    return resp


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)

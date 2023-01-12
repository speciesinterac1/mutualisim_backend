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

app = Flask(__name__)
api = Api(app)
CORS(app, resources={r"/*": {"origins": "*"}})


@app.route('/run/<sessionid>', methods=['GET', 'POST'])
def run(sessionid):
    try:
        file = os.mkdir(f'realtime/{sessionid}')
    except:
        pass
    with open(f'realtime/{sessionid}/realtime.json', 'w') as fp:
        pass
    with open(f'realtime/{sessionid}/glucose_realtime.json', 'w') as fp:
        pass
    with open(f'realtime/{sessionid}/adenine_realtime.json', 'w') as fp:
        pass
    with open(f'realtime/{sessionid}/lysine_realtime.json', 'w') as fp:
        pass
    data = run_simulator(sessionid)
    return data


@app.route('/<sessionid>/stream')
def stream(sessionid):

    def get_data():
        path = os.path.abspath(f'realtime/{sessionid}/realtime.json')
        while path:
            time.sleep(0.3)
            f = open(path, "r")
            # data = {"population": f.read()}
            yield f'data: {f.read()}  \n\n'
            f.close()
    resp = Response(get_data(), mimetype='text/event-stream')

    return resp


@app.route('/<sessionid>/glucose')
def glucose(sessionid):

    def get_data():
        glucose_path = os.path.abspath(
            f'realtime/{sessionid}/glucose_realtime.json')
        while glucose_path:
            time.sleep(0.3)
            try:
                g = open(glucose_path, "r")
                # data = {"glucose": g.read()}
                yield f'data: {g.read()}  \n\n'
                g.close()
            except:
                yield f'data: {""}  \n\n'
    resp = Response(get_data(), mimetype='text/event-stream')

    return resp


@app.route('/<sessionid>/adenine')
def adenine(sessionid):

    def get_data():
        adenine_path = os.path.abspath(
            f'realtime/{sessionid}/adenine_realtime.json')
        while adenine_path:
            time.sleep(0.3)
            g = open(adenine_path, "r")
            # data = {"adenine": g.read()}
            yield f'data: {g.read()}  \n\n'
            g.close()
    resp = Response(get_data(), mimetype='text/event-stream')

    return resp


@app.route('/<sessionid>/lysine')
def lysine(sessionid):

    def get_data():
        # sessionid = request.args.get('sessionid')
        # print(sessionid)
        lysine_path = os.path.abspath(
            f'realtime/{sessionid}/lysine_realtime.json')
        while lysine_path:
            time.sleep(0.3)
            g = open(lysine_path, "r")
            # data = {"lysine": g.read()}
            yield f'data: {g.read()}  \n\n'
            g.close()
    resp = Response(get_data(), mimetype='text/event-stream')

    return resp


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000)

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
import os

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
        path = os.path.abspath("realtime.json")
        while True:
            time.sleep(0.3)
            f = open(path, "r")
            # data = {"population": f.read()}
            yield f'data: {f.read()}  \n\n'
            f.close()
    resp = Response(get_data(), mimetype='text/event-stream')

    return resp


@app.route('/glucose')
def glucose():

    def get_data():
        glucose_path = os.path.abspath("realtime/glucose_realtime.json")
        while True:
            time.sleep(0.3)
            g = open(glucose_path, "r")
            # data = {"glucose": g.read()}
            yield f'data: {g.read()}  \n\n'
            g.close()
    resp = Response(get_data(), mimetype='text/event-stream')

    return resp


@app.route('/adenine')
def adenine():

    def get_data():
        adenine_path = os.path.abspath("realtime/adenine_realtime.json")
        while True:
            time.sleep(0.3)
            g = open(adenine_path, "r")
            # data = {"adenine": g.read()}
            yield f'data: {g.read()}  \n\n'
            g.close()
    resp = Response(get_data(), mimetype='text/event-stream')

    return resp


@app.route('/lysine')
def lysine():

    def get_data():
        lysine_path = os.path.abspath("realtime/lysine_realtime.json")
        while True:
            time.sleep(0.3)
            g = open(lysine_path, "r")
            # data = {"lysine": g.read()}
            yield f'data: {g.read()}  \n\n'
            g.close()
    resp = Response(get_data(), mimetype='text/event-stream')

    return resp


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000)

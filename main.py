import time
from flask import Flask, Response, send_file
from flask_restful import Api
from flask_cors import CORS
from helper import run_simulator
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


@app.route('/<sessionid>/csv', methods=['GET'])
def download(sessionid):
    path = f'csv/{sessionid}/output.csv'
    return send_file(path, as_attachment=True)


@app.route('/<sessionid>/stream')
def stream(sessionid):

    def get_data():
        # TODO - handle if path does not exist
        path = os.path.abspath(f'realtime/{sessionid}/data.json')
        while path:
            time.sleep(1)
            with open(path, "r") as realtime:
                yield f'data: {realtime.read()}  \n\n'
    resp = Response(get_data(), mimetype='text/event-stream')

    return resp


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000)

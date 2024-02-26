from flask import Flask
from server import defaultState
import json

app = Flask(__name__)


@app.route("/test")
def get_coordinates():
    result = '{"1": 0, "11": 1, "12": 1, "2": 0, "21": 1, "23": 1, "3": 0, "31": 1, "32": 1, "4": 0, "41": 1, "43": 0, "5": 0, "51": 1, "52": 0}'
    return result


@app.route("/default")
def default():
    result = defaultState()
    return json.dump(result)


if __name__ == "__main__":
    app.run()

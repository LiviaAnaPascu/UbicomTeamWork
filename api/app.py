from flask import Flask
from server import box_coordinates
import json

app = Flask(__name__)


@app.route("/test")
def get_coordinates():
    result = '{"1": 0, "11": 0, "12": 0, "2": 0, "21": 0,"22": 1,"23": 0, "3": 0, "31": 0, "32": 0, "4": 0 , "41": 0, "42":1, "43": 0, "51": 0, "52": 0}'
    return result


if __name__ == "__main__":
    app.run()

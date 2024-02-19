from flask import Flask
from server import box_coordinates
import json

app = Flask(__name__)


@app.route("/coordinates")
def get_coordinates():
    result = "TODO"
    return json.dumps(result)


if __name__ == "__main__":
    app.run()

from flask import Flask
from flask_mysqldb import MySQL
from datetime import datetime
import json

 
grid_size = 3

# testJson_string =  '{"1": 0, "11": 0, "12": 0, "2": 0,
#  "21": 0,"22": 1,"23": 0, "3": 0, "31": 0, "32": 0, "4": 0
#  , "41": 0, "42":1, "43": 0, "51": 0, "52": 0}'
# HELPER FUNCTION

def write_to_store(dict_json):
    # Writing to sample.json
    with open("gameset.json", "w") as outfile:
       json.dump(dict_json, outfile)

def generate_box_coordinates():
    box_coords = []
    for i in range(1, grid_size * 2, 2):
        for j in range(1, grid_size, 1):
            if i < grid_size * 2 - 1 and j < grid_size * 4 - 3:
                box_coords.append(
                    [f"{i}{j}", f"{i + 1}{j + 1}", f"{i + 2}{j}", f"{i + 1}{j}"]
                )
    return box_coords


def defaultState():
    box_coordinates = generate_box_coordinates()

    flat_box_coordinates = set(coord for box in box_coordinates for coord in box)

    for i, box in enumerate(box_coordinates):
        flat_box_coordinates.add(f"{i + 1}")

    flat_box_coordinates = list(flat_box_coordinates)
    my_dict = {}
    for index, element in enumerate(flat_box_coordinates):
        my_dict[element] = 0

    return my_dict


app = Flask(__name__)

app.config['MYSQL_HOST'] = 'sql11.freesqldatabase.com'
app.config['MYSQL_USER'] = 'sql11686941'
app.config['MYSQL_PASSWORD'] = '1KtvLJDb4z'
app.config['MYSQL_DB'] = 'flask'
 
mysql = MySQL(app)

@app.route("/test")
def get_coordinates():
    cursor = mysql.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS books_db")
    cursor.execute("SHOW DATABASES")
    now = datetime.now()
    result = '{"1": 0, "11": 1, "12": 1, "2": 0, "21": 1, "23": 1, "3": 0, "31": 1, "32": 1, "4": 0, "41": 1, "43": 0, "5": 0, "51": 1, "52": 0}'
    return result


@app.route("/reset")
def reset_gameboard():
    game = defaultState()
    # Serializing json
    json_object = json.dumps(game, indent=4)
    write_to_store(json_object)
    return json_object
    # with open("gameset.json", "w") as outfile:
    # json.dump(game, outfile)


# @app.route("/gameboard")
# def gameboard():
#     game = defaultState()



# @app.route("/default")
# def default():
#     result = defaultState()
#     return result


if __name__ == "__main__":
    app.run()

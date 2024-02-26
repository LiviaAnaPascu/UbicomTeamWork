#   •  -1,1- • -1,2- •
#   |        |       |
#  2,1      2,2     2,3
#   |        |       |
#   •  -3,1- • -3,2- •
#   |        |       |
#  4,1      4,2     4,3
#   |        |       |
#   •  -5,1- • -5,2- •

# Box 1: [(1, 1), (2, 2), (3, 1), (2, 1)]
# Box 2: [(1, 2), (2, 3), (3, 2), (2, 2)]
# Box 3: [(3, 1), (4, 2), (5, 1), (4, 1)]
# Box 4: [(3, 2), (4, 3), (5, 2), (4, 2)]

grid_size = 3

# testJson_string =  '{"1": 0, "11": 0, "12": 0, "2": 0,
#  "21": 0,"22": 1,"23": 0, "3": 0, "31": 0, "32": 0, "4": 0
#  , "41": 0, "42":1, "43": 0, "51": 0, "52": 0}'


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


def checkBoxes(val, current, player):
    coordinates = generate_box_coordinates()
    for index, box in enumerate(coordinates):
        filtered_items = [
            (key, value) for key, value in current.items() if key in box and value == 1
        ]
        taken_lines = len(filtered_items)

        if taken_lines == 4 and val in box:
            print(f"Last line in box {index + 1} taken by player {player}")

            res = all(ele in box for ele in coordinates[index])
            if res:
                return index + 1  # Return the key of the box


def checkIsGameOver(current):
    coordinates = generate_box_coordinates()
    takenBoxes = 0
    print(current["1"], current["2"], current["3"], current["4"])
    for index, box in enumerate(coordinates):
        box = current[str(index + 1)]
        print(str(index + 1), ": ", box)
        if box != 0:
            takenBoxes += 1
        if takenBoxes == 4:
            return True


def getWinner(player1Score, player2Score):
    if player1Score > player2Score:
        print("Player 1 Wins")
    else:
        print("Player 2 Wins")


def play():
    coordinates = defaultState()
    player1Score = 0
    player2Score = 0

    coordinates["21"] = 1
    coordinates["11"] = 1
    coordinates["22"] = 1
    coordinates["31"] = 1
    coordinates["12"] = 1
    coordinates["23"] = 1
    coordinates["32"] = 1
    coordinates["41"] = 1
    coordinates["43"] = 1
    coordinates["51"] = 1
    coordinates["52"] = 1
    coordinates["2"] = 1
    coordinates["1"] = 1

    print(coordinates)
    currentPlayer = 1
    lastKey = 0

    while True:
        boxCheck = checkBoxes(lastKey, coordinates, currentPlayer)

        print("Player 1's turn.")
        player1Input = input("Enter line coordinates (row,column): ")
        currentPlayer = 1
        for key in coordinates:
            lastKey = key
            if key == player1Input and coordinates[key] == 0:
                coordinates[key] = 1
                boxCheck = checkBoxes(key, coordinates, currentPlayer)
                if boxCheck is not None:
                    coordinates[str(boxCheck)] = 1
                    player1Score += 1

        boxCheck = checkBoxes(lastKey, coordinates, currentPlayer)
        if checkIsGameOver(coordinates) is True:
            getWinner(player1Score, player2Score)
            break

        print("Player 2's turn.")
        player2Input = input("Enter line coordinates (row,column): ")
        currentPlayer = 2
        for key in coordinates:
            lastKey = key
            if key == player2Input and coordinates[key] == 0:
                coordinates[key] = 1
                boxCheck = checkBoxes(key, coordinates, currentPlayer)
                if boxCheck is not None:
                    coordinates[str(boxCheck)] = 2
                    player2Score += 1
        if checkIsGameOver(coordinates) is True:
            getWinner(player1Score, player2Score)
            break

        boxCheck = checkBoxes(lastKey, coordinates, currentPlayer)
        if checkIsGameOver(coordinates) is True:
            getWinner(player1Score, player2Score)
            break


play()

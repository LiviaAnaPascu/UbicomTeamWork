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


def generate_box_coordinates():
    box_coords = []
    for i in range(1, grid_size * 2, 2):
        for j in range(1, grid_size, 1):
            if i < grid_size * 2 - 1 and j < grid_size * 4 - 3:
                box_coords.append([(i, j), (i + 1, j + 1), (i + 2, j), (i + 1, j)])
    return box_coords


box_coordinates = generate_box_coordinates()

for i, box in enumerate(box_coordinates):
    print(f"Box {i + 1}: {box}")


def print_grid_with_dots_and_lines(box_coords):
    flat_box_coordinates = set(coord for box in box_coords for coord in box)
    row = 1

    for i in range(1, grid_size * 2, 1):  # Iterate over rows
        for j in range(1, grid_size, 2):  # Iterate over columns
            coord = (i, j)
            if row % 2 == 1:
                for coords in flat_box_coordinates:
                    if coords[0] == row:
                        print(" - ", end="")
            else:
                for coords in flat_box_coordinates:
                    if coords[0] == row:
                        print("| ", end="")
            row += 1
            print()


print_grid_with_dots_and_lines(box_coordinates)

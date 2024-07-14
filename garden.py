import sys
import itertools


def read_garden(filename):
    with open(filename, 'r') as file:
        garden = [list(line.strip()) for line in file if line.strip()]
    return garden

def read_flowers(filename):
    flowers = []
    with open(filename, 'r') as file:
        for line in file:
            try:
                flower_type, count, min_dist = line.strip().split(',')
                flowers.append((flower_type, int(count), int(min_dist)))
                #print("Flower Rule", flower_type, int(count), int(min_dist))

            except ValueError:
                #print(f"Ignoring Flower line '{line}'")
                pass
    return flowers

# Manhatten distance - abs(DY) + abs(DX)
def distance(x1, x2, y1, y2):
    return abs(x2 - x1) + abs(y2 - y1)

# return list of paired row, column tuples of a given flower
def find_positions_from_type(garden, flower_type):
    positions = [(r, c) for r in range(len(garden)) for c in range(len(garden[0])) if garden[r][c] == flower_type]
    return positions

def find_empty_positions(garden):
    return find_positions_from_type(garden, ' ')

def is_valid_position(garden, row, col, flower_type, min_dist):
    for r in range(len(garden)):
        for c in range(len(garden[0])):
            if garden[r][c] == flower_type:
                manhat_dist = distance(col, c, row, r) 
                if manhat_dist < min_dist: # Distance Rule broken - not valid.
                    return False
    return True

# Nothing fancy here  - just greedily plant at the first free space we can.
def updated_positions_greedy(garden, flower_type, count, min_dist):
    placed = 0
    for row, col in itertools.product(range(len(garden)), range(len(garden[0]))):
        if garden[row][col] == ' ' and is_valid_position(garden, row, col, flower_type, min_dist):
            placed += 1
            garden[row][col] = flower_type  # plant flower
            if placed == count:
                return True
    return False

# TODO
def update_positions_backtrack(garden, flower_type, count, min_dist):
    raise NotImplementedError("Not Implemented Planting Strategy")

#def backtrack(garden, flowers, index, positions):
#    if index == len(flowers):
#        return True
#    flower_type, count, min_dist = flowers[index]
#    for row, col in itertools.product(range(len(garden)), range(len(garden[0]))):
#            positions.append((row, col))
#        if garden[row][col] == ' ' and is_valid_position(garden, row, col, flower_type, min_dist, positions):
#            garden[row][col] = flower_type
#            if len(positions) % count == 0:
#                if backtrack(garden, flowers, index + 1, positions):
#                    return True
#            elif backtrack(garden, flowers, index, positions):
#                return True
#            positions.pop()
#            garden[row][col] = ' '
#    return False

def plant_flowers(garden, flowers):
    plant_strategy = updated_positions_greedy
#    plant_strategy = update_positions_backtrack

    for flower_type, count, min_dist in flowers:
        planted = plant_strategy(garden, flower_type, count, min_dist)
        if not planted:
            print(f"Unable to plant all flowers of type: {flower_type}")
            return False
    return True


def print_constraints(flowers):
    for _ in flowers:
        print(_)

def print_garden(garden):
    for row in garden:
        print(''.join(row))


def validate_garden(garden, flowers):
    valid = True
    # For each flower - make sure we fullfil our number quoto and distance constraints
    for flower_type, count, min_dist in flowers:
        positions = find_positions_from_type(garden, flower_type)

        if len(positions) != count:
            print(f"Error: Expected {count} flowers of type '{flower_type}', but found {len(positions)}.")
            valid = False
        for i in range(len(positions)):
            for j in range(i + 1, len(positions)):
                r1, c1 = positions[i]
                r2, c2 = positions[j]
                if distance(c1, c2, r1, r2) < min_dist:
                    print(f"Error: Flowers of type '{flower_type}' at positions ({r1},{c1}) and ({r2},{c2}) are too close.")
                    valid = False
    return valid

def main():
    if len(sys.argv) != 3:
        print("Usage: python garden.py <garden_file> <flowers_file>")
        return

    garden_file = sys.argv[1]
    flowers_file = sys.argv[2]

    garden = read_garden(garden_file)
    flowers = read_flowers(flowers_file)

    print("\nUnplanted garden")
    print_garden(garden)
    print("\nRules")
    print_constraints(flowers)

    if plant_flowers(garden, flowers):
        print("\nFinshed! Our designed garden")
        print_garden(garden)
        if validate_garden(garden, flowers):
            print("Nice!")
        else:
            print("The garden is invalid.")
    else:
        print("Failed to plant all flowers according to the constraints.")

if __name__ == "__main__":
    main()


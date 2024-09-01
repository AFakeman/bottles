from pprint import pprint
import argparse
import sys

def copy_bottles(bottles):
    return [[c for c in bottle] for bottle in bottles]


def get_top_color(bottle):
    for idx in range(len(bottle) - 1, 0, -1):
        if bottle[idx] != ' ':
            return bottle[idx]
    return bottle[0]


def string_to_bottle(string):
    bottle = [c for c in string]
    assert(len(bottle) <= 4)
    if len(bottle) < 4:
        bottle += [' ' for i in range(len(bottle), 4)]
    return bottle


def read_bottles_stdin(num_bottles, reverse=False):
    bottles = []

    for bottle_idx in range(num_bottles):
        bottle_str = input(f"Enter bottle {bottle_idx} contents: ")
        if reverse:
            bottle_str = bottle_str[::-1]
        bottles.append(string_to_bottle(bottle_str))

    return bottles


def read_bottles_file(num_bottles, filename, reverse=False):
    bottles = []

    if filename != '-':
        with open(filename) as f:
            for line in f:
                bottles.append(string_to_bottle(line[:-1]))
    else:
        for line in sys.stdin:
            bottles.append(string_to_bottle(line[:-1]))

    if len(bottles) > num_bottles:
        raise ValueError("Too many lines provided!")

    if len(bottles) < num_bottles:
        bottles += [[] for i in range(num_bottles - len(bottles))]

    return bottles


def is_solved(bottles):
    for bottle in bottles:
        if not is_full_bottle(bottle):
            return False
    return True


def is_full_bottle(bottle):
    return all(map(lambda x: x == bottle[0], bottle))


def validate_bottles(bottles):
    colors = {}
    for bottle in bottles:
        for bottle_layer in bottle:
            if bottle_layer == ' ':
                continue
            colors.setdefault(bottle_layer, 0)
            colors[bottle_layer] += 1

    for color, count in colors.items():
        if count != 4:
            raise ValueError(f"Color '{color}' has '{count}' total layers")


def bottle_pour(source, dest):
    source_idx = 3
    source_free = 0
    while source_idx >= 0 and source[source_idx] == ' ':
        source_idx -= 1
        source_free += 1

    color = source[source_idx]

    max_movable = 0

    while source_idx >= 0 and source[source_idx] == color:
        source_idx -= 1
        max_movable += 1

    dest_free = sum(color == ' ' for color in dest)
    to_move = min(max_movable, dest_free)

    source_idx = 4 - 1 - source_free
    dest_idx = 4 - dest_free

    for _ in range(to_move):
        source[source_idx] = ' '
        dest[dest_idx] = color
        source_idx -= 1
        dest_idx += 1


def list_available_turns(bottles):
    bottle_candidates = [idx for idx in range(len(bottles)) if bottles[idx][-1] == ' ']
    top_colors = [get_top_color(bottle) for bottle in bottles]

    for source_idx, source in enumerate(bottles):
        if (is_full_bottle(source)):
            continue
        top_color = top_colors[source_idx]
        for dest_idx in bottle_candidates:
            if dest_idx == source_idx:
                continue
            if (top_colors[dest_idx] != ' ' and top_colors[dest_idx] != top_color):
                continue
            # Pour one bottle into another
            new_bottles = copy_bottles(bottles)
            bottle_pour(new_bottles[source_idx], new_bottles[dest_idx])
            yield new_bottles


# Algorithm is recusive. Python has a 1000 depth limit, but the solutions are
# normally short, so if we hit it, it's likely a reason to check if the algo is
# looping somewhere.
def solve(bottles, parents=list()):
    validate_bottles(bottles)
    for candidate in list_available_turns(bottles):
        if candidate in parents:
            continue
        if is_solved(candidate):
            return [bottles, candidate]
        else:
            solution = solve(candidate, parents + [bottles])
            if solution is None:
                continue
            return [bottles] + solution
    return None


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('command', choices=["solve", "list-moves"], default="solve")
    parser.add_argument('-n', '--num-bottles')
    parser.add_argument('-i', '--input-file')
    parser.add_argument('-r', '--reverse', action='store_true')

    args = parser.parse_args()

    if args.num_bottles is None:
        num_bottles = int(input("Enter the number of bottles: "))
    else:
        num_bottles = int(args.num_bottles)

    if args.input_file is None:
        bottles = read_bottles_stdin(num_bottles, args.reverse)
    else:
        bottles = read_bottles_file(num_bottles, args.input_file, args.reverse)

    validate_bottles(bottles)

    if args.command == "solve":
        pprint(solve(bottles))
    elif args.command == "list-moves":
        pprint(list(list_available_turns(bottles)))

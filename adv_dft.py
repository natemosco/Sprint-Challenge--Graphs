from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph = literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []

"""
new room? make new entry: {0: {"n": "*", "s": "*", "e": "*", "w": "*"}}
add all unexplored paths to stack
?identify the rm id's before exploring?  {0: {"n": "4", "s": "8", "e": "1", "w": "3"}}
pop off the stack == call recursion
"""


def get_opposite(direction):
    opposite = 'letter'
    if direction == 'n':
        opposite = 's'
    elif direction == 's':
        opposite = 'n'
    elif direction == 'w':
        opposite = 'e'
    elif direction == 'e':
        opposite = 'w'
    return opposite


def dft(visited=None, temp_path=None, prev=None):
    room = player.current_room
    visited = {} if visited is None else visited
    temp_path = [] if temp_path is None else temp_path

    if room.id not in visited:
        visited[room.id] = {}
        for cardinal_direction in room.get_exits():
            visited[room.id][cardinal_direction] = "*"
        if prev is not None:
            from_direction = get_opposite(prev)
            from_id = room.get_room_in_direction(from_direction).id
            visited[room.id][from_direction] = from_id
    if len(visited) == 500:
        return

    for direction, rm_id in visited[room.id].items():
        if rm_id == "*":
            id_in_this_direction = room.get_room_in_direction(direction).id
            visited[room.id][direction] = id_in_this_direction

            traversal_path.append(direction)
            player.travel(direction)
            dft(visited, direction)
    if "*" not in visited[room.id]:
        player.travel(get_opposite(prev))
        traversal_path.append(get_opposite((prev)))


dft()
# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
print("after Here:\n", player.current_room,
      "RIGHT HERE!!!", "type:", type(player.current_room))
print(player.current_room.id)
print(player.current_room.get_exits())
print(player.current_room.get_room_in_direction('s').id)
print(player.travel('s'))
print(player.current_room.get_room_in_direction('n').id, "type:",
      type(player.current_room.get_room_in_direction('n').id))
print(player.current_room.id, "p.cur.id")
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(
        f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")


#######
# UNCOMMENT TO WALK AROUND
#######
player.current_room.print_room_description(player)
while True:
    cmds = input("-> ").lower().split(" ")
    if cmds[0] in ["n", "s", "e", "w"]:
        player.travel(cmds[0], True)
    elif cmds[0] == "q":
        break
    else:
        print("I did not understand that command.")

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
# ! this function can be replaced with room.get_room_in_direction('n').id


def bfs():

    player.current_room = world.starting_room
    # queue = []
    # queue.append([player.current_room])
    visited = {}
    my_traversal_path = []
    while len(visited) < 500:
        print(len(visited), "visited")
        # room = queue.pop(0)
        room = player.current_room
        exits = room.get_exits()  # *{0: [n,s,e,w]}

        if room.id not in visited:
            visited[room.id] = {}
            for cardinal_direction in exits:
                visited[room.id][cardinal_direction] = "*"
                # *visited = {0: {"n": "*", "s": "*", "e": "*", "w": "*"}}
        if len(my_traversal_path) > 0:
            previous = get_opposite(my_traversal_path[-1])
            visited[room.id][previous] = room.get_room_in_direction(
                previous).id

        for cardinal_direction in exits:
            # have all exits been visited before?
            if "*" not in visited[room.id].values():
                back_track_to_smallest_id = ('cardinal_direction', 501)
                for key_value in visited[room.id].items():
                    if key_value[1] < back_track_to_smallest_id[1]:
                        back_track_to_smallest_id = key_value
                my_traversal_path.append(back_track_to_smallest_id[0])
                player.travel(back_track_to_smallest_id[0])
                break
            elif visited[room.id][cardinal_direction] == "*":
                next_rm_id = room.get_room_in_direction(cardinal_direction).id

                # replace  "n": "*" with "n": "8"
                visited[room.id][cardinal_direction] = next_rm_id
                my_traversal_path.append(cardinal_direction)
                player.travel(cardinal_direction)
                break

    # print(len(my_traversal_path), "my_traversal_path")
    global traversal_path
    traversal_path = my_traversal_path


bfs()

# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
print("after Here:\n", player.current_room,
      "RIGHT HERE!!!", "type:", type(player.current_room))
print(player.current_room.id)
print(player.current_room.get_exits())
print(player.current_room.get_room_in_direction('s').id)
print(player.travel('s'))
print(player.current_room.get_room_in_direction('n').id)
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

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


def dfs():

    player.current_room = world.starting_room
    # queue = []
    # queue.append([player.current_room])
    visited = {}
    my_traversal_path = []
    prev_room = None  # ?(get_opposite(largest_next_room[0]), prev_rm_id)
    while len(visited) < 500:

        # print(len(visited), "visited")
        if len(my_traversal_path) == 539:
            with open("./my_path.txt", "w") as path:
                for location in my_traversal_path:
                    path.write(f"{location}\n")
            path.close()

        # room = queue.pop(0)
        room = player.current_room
        exits = room.get_exits()  # *{0: [n,s,e,w]}

        if room.id not in visited:
            visited[room.id] = {}
            for cardinal_direction in exits:
                visited[room.id][cardinal_direction] = "*"
                # * FIRST PASS visited = {0: {"n": "*", "s": "*", "e": "*", "w": "*"}}
                # * SECOND PASS visited = {
                # *                          0: {"n": "*", "s": 8, "e": "*", "w": "*"}
                # *                          8: {"n": "*", "w": "*"}}
                # ? "*" == unvisited:
            if prev_room is not None:
                visited[room.id][prev_room[0]] = prev_room[1]
                # * SECOND PASS visited = {
                # *                          0: {"n": "*", "s": 8, "e": "*", "w": "*"}
                # *                          8: {"n": "0", "w": "*"}}

        # have all exits been visited before?
        if room.id == 0 and "*" not in visited[0].values():
            """
            *if you're back at 0 (starting point) and havent hit all 500 rooms. first
            *check visited path to identify a gap
            ?then find path to the gap
            *go there and continue with traversal
            """
            unvisited = ('direction', 501)
            for room_id in visited:
                if "*" in visited[room_id].values():
                    unvisited = ('direction', room_id)

            path_to_unvisited = []
            back_to_zero = False
            while not back_to_zero:
                for pair in visited[unvisited[1]].items():
                    if pair[1] == "*":
                        continue
                    if pair[1] < unvisited[1]:
                        unvisited = pair
                    if pair[1] == 0:
                        back_to_zero = True
                path_to_unvisited.insert(0, get_opposite(unvisited[0]))

            for direction in path_to_unvisited:
                player.travel(direction)
                my_traversal_path.append(
                    (direction, room.get_room_in_direction(direction)))
        elif "*" not in visited[room.id].values():
            back_track_to_smallest_id = ('cardinal_direction', 501)
            for key_value in visited[room.id].items():
                if key_value[1] < back_track_to_smallest_id[1]:
                    back_track_to_smallest_id = key_value
            my_traversal_path.append(
                (back_track_to_smallest_id[0], back_track_to_smallest_id[1]))
            player.travel(back_track_to_smallest_id[0])

        else:
            largest_next_room = ('some_direction', -10)

            # [('n':'*'), ('s':*), ('e':'*'), ('w':*)]
            for key_value in visited[room.id].items():
                if key_value[1] == "*":
                    unvisited_room_id = room.get_room_in_direction(
                        key_value[0]).id  # * evals to [('n':'4'), ('s':8), ('e':'1'), ('w':3)]
                    if unvisited_room_id > largest_next_room[1]:
                        largest_next_room = (key_value[0], unvisited_room_id)
            # replace  "n": "*" with "n": "8"
            visited[room.id][largest_next_room[0]] = largest_next_room[1]
            # store values of previous room (dir_i_came_from, prev_rm_id)

            prev_rm_id = int(room.id)
            prev_room = (get_opposite(largest_next_room[0]), prev_rm_id)
            # * go to next room and add to traversal_path
            my_traversal_path.append(largest_next_room)
            player.travel(largest_next_room[0])

    global traversal_path
    for pair in my_traversal_path:
        traversal_path.append(pair[0])


dfs()

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

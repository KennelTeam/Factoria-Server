import Room


free_ids = set(list(range(1, 100)))
rooms = {}


def create_room(client, nickname):
    if len(free_ids) > 0:
        id = next(iter(free_ids))
        free_ids.remove(id)
        rooms[id] = Room.Room(id, client, nickname)
        return id
    else:
        return -1


def close_room(room_id):
    for client in rooms[room_id].clients:
        if client is not None:
            client.send({'message_type': 'room_closed'})
    rooms.pop(room_id)
    free_ids.add(room_id)


def connect_to_room(id, client, nickname):
    print("connect to room {}".format(id))
    if id in rooms.keys():
        return rooms[id].connect_to_room(client, nickname)
    else:
        return False

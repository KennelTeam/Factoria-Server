import threading
import json
import RoomManager


BUFFER_SIZE = 1024


class ClientProcessor(threading.Thread):
    address = ('', 0)
    connection = None
    nickname = ''
    room_id = -1
    client_id = -1
    running = False

    def __init__(self, address, connection):
        threading.Thread.__init__(self)
        self.address = address
        self.connection = connection
        self.nickname = ""
        self.room_id = -1
        self.client_id = -1
        self.running = False

    def send(self, data):
        self.connection.sendall(json.dumps(data, ensure_ascii=False).encode('utf-8'))

    def process(self, data):
        print(data)

        data = data.decode('utf-8')

        print(data)
        data = json.loads(data)

        print(data)

        message_type = data['message_type']
        if message_type == 'connect_to_room':
            self.room_id = data['room_id']
            self.nickname = data['nickname']
            result = RoomManager.connect_to_room(self.room_id, self, self.nickname)
            if result:
                self.client_id = 1
            response = {'status': result, 'message_type': 'response'}

            self.send(response)
        elif message_type == 'create_room':
            self.nickname = data['nickname']
            self.room_id = RoomManager.create_room(self, self.nickname)
            response = {'room_id': self.room_id, 'message_type': 'room_created'}
            if self.room_id != -1:
                self.client_id = 0
            self.send(response)

        elif message_type == 'leave_room':
            if self.room_id != -1 and self.room_id in RoomManager.rooms.keys():
                RoomManager.rooms[self.room_id].exit(self.client_id)
                result = True
            else:
                result = False
            self.send({'status': result, 'message_type': 'response'})
            if self.client_id == 0:
                RoomManager.close_room(self.room_id)
            if result:
                self.running = False

        elif message_type == 'answer':
            answer = data['answer']
            if self.room_id != -1 and RoomManager.rooms[self.room_id].game is not None:
                result = RoomManager.rooms[self.room_id].game.answer_question(self.client_id, answer)
            else:
                result = False
            if result:
                question, number = RoomManager.rooms[self.room_id].game.get_question(self.client_id)
                if question is not None:
                    self.send({'message_type': 'question', 'variants': question, 'number': number})
            self.send({'status': result, 'message_type': 'response'})

        elif message_type == 'start_game':
            if self.room_id != -1:
                if RoomManager.rooms[self.room_id].game is not None:
                    response = {'status': False, 'message_type': 'response'}
                else:
                    result = RoomManager.rooms[self.room_id].start_game()
                    response = {'status': result, 'message_type': 'response'}
            else:
                response = {'status': False, 'message_type': 'response'}
            self.send(response)

    def run(self):
        self.running = True
        with self.connection:
            while self.running:
                data = self.connection.recv(BUFFER_SIZE)
                if not data:
                    self.running = False
                self.process(data)

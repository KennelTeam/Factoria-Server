import threading
import json
import RoomManager
import socket
import errno
import time


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

    def process_error(self, error):
        self.running = False
        if error.errno == errno.ECONNRESET:
            self.leave_room()
        else:
            print("Unexpected error!!")
            print(str(e))

    def send(self, data, isPriority=True):
        for key in data.keys():
            data[key] = str(data[key])
        try:
            self.connection.sendall(json.dumps(data, ensure_ascii=False).encode('utf-8'))
        except socket.error as e:
            if isPriority:
                self.process_error(e)

    def connect_to_room(self, room_id, nickname):
        self.room_id = room_id
        self.nickname = nickname
        result = RoomManager.connect_to_room(self.room_id, self, self.nickname)
        if result:
            self.client_id = 1
        return result

    def create_room(self, nickname):
        self.nickname = nickname
        self.room_id = RoomManager.create_room(self, self.nickname)

        response = {'room_id': self.room_id, 'message_type': 'room_created'}
        if self.room_id != -1:
            self.client_id = 0

        return response

    def leave_room(self):
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

    def answer(self, answer):
        if self.room_id != -1 and RoomManager.rooms[self.room_id].game is not None:
            result = RoomManager.rooms[self.room_id].game.answer_question(self.client_id, answer)
        else:
            result = False

        return result

    def start_game(self):
        if RoomManager.rooms[self.room_id].game is not None:
            response = {'status': False, 'message_type': 'response'}
        else:
            result = RoomManager.rooms[self.room_id].start_game()
            response = {'status': result, 'message_type': 'response'}
        return response

    def get_question(self):
        print("get question")
        if RoomManager.rooms[self.room_id].game is not None:
            question, number = RoomManager.rooms[self.room_id].game.get_question(self.client_id)
            print(question, number)
            if question is not None:
                time.sleep(0.5)
                self.send({'message_type': 'question', 'variants': question, 'number': number})

    def process(self, data):
        try:
            data = data.decode('utf-8')
            data = json.loads(data)
            print(data)
            message_type = data['message_type']
        except Exception as e:
            return

        if message_type == 'connect_to_room':
            print("connect to room")
            if 'room_id' not in data.keys() or 'nickname' not in data.keys():
                result = False
            else:
                result = self.connect_to_room(int(data['room_id']), data['nickname'])
            response = {'status': result, 'message_type': 'response'}
            self.send(response)
        elif message_type == 'create_room':
            if 'nickname' in data.keys():
                response = self.create_room(data['nickname'])
            else:
                response = {'room_id': -1, 'message_type': 'room_created'}
            self.send(response)

        elif message_type == 'leave_room':
            self.leave_room()

        elif message_type == 'answer':
            if 'answer' not in data.keys():
                result = False
            else:
                result = self.answer(data['answer'])

            self.send({'status': result, 'message_type': 'response'})

        elif message_type == 'start_game':
            if self.room_id != -1:
                response = self.start_game()
            else:
                response = {'status': False, 'message_type': 'response'}
            self.send(response)
        elif message_type == "get_question":
            if self.room_id != -1:
                self.get_question()
                response = {'status': True, 'message_type': 'response'}
            else:
                response = {'status': False, 'message_type': 'response'}
            self.send(response)


    def run(self):
        self.running = True
        with self.connection:
            while self.running:
                try:
                    data = self.connection.recv(BUFFER_SIZE)
                except socket.error as e:
                    self.process_error(e)
                    break
                if not data:
                    self.running = False
                self.process(data)
        self.leave_room()

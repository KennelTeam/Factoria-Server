import Game
import time


EMPTY_CLIENT = None


class Room:
    clients = [EMPTY_CLIENT, EMPTY_CLIENT]
    game = None
    nicknames = ['', '']
    id = 0

    def __init__(self, id, initiator, nickname):

        self.clients = [EMPTY_CLIENT, EMPTY_CLIENT]
        self.clients[0] = initiator
        self.id = id
        self.nicknames = ['', '']
        self.nicknames[0] = nickname
        self.game = None

    def on_player_finished(self, player_id):
        if self.clients[1 - player_id] == EMPTY_CLIENT or self.game.client_finish_time[1 - player_id] != -1:
            self.clients[player_id].send({'message_type': 'finished', 'results': self.get_results()})
            if self.clients[1 - player_id] is not None:
                self.clients[1 - player_id].send({'message_type': 'finished', 'results': self.get_results()})
            self.game = None

    def on_player_answered(self, player_id):
        message = {
            'message_type': 'answer_info',
            'answered_player': self.nicknames[player_id]
        }

        print(self.clients)

        self.clients[0].send(message)
        self.clients[1].send(message)

    def on_player_mistaken(self, player_id):
        message = {
            'message_type': 'mistake_info',
            'mistaken_player': self.nicknames[player_id]
        }

        self.clients[0].send(message)
        self.clients[1].send(message)

    def start_game(self):
        print(self.clients)
        print(self.id)
        if self.clients[1] is not None:
            self.game = Game.Game(self.on_player_answered, self.on_player_mistaken, self.on_player_finished)

            message = {
                'message_type': 'start_game',
                'dividers_count': len(self.game.dividers)
            }
            print(message)
            # print(self.clients)

            self.clients[0].send(message)
            self.clients[1].send(message)
            print("sending questions")
            return True
        else:
            return False

    def connect_to_room(self, client, nickname):
        print("connect to room")
        print(client, nickname)
        if self.clients[1] is None:
            self.clients[1] = client
            self.nicknames[1] = nickname
            print("connected")

            self.clients[0].send({'message_type': "connected_player", "nickname": nickname})
            self.clients[1].send({'message_type': 'connected_player', "nickname": self.nicknames[0]})
            print("clients are notified")
            time.sleep(0.5)
            print(self.clients)
            return True
        else:
            return False

    def exit(self, client_id):
        print("disconnected player {}".format(client_id))
        if self.clients[1 - client_id] is not None:
            self.clients[1 - client_id].send({'message_type': 'disconnected_player', 'nickname': self.nicknames[client_id]}, isPriority=False)
        self.clients[client_id] = EMPTY_CLIENT
        self.nicknames[client_id] = ''

    def get_results(self):
        return {
            self.nicknames[0]: str({
                'mistakes': str(self.game.client_mistakes[0]),
                'progress': str(self.game.client_progress[0]),
                'time': str(self.game.client_finish_time[0] - self.game.begin_time)
            }),
            self.nicknames[1]: str({
                'mistakes': str(self.game.client_mistakes[1]),
                'progress': str(self.game.client_progress[1]),
                'time': str(self.game.client_finish_time[1] - self.game.begin_time)
            })
        }

import Game
import time
from enum import Enum
import RoomManager


class FinishReason(Enum):
    WON = 1
    DISCONNECTED = 2


class Room:
    clients = [None, None]
    game = None
    nicknames = ['', '']
    id = 0

    def __init__(self, id, initiator, nickname):

        self.clients = [None, None]
        self.clients[0] = initiator
        self.id = id
        self.nicknames = ['', '']
        self.nicknames[0] = nickname
        self.game = None

    def on_player_finished(self, player_id):
        self.finish_game(FinishReason.WON, player_id)

    def on_player_answered(self, player_id):
        print('Answered')
        message = {
            'message_type': 'answer_info',
            'answered_player': self.nicknames[player_id]
        }

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
        if self.clients[1] is not None:
            self.game = Game.Game(
                self.on_player_answered, self.on_player_mistaken, self.on_player_finished)

            message = {
                'message_type': 'start_game',
                'dividers_count': len(self.game.dividers)
            }

            self.clients[0].send(message)
            self.clients[1].send(message)
            return True
        else:
            return False

    def connect_to_room(self, client, nickname):
        if self.clients[1] is None:
            self.clients[1] = client
            self.nicknames[1] = nickname

            self.clients[0].send(
                {'message_type': "connected_player", "nickname": nickname})
            self.clients[1].send(
                {'message_type': 'connected_player', "nickname": self.nicknames[0]})
            time.sleep(0.5)
            return True
        else:
            return False

# Oh my bug...  When client joins the rooms he deifnitely becomes player number 1
# However either client number 1 or number 0 may disconnect
# Oh, looks like there is a crutch and ClientProcessor checks
# wheter the host is leaving room and if so closes the room
    def exit(self, client_id):
        print('Exit called', client_id)
        self.finish_game(FinishReason.DISCONNECTED, client_id)

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

    def finish_game(self, reason: FinishReason, player_id):
        if reason == FinishReason.WON:
            for i, client in enumerate(self.clients):
                if client is not None:
                    if player_id == i:
                        msg = 'You win!'
                    else:
                        msg = 'You loose'
                    client.send(
                        {'message_type': 'result', 'result': msg})
        elif reason == FinishReason.DISCONNECTED:
            client = self.clients[1 - player_id]
            if client is not None:
                client.send({
                    'message_type': 'result', 'result': 'Other player has disconnected'
                })

        RoomManager.close_room(self.id)

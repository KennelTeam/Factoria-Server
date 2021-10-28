import Game


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
        if self.clients[1] is not None:
            self.game = Game.Game(self.on_player_answered, self.on_player_mistaken, self.on_player_finished)

            message = {
                'message_type': 'start_game',
                'dividers_count': len(self.game.dividers)
            }

            # print(self.clients)

            self.clients[0].send(message)
            self.clients[1].send(message)

            # print("therethere")
            question0, number0 = self.game.get_question(0)
            self.clients[0].send({'message_type': 'question', 'variants': question0, 'number': number0})

            question1, number1 = self.game.get_question(1)
            self.clients[1].send({'message_type': 'question', 'variants': question1, 'number': number1})
            return True
        else:
            return False

    def connect_to_room(self, client, nickname):
        if self.clients[1] is None:
            self.clients[1] = client
            self.nicknames[1] = nickname

            self.clients[0].send({'message_type': "connected_player", "nickname": nickname})
            self.clients[1].send({'message_type': 'connected_player', "nickname": self.nicknames[0]})
            return True
        else:
            return False

    def exit(self, client_id):
        self.clients[1 - client_id].send({'message_type': 'disconnected_player', 'nickname': self.nicknames[client_id]})

        self.clients[client_id] = EMPTY_CLIENT
        self.nicknames[client_id] = ''

    def get_results(self):
        return {
            self.nicknames[0]: {
                'mistakes': self.game.client_mistakes[0],
                'progress': self.game.client_progress[0],
                'time': self.game.client_finish_time[0] - self.game.begin_time
            },
            self.nicknames[1]: {
                'mistakes': self.game.client_mistakes[1],
                'progress': self.game.client_progress[1],
                'time': self.game.client_finish_time[1] - self.game.begin_time
            }
        }

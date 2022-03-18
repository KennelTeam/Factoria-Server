import time
import random

EASY_PRIMES = [2, 3, 5, 7, 11, 13]
MEDIUM_PRIMES = [17, 19, 23, 29, 31, 37]
HARD_PRIMES = [37, 41, 43, 47, 59, 61]

ALL_PRIMES = [HARD_PRIMES, MEDIUM_PRIMES, EASY_PRIMES]


def generate_dividers(hard_primes_count=1, medium_primes_count=2, easy_primes_count=4):
    dividers = [[], [], []]
    number = 1
    for i in range(hard_primes_count):
        dividers[0].append(random.choice(HARD_PRIMES))
    for i in range(medium_primes_count):
        dividers[1].append(random.choice(MEDIUM_PRIMES))
    for i in range(easy_primes_count):
        dividers[2].append(random.choice(EASY_PRIMES))

    for d in dividers:
        for div in d:
            number *= div

    return dividers, number


class Game:
    def __init__(self, answer_callback, mistake_callback, finish_callback):
        self.answer_callback = answer_callback
        self.mistake_callback = mistake_callback
        self.finish_callback = finish_callback

        self.client_progress = [[2, 0], [2, 0]]
        self.client_finish_time = [-1, -1]
        self.client_mistakes = [0, 0]
        self.begin_time = time.time()
        self.dividers, self.number = generate_dividers()
        self.client_numbers = [self.number, self.number]
        for i in range(3):
            random.shuffle(self.dividers[i])

    def get_question(self, player_id):
        dividers_begin_index = self.client_progress[player_id]

        if dividers_begin_index[0] == len(self.dividers):
            return None, 1

        variants = [self.dividers[self.client_progress[player_id][0]][self.client_progress[player_id][1]]]
        while len(variants) < 3:
            variant = random.choice(ALL_PRIMES[self.client_progress[player_id][0]])
            if self.client_numbers[player_id] % variant != 0:
                variants.append(variant)
        return variants, self.client_numbers[player_id]

    def answer_question(self, player_id, divider, points_me, points_enemy):
        if divider == self.dividers[self.client_progress[player_id][0]][self.client_progress[player_id][1]]:
            self.client_numbers[player_id] //= self.dividers[self.client_progress[player_id][0]]\
                [self.client_progress[player_id][1]]
            self.client_progress[player_id][1] += 1
            if self.client_progress[player_id][1] == len(self.dividers[self.client_progress[player_id][0]]):
                self.client_progress[player_id][0] -= 1
                self.client_progress[player_id][1] = 0
            self.answer_callback(player_id)

            if self.client_numbers[player_id] == 1:
                print('Yeah it\'s finish')
                self.client_finish_time[player_id] = time.time()
                if points_me > points_enemy:
                    self.finish_callback(player_id)
                else:
                    self.finish_callback(1 - player_id)

            return True
        else:
            self.client_mistakes[player_id] += 1
            self.mistake_callback(player_id)
            return False

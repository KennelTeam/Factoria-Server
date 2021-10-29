import time
import random

EASY_PRIMES = [2, 3, 5, 7]
MEDIUM_PRIMES = [11, 13, 17, 19, 23, 29, 31]
HARD_PRIMES = [37, 41, 43, 47, 59, 61]

ALL_PRIMES = EASY_PRIMES + MEDIUM_PRIMES + HARD_PRIMES


def generate_dividers(hard_primes_count=1, medium_primes_count=1, easy_primes_count=3):
    dividers = []
    number = 1
    for i in range(hard_primes_count):
        dividers.append(random.choice(HARD_PRIMES))
    for i in range(medium_primes_count):
        dividers.append(random.choice(MEDIUM_PRIMES))
    for i in range(easy_primes_count):
        dividers.append(random.choice(EASY_PRIMES))

    for d in dividers:
        number *= d

    return dividers, number


class Game:
    def __init__(self, answer_callback, mistake_callback, finish_callback):
        self.answer_callback = answer_callback
        self.mistake_callback = mistake_callback
        self.finish_callback = finish_callback

        self.client_progress = [0, 0]
        self.client_finish_time = [-1, -1]
        self.client_mistakes = [0, 0]
        self.begin_time = time.time()
        self.dividers, self.number = generate_dividers()
        self.client_numbers = [self.number, self.number]
        random.shuffle(self.dividers)

    def get_question(self, player_id):
        # print("there")
        dividers_begin_index = self.client_progress[player_id]

        if dividers_begin_index == len(self.dividers):
            return None, 1

        variants = []
        var1 = random.choice(ALL_PRIMES)
        while var1 in self.dividers[dividers_begin_index:]:
            var1 = random.choice(ALL_PRIMES)
        variants.append(var1)
        # print("there2")
        var2 = random.choice(ALL_PRIMES)
        while var2 in self.dividers[dividers_begin_index:] + [var1]:
            var2 = random.choice(ALL_PRIMES)
        # print("there3")
        variants.append(var2)
        variants.append(self.dividers[dividers_begin_index])
        random.shuffle(variants)
        return variants, self.client_numbers[player_id]

    def answer_question(self, player_id, divider):
        if divider == self.dividers[self.client_progress[player_id]]:
            self.client_numbers[player_id] //= self.dividers[self.client_progress[player_id]]
            self.client_progress[player_id] += 1
            self.answer_callback(player_id)

            if self.client_progress[player_id] == len(self.dividers):
                self.client_finish_time[player_id] = time.time()
                self.finish_callback(player_id)
            return True
        else:
            self.client_mistakes[player_id] += 1
            self.mistake_callback(player_id)
            return False


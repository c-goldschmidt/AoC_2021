import copy
import itertools
from functools import lru_cache

from day import Day


class GameEnd(StopIteration):
    pass


class Player:
    def __init__(self, pos):
        self.pos = pos - 1
        self.score = 0
        self.max_score = 1000

    def __hash__(self):
        return hash((self.score, self.pos))

    def move(self, dies):
        dies = sum(dies)

        self.pos = (self.pos + dies) % 10
        self.score += self.pos + 1

        if self.score >= self.max_score:
            raise GameEnd()


class Day21(Day):
    all_rolls = [sum(die) + 3 for die in itertools.product(range(3), range(3), range(3))]

    def parse(self, content):
        return [Player(int(line[-1])) for line in super().parse(content)]

    def _roll(self, i):
        dies = []
        for _ in range(3):
            dies.append(i)
            i = 1 if i == 100 else i + 1

        return i, dies

    def part1(self):
        p1 = copy.deepcopy(self.input[0])
        p2 = copy.deepcopy(self.input[1])
        i = 1
        rolls = 0

        while True:
            try:
                i, dies = self._roll(i)
                rolls += 3
                p1.move(dies)

                i, dies = self._roll(i)
                rolls += 3
                p2.move(dies)
            except GameEnd:
                lost = p2 if p1.score >= 1000 else p1
                return rolls * lost.score

    def _result(self, pos, score, die_sum):
        pos = (pos + die_sum) % 10
        score += pos + 1
        if score >= 21:
            return pos, score, True

        return pos, score, False

    @lru_cache(maxsize=None)
    def play_turn(self, pos_1, score_1, pos_2, score_2, index=0, die_sum=None):
        pos = [pos_1, pos_2]
        score = [score_1, score_2]
        wins = [0, 0]

        if die_sum:
            pos[index], score[index], win = self._result(pos[index], score[index], die_sum)

            if win:
                wins[index] += 1
                return tuple(wins)

            index = (index + 1) % 2  # switch player

        for _die_sum in self.all_rolls:
            p1, p2 = self.play_turn(pos[0], score[0], pos[1], score[1], index, _die_sum)
            wins[0] += p1
            wins[1] += p2

        return tuple(wins)

    def part2(self):
        p1, p2 = self.input
        p1_win, p2_win = self.play_turn(p1.pos, 0, p2.pos, 0)
        return max(p1_win, p2_win)

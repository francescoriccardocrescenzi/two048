"""Unit tests for two048.py ."""

import unittest as ut
from two048 import Game, Status
import numpy as np

class TestGame(ut.TestCase):
    """Unit tests for the Game class."""
    def test_shift_up(self):
        """Check whether Game.shift_up works properly."""
        n = 4
        winning_number = 2048
        game = Game(n,winning_number)
        game.table = np.array([
            [0,0,0,2],
            [0,0,0,2],
            [2,0,0,0],
            [4,0,0,2]
        ])
        result = game.table = np.array([
            [2,0,0,4],
            [4,0,0,2],
            [0,0,0,0],
            [0,0,0,0]
        ])
        game.shift_up()
        self.assertTrue(np.all(game.table == result))

    def test_shift_left(self):
        """Check whether Game.shift_left works properly."""
        n = 4
        winning_number = 2048
        game = Game(n, winning_number)
        game.table = np.array([
            [0, 0, 0, 2],
            [0, 0, 2, 2],
            [2, 0, 0, 0],
            [4, 0, 0, 2]
        ])
        result = game.table = np.array([
            [2, 0, 0, 0],
            [4, 0, 0, 0],
            [2, 0, 0, 0],
            [4, 2, 0, 0]
        ])
        game.shift_left()
        self.assertTrue(np.all(game.table == result))

    def test_shift_right(self):
        """Check whether Game.shift_right works properly."""
        n = 4
        winning_number = 2048
        game = Game(n, winning_number)
        game.table = np.array([
            [0, 0, 0, 2],
            [0, 0, 2, 2],
            [2, 0, 0, 0],
            [4, 0, 0, 2]
        ])
        result = game.table = np.array([
            [0, 0, 0, 2],
            [0, 0, 0, 4],
            [0, 0, 0, 2],
            [0, 0, 4, 2]
        ])
        game.shift_right()
        self.assertTrue(np.all(game.table == result))


if __name__ == "__main__":
    ut.main()
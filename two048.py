"""Game engine for "2048".

This module defines a class Game whose instances are 2048 games.
"""

# Import useful libraries:
#   - numpy: the "2048" game is played on a numpy array
#   - random: random handles
#   - enum: the status of the "2048" game is memorized as an Enum
#   - re: we use the sub function to print the game table

import numpy as np
import random
from enum import Enum
import re

random.seed()

Status = Enum("Status", ["WON", "LOST", "IN_PROGRESS"])


class Game:
    """Each instance represents a 2048 game.

    The game table is represented as a nxn numpy array (n is provided by the user an is usually set = 4).
    Use the shift_left, shift right, shift_up, shift_down methods to
    shift the numbers on the table. These methods represent moves the player can make.
    A move is legal if it results in at least one number shifting or changing.
    Every time the player makes a legal move, a 2 is randomly inserted on the table.
    If the player cannot make any legal move, they lose.
    If the player manages to obtain a number >= winning number (winning number is provided by the user and is usually
    set = 2048), they win.
    The status of the game (WON - LOST - IN_PROGRESS) is memorized as a Status Enum.
    """

    def __init__(self, n: int, winning_number: int):
        """Initialize a 2048 game and set up all the instance variables.

        Arguments:
            n -- size of the game table
            winning_number -- number that the user should exceed to win
        """
        self.n = n
        self.table = np.zeros((n, n), dtype=int)
        self.winning_number = winning_number
        self.status = Status.IN_PROGRESS

        self.insert_random_2()

    def compact(self, axis: int, direction: int):
        """Compact self.table along the given axis and towards the given direction.

        Arguments:
            axis -- 0 for rows, 1 for columns
            direction -- +1 to compact towards the beginning, -1 to compact towards the end
        """
        # The code is written to work along rows. The axis == 1 case is covered by creating a transposed view of
        # self.table. If the direction is set to -1 we also permutate the columns of such view.
        table_view = self.table if axis == 0 else self.table.transpose()
        table_view = table_view[:, ::direction]

        # Compact each row of table_view one at a time.
        # i -- row index
        # j -- column index
        for i in range(self.n):
            # We need to keep track of the number eliminated elements to avoid getting stuck in a loop.
            num_eliminated_elements = 0
            j = 0
            while j < self.n - num_eliminated_elements - 1:
                if table_view[i, j] == 0:
                    # Compact the array by "eliminating" table_view[i, j]. The concatenate function is used for the sake
                    # of efficiency.
                    table_view[i, j:] = np.concatenate((table_view[i, j + 1:], np.zeros(1)))
                    num_eliminated_elements += 1
                else:
                    j += 1

    def sum_adjacent_equal_elements(self, axis: int, direction: int):
        """Sum the adjacent equal elements along the given axis and towards the given direction.

        Arguments:
            axis -- 0 for rows, 1 for columns
            direction -- +1 to compact towards the beginning, -1 to compact towards the end
        """
        # The code is written to work along rows. The axis == 1 case is covered by creating a transposed view of
        # self.table. If the direction is set to -1 we also permutate the columns of such view.
        table_view = self.table if axis == 0 else self.table.transpose()
        table_view = table_view[:, ::direction]

        # Compact each row of table_view one at a time.
        # i -- row index
        # j -- column index
        for i in range(self.n):
            # We need to keep track of the number eliminated elements to avoid getting stuck in a loop.
            num_eliminated_elements = 0
            j = 0
            while j < self.n - num_eliminated_elements - 1:
                if table_view[i, j] == table_view[i, j + 1]:
                    table_view[i, j + 1] = 2 * table_view[i, j + 1]
                    table_view[i, j:] = np.concatenate((table_view[i, j + 1:], np.zeros(1)))
                    num_eliminated_elements += 1
                else:
                    j += 1

    def shift_left(self):
        """Shift the table left.

        The same algorithm is applied to every row:
            - compact the row to the left by removing empty space
            - replace consecutive equal integers with a single integer equal to their sum
        """
        self.compact(0, +1)
        self.sum_adjacent_equal_elements(0, +1)

    def shift_right(self):
        """Shift the table right.

        The same algorithm is applied to every row:
            - compact the row to the right by removing empty space
            - replace consecutive equal integers with a single integer equal to their sum
        """
        self.compact(0, -1)
        self.sum_adjacent_equal_elements(0, -1)

    def shift_up(self):
        """Shift the table up.

        The same algorithm is applied to every column:
            - compact the column above by removing empty space
            - replace consecutive equal integers with a single integer equal to their sum
        """
        self.compact(1, +1)
        self.sum_adjacent_equal_elements(1, +1)

    def shift_down(self):
        """Shift the table down.

        The same algorithm is applied to every column:
            - compact the column below by removing empty space
            - replace consecutive equal integers with a single integer equal to their sum
        """
        # i -- column index
        # j -- row index
        self.compact(1, -1)
        self.sum_adjacent_equal_elements(1, -1)

    def update_status(self):
        """Check whether the game has been won or lost and update the self.status instance variable if necessary."""
        # If there is at least one element in self.table >= self.winning_number, update the game status to WON.
        if np.any(self.table >= self.winning_number):
            self.status = Status.WON
            return
        # If any entry of the table is null, the game is certainly not lost. Since at this point we know that the game
        # is not lost, any subsequent check becomes unnecessary.
        if np.any(self.table == 0):
            return
        # At this point, we know that the game is not won and that no entry of self.table is null. Check if the player
        # can make any legal move, i.e. if there are two consecutive equal elements of self.table along either axis.
        # If this is the case, no further check is needed and we can return. If the player can make no legal move,
        # the game is lost.
        for i in range(self.n):
            for j in range(self.n):
                # The indexing may fail due to out of bounds errors and thus a try block is required. If the indexing
                # fail, just try a different pair of indices.
                try:
                    if self.table[i,j] == self.table[i+1,j]:
                        return
                except IndexError:
                    pass
                try:
                    if self.table[i,j] == self.table[i,j+1]:
                        return
                except IndexError:
                    pass
        self.status = Status.LOST

    def display(self):
        """Display the game table in a legible format."""
        # The first bracket needs to be replaced by a space to preserve indentation.
        print()
        print(re.sub("[\[\]]", "", " " + np.array_str(self.table)))
        print()

    def insert_random_2(self):
        """Replace a random null entry of self.table with the number 2. Nothing is done if there is no null entry."""
        coordinates = np.where(self.table == 0)
        number_of_empty_cells = coordinates[0].shape[0]
        if number_of_empty_cells > 0:
            k = random.randrange(number_of_empty_cells)
            i = coordinates[0][k]
            j = coordinates[1][k]
            self.table[i, j] = 2
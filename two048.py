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
from re import sub

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

    def __init__(self, n, winning_number):
        """Initialize a 2048 game and set up all the instance variables.

        Arguments:
            self
            n -- integer representing the size of the game table
            winning_number -- integer representing the number that the user should exceed to win
        """
        self.n = n
        self.table = np.zeros((n, n), dtype=int)
        self.winning_number = winning_number
        self.status = Status.IN_PROGRESS

        self.insert_random_2()

    def shift_left(self):
        """Shift the table left.

        The same algorithm is applied to every row:
            - compact the row to the left by removing empty space
            - replace consecutive equal integers with a single integer equal to their sum
        """
        # i -- row index
        # j -- column index
        for i in range(self.n):
            # We need to keep track of the number eliminated elements to avoid getting stuck in a loop.
            num_eliminated_elements = 0
            # Iterate over the i-th row to compact the row by eliminating null entries.
            j = 0
            while j < self.n - num_eliminated_elements - 1:
                if self.table[i, j] == 0:
                    # Compact the array by "eliminating" self.table[i, j]. The concatenate function is used for the sake
                    # of efficiency.
                    self.table[i, j:] = np.concatenate((self.table[i, j + 1:], np.zeros(1)))
                    num_eliminated_elements += 1
                else:
                    j += 1
            # Iterate over the i-th row again to sum up consecutive equal entries.
            j = 0
            while j < self.n - num_eliminated_elements - 1:
                if self.table[i, j] == self.table[i, j + 1]:
                    self.table[i, j + 1] = 2*self.table[i, j + 1]
                    self.table[i, j:] = np.concatenate((self.table[i, j + 1:], np.zeros(1)))
                    num_eliminated_elements += 1
                else:
                    j += 1

    def shift_right(self):
        """Shift the table right.

        The same algorithm is applied to every row:
            - compact the row to the right by removing empty space
            - replace consecutive equal integers with a single integer equal to their sum
        """
        # i -- row index
        # j -- column index
        for i in range(self.n):
            # We need to keep track of the number eliminated elements to avoid getting stuck in a loop.
            num_eliminated_elements = 0
            # Iterate through the i-th row in reverse order to compact the row by eliminating null entries.
            j = self.n - 1
            while j > num_eliminated_elements:
                if self.table[i, j] == 0:
                    # Compact the array by "eliminating" self.table[i, j]. The concatenate function is used for the sake
                    # of efficiency.
                    self.table[i, :j + 1] = np.concatenate((np.zeros(1), self.table[i, :j]))
                    num_eliminated_elements += 1
                else:
                    j -= 1
            # Iterate over the i-th row again to sum up consecutive equal entries.
            j = self.n - 1
            while j > num_eliminated_elements:
                if self.table[i, j] == self.table[i, j - 1]:
                    self.table[i, j - 1] = 2 * self.table[i, j - 1]
                    self.table[i, :j + 1] = np.concatenate((np.zeros(1), self.table[i, :j]))
                    num_eliminated_elements += 1
                else:
                    j -= 1

    def shift_up(self):
        """Shift the table up.

        The same algorithm is applied to every column:
            - compact the column above by removing empty space
            - replace consecutive equal integers with a single integer equal to their sum
        """
        # i -- column index
        # j -- row index
        for i in range(self.n):
            # We need to keep track of the number eliminated elements to avoid getting stuck in a loop.
            num_eliminated_elements = 0
            # Iterate through the i-th column in reverse order to compact the row by eliminating null entries.
            j = 0
            while j < self.n - num_eliminated_elements - 1:
                if self.table[j, i] == 0:
                    # Compact the array by "eliminating" self.table[i, j]. The concatenate function is used for the sake
                    # of efficiency.
                    self.table[j:, i] = np.concatenate((self.table[j + 1:, i], np.zeros(1)))
                    num_eliminated_elements += 1
                else:
                    j += 1
            # Iterate over the i-th column again to sum up consecutive equal entries.
            j = 0
            while j < self.n - num_eliminated_elements - 1:
                if self.table[j, i] == self.table[j + 1, i]:
                    self.table[j + 1, i] = 2 * self.table[j + 1, i]
                    self.table[j:, i] = np.concatenate((self.table[j + 1:, i], np.zeros(1)))
                    num_eliminated_elements += 1
                else:
                    j += 1

    def shift_down(self):
        """Shift the table down.

        The same algorithm is applied to every column:
            - compact the column below by removing empty space
            - replace consecutive equal integers with a single integer equal to their sum
        """
        # i -- column index
        # j -- row index
        for i in range(self.n):
            # We need to keep track of the number eliminated elements to avoid getting stuck in a loop.
            num_eliminated_elements = 0
            # Iterate through the i-th column in reverse order to compact the row by eliminating null entries.
            j = self.n - 1
            while j > num_eliminated_elements:
                if self.table[j, i] == 0:
                    # Compact the array by "eliminating" self.table[i, j]. The concatenate function is used for the sake
                    # of efficiency.
                    self.table[:j + 1, i] = np.concatenate((np.zeros(1), self.table[:j, i]))
                    num_eliminated_elements += 1
                else:
                    j -= 1
            # Iterate over the i-th column again to sum up consecutive equal entries.
            j = self.n - 1
            while j > num_eliminated_elements:
                if self.table[j, i] == self.table[j - 1, i]:
                    self.table[j - 1, i] = 2 * self.table[j - 1, i]
                    self.table[:j + 1, i] = np.concatenate((np.zeros(1), self.table[:j, i]))
                    num_eliminated_elements += 1
                else:
                    j -= 1

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
                # fail, just try a different pair of indeces.
                try:
                    if self.table[i,j] == self.table[i+1,j]:
                        return
                except:
                    pass
                try:
                    if self.table[i,j] == self.table[i,j+1]:
                        return
                except:
                    pass
        self.status = Status.LOST

    def display(self):
        """Display the game table in a legible format."""
        # We use the array_str numpy method to convert the table to a string, and then we use a regular expression to
        # remove the brackets. The first bracket needs to be replaced by a space to preserve indentation.
        # A blank line is printed before and after the table.
        print()
        print(sub("[\[\]]", "", " " + np.array_str(self.table)))
        print()

    def insert_random_2(self):
        """Replace a random null entry of self.table with the number 2. Nothing is done if there is no null entry."""
        if np.any(self.table == 0):
            # Select random indices i,j until self.table[i, j] == 0. Then set self.table[i, j] = 2.
            i = random.randrange(self.n)
            j = random.randrange(self.n)
            while self.table[i, j] != 0:
                i = random.randrange(self.n)
                j = random.randrange(self.n)
            self.table[i, j] = 2
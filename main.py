"""Play a command line "2048" game."""
from two048 import Game, Status

# Create a new "2048" game, set a random entry and display it.
game = Game(4, 2048)
game.display()

# As long as the game is not won or lost, allow the player to make moves by inputting characters.
# Illegal moves or meaningless strings are ignored.
while game.status == Status.IN_PROGRESS:
    c = input()
    if c == "w":
        game.shift_up()
    elif c == "d":
        game.shift_right()
    elif c == "s":
        game.shift_down()
    elif c == "a":
        game.shift_left()
    else:
        print("Use the 'w', 'a', 's', 'd' keys to control the game.")

    game.insert_random_2()
    game.update_status()
    game.display()


if game.status == Status.LOST:
    print("You lost!")
elif game.status == Status.WON:
    print("You won!")

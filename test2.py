from interactiveGame import *

try:
    n = int(raw_input("Welcome to Clue Master Detective! How many players in the game? "))
    while n < 2:
        n = int(raw_input("At least 2 players needed. How many players do you want? "))
    game = InteractiveGame(n)
    game.play()

except Exception as e:
    print "Error while running this game: ", e


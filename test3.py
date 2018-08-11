from moreInteractiveGame import InteractiveGame
from cmdCard import findWord
from listOfCards import *

try:
    print "Welcome to Clue Master Detective! "
    flag = 'y'

    while flag == 'y':
        n = int(raw_input("How many players in the game? "))
        while n < 2:
            n = int(raw_input("At least 2 players needed. How many players do you want? "))

        diffLevel = int(raw_input("Select your difficulty level (1 - 10): "))
        while diffLevel < 1 or diffLevel > 9:
            diffLevel = int(raw_input("Invalid input. Select your difficulty level (1 - 9) "))

        game = InteractiveGame(n, diffLevel)
        game.play()

        flag = 'n'
        #flag = raw_input("Want to play another game? (y/n) ").lower()

except Exception as e:
    print "Error while running the game: ", e

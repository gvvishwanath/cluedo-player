from player import Player, ACCUSED_CORRECTLY
from listOfCards import SuspectCards, WeaponCards, RoomCards
from confidential import Confidential

from random import randrange

NO_RESULT = 10

class Game:
    def __init__(self, numPlayers):
        self.numPlayers = numPlayers
        self.players = []
        for i in range(numPlayers):
            player = Player(i, "Nameless")
            self.players.append(player)

        self.suspectCards = SuspectCards
        self.weaponCards = WeaponCards
        self.roomCards = RoomCards
        self.envelope = Confidential()
        self.cardsToDeal = []
        self.currentPlayer = Player(-1, "Nobody")

        print "A CMD game for %d players is ready!\n" % self.numPlayers
        print "Enter their names: "
        for i in range(self.numPlayers):
            self.setName(i, raw_input())
        print


    def setName(self, i, name):
        if i in range(self.numPlayers):
            self.players[i].name = name


    def putAwayAnswers(self):
        suspectId = randrange(0, len(self.suspectCards))
        suspectCard = self.suspectCards[suspectId]

        weaponId = randrange(0, len(self.weaponCards))
        weaponCard = self.weaponCards[weaponId]

        roomId = randrange(0, len(self.roomCards))
        roomCard = self.roomCards[roomId]

        self.envelope.putInEnvelope([suspectCard, weaponCard, roomCard])

        for i in range(len(self.suspectCards)):
            if i != suspectId:
                self.cardsToDeal.append(self.suspectCards[i])
        self.shuffle()

        for i in range(len(self.weaponCards)):
            if i != weaponId:
                self.cardsToDeal.append(self.weaponCards[i])
        self.shuffle()

        for i in range(len(self.roomCards)):
            if i != roomId:
                self.cardsToDeal.append(self.roomCards[i])
        self.shuffle()


    def shuffle(self):
        print "Shuffling the cards..."
        l = len(self.cardsToDeal)

        for i in range(l):
            j = randrange(0, l)
            temp = self.cardsToDeal[i]
            self.cardsToDeal[i] = self.cardsToDeal[j]
            self.cardsToDeal[j] = temp


    def deal(self):
        print "Dealing the cards..."
        for i in range(len(self.cardsToDeal)):
            id = i%self.numPlayers
            self.players[id].takeCard(self.cardsToDeal[i])
        self.cardsToDeal = []
        print


    def playRound(self):
        for i in range(self.numPlayers):
            self.currentPlayer = self.players[i]
            print "It is ",self.currentPlayer,"'s turn now."
            listeners = self.players[0:i] + self.players[i+1:self.numPlayers]
            playersWhoShowed = []
            allPassed = True

            if not self.currentPlayer.canGuess:
                continue

            guess = self.currentPlayer.makeGuess()

            for listener in listeners:
                listener.listen(guess)
                card = listener.showCard()
                self.players[i].seeCard(listener, card)

                if card is not None:
                    allPassed = False
                    playersWhoShowed.append(listener.ID)

            if allPassed:
                self.players[i].isAccusing = True
                result = self.players[i].accuse(self.envelope)
                if result == ACCUSED_CORRECTLY:
                    return result

            try:
                for listener in listeners:
                    listener.observe(playersWhoShowed, guess, self.players[i])
            except Exception as e:
                print "Exception in listener.observe():", e

            print

        return NO_RESULT


    def reset(self):
        for player in self.players:
            self.cardsToDeal.append(player.returnCards())


    def displayResults(self):
        print
        print "This is what the players had or found: "
        for player in self.players:
            player.checkList.printList()


    def play(self):
        self.putAwayAnswers()
        self.deal()

        rnd = 1
        maxRounds = 15

        while True and rnd < maxRounds:
            print "Playing round %d" % rnd
            result = self.playRound()
            if result == ACCUSED_CORRECTLY:
                print self.currentPlayer, " wins the game! Congrats, ", self.currentPlayer.name + "!"
                print
                self.displayResults()
                self.reset()
                return result
            rnd += 1
            print

        print "Game timed out. Play it again later."
        self.displayResults()
        self.reset()
        return NO_RESULT


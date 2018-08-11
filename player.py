from checklist import CheckList
from cmdCard import SUSPECT, WEAPON, ROOM

ACCUSED_CORRECTLY = 12
ACCUSED_WRONGLY = 13
MAGIC_NUMBER = -2

class Player(object):
    def __init__(self, ID=None, name=None):
        self.ID = ID
        self.name = name

        self.checkList = CheckList(self.ID)
        self.cardList = []

        self.guess = {}
        self.othersGuess = {}
        self.guess[SUSPECT] = self.othersGuess[SUSPECT] = None
        self.guess[WEAPON] = self.othersGuess[WEAPON] = None
        self.guess[ROOM] = self.othersGuess[ROOM] = None
        self.cardToShow = None

        self.isAccusing = False
        self.canGuess = True
        self.guessPreDecided = False

    def __str__(self):
        return "Player: " + str(self.ID) + " (" + self.name + ")";


    def takeCard(self, card):
        self.cardList.append(card)
        self.checkList.mark(self.ID, card)


    def returnCards(self):
        cardsToReturn = self.cardList
        self.cardList = []
        self.checkList.reset()
        return cardsToReturn


    def seeCard(self, showingPlayer, card):
        if card is None:
            return
        elif card.name is None:
            return

        print showingPlayer, " shows a card to ", self
        self.checkList.mark(showingPlayer.ID, card)


    def showCard(self):
        suspect = self.othersGuess[SUSPECT]
        weapon = self.othersGuess[WEAPON]
        room = self.othersGuess[ROOM]

        if weapon in self.cardList:
            self.cardToShow = weapon
            print self, " has a card to show"

        elif suspect in self.cardList:
            self.cardToShow = suspect
            print self, " has a card to show"

        elif room in self.cardList:
            self.cardToShow = room
            print self, " has a card to show"

        else:
            self.cardToShow = None
            print self, " has no card to show"

        return self.cardToShow


    def listen(self, guess):
        self.othersGuess = guess


    def makeGuess(self):
        if not self.guessPreDecided:
            self.guess[SUSPECT] = self.checkList.firstUnmarkedSuspect()
            self.guess[WEAPON] = self.checkList.firstUnmarkedWeapon()
            self.guess[ROOM] = self.checkList.firstUnmarkedRoom()

        print self, " makes the guess: ", self.guess[SUSPECT],  ", " , self.guess[WEAPON], ", ", self.guess[ROOM]
        self.guessPreDecided = False
        return self.guess


    def check(self):
        self.isAccusing = True


    def accuse(self, envelope):
        if self.isAccusing:
            print self, " is accusing."
            answer = envelope.takeOutOfEnvelope()

            if answer[SUSPECT] == self.guess[SUSPECT] and answer[WEAPON] == self.guess[WEAPON] and answer[ROOM] == \
                    self.guess[ROOM]:
                print answer[SUSPECT]
                print answer[WEAPON]
                print answer[ROOM]
                print self, " has made the correct accusation!"
                return ACCUSED_CORRECTLY

            else:
                self.canGuess = False
                print self, " has made a wrong accusation. Cannot guess now, but can show cards to other players."
                return ACCUSED_WRONGLY


    def observe(self, playersWhoShowed, guess, asker):
        checkTable = {}
        for key in guess:
            checkTable[key] = self.checkList.markedAsHaving(guess[key])

        l = len(playersWhoShowed)
        if l == 3:
            ''' None of the asked cards is the answer. '''
            toMark = str(MAGIC_NUMBER) + "obs"
            for key in guess:
                if checkTable[key] is None:
                    print self," has found something by observation!"
                    self.checkList.mark(toMark, guess[key])

        elif l == 2:
            ''' If the asking player has one of the asked cards, then the other two are also not answers. '''

            '''if checkTable[SUSPECT] == asker.ID:
                if checkTable[WEAPON] is not None:
                    self.checkList.mark(MAGIC_NUMBER, guess[WEAPON])
                if checkTable[ROOM] is not None:
                    self.checkList.mark(MAGIC_NUMBER, guess[ROOM])

            elif checkTable[WEAPON] == asker.ID:
                if checkTable[SUSPECT] is not None:
                    self.checkList.mark(MAGIC_NUMBER, guess[SUSPECT])
                if checkTable[ROOM] is not None:
                    self.checkList.mark(MAGIC_NUMBER, guess[ROOM])

            if checkTable[ROOM] == asker.ID:
                if checkTable[WEAPON] is not None:
                    self.checkList.mark(MAGIC_NUMBER, guess[WEAPON])
                if checkTable[SUSPECT] is not None:
                    self.checkList.mark(MAGIC_NUMBER, guess[SUSPECT])'''

            ''' If self is one of the showing players, and self has two, the other player has the third. '''

            otherIndex = -1

            if self in playersWhoShowed:
                if playersWhoShowed[0] == self:
                    otherIndex = 1
                else:
                    otherIndex = 0

                toMark = str(otherIndex) + "obs"

                if checkTable[SUSPECT] == self.ID and checkTable[WEAPON] == self.ID:
                    print self, " has found something by observation!"
                    self.checkList.mark(toMark, guess[ROOM])

                elif checkTable[SUSPECT] == self.ID and checkTable[ROOM] == self.ID:
                    print self, " has found something by observation!"
                    self.checkList.mark(toMark, guess[WEAPON])

                elif checkTable[ROOM] == self.ID and checkTable[WEAPON] == self.ID:
                    print self, " has found something by observation!"
                    self.checkList.mark(toMark, guess[SUSPECT])

        elif l == 1:
            ''' If I haven't marked the showing player as having any of the three cards, and I have marked two,
            then the third belongs to this player.'''

            playerMarked = False
            if playersWhoShowed[0] in checkTable.values():
                playerMarked = True

            if not playerMarked:
                numCardsKnown = 0
                cardUnknown = None

                for key in checkTable:
                    if checkTable[key] is not None:
                        numCardsKnown += 1
                    else:
                        cardUnknown = guess[key]

                if numCardsKnown == 2:
                    print self, " has found something by observation!"
                    toMark = str(playersWhoShowed[0]) + "obs"
                    self.checkList.mark(toMark, cardUnknown)

        else:
            ''' Repeat the guess. '''
            self.guessPreDecided = True
            self.guess[SUSPECT] = guess[SUSPECT]
            self.guess[WEAPON] = guess[WEAPON]
            self.guess[ROOM] = guess[ROOM]










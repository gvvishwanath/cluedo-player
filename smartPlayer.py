from player import *
from cmdCard import INVALID

expert = 7

class ProgrammablePlayer(Player):
    def __init__(self, ID=None, name=None, diffLevel=1):
        Player.__init__(self, ID, name)
        self.diffLevel = diffLevel

        self.suspectPredecided = False
        self.weaponPredecided = False
        self.roomPredecided = False

        self.count = {SUSPECT: 0, WEAPON: 0, ROOM: 0, INVALID: 0}


    def takeCard(self, card):
        self.cardList.append(card)
        self.checkList.mark(self.ID, card)
        self.count[card.code] += 1


    def returnCards(self):
        cardsToReturn = self.cardList
        self.cardList = []
        self.checkList.reset()

        self.suspectPredecided = False
        self.weaponPredecided = False
        self.roomPredecided = False

        self.count = {SUSPECT: 0, WEAPON: 0, ROOM: 0, INVALID: 0}

        return cardsToReturn


    def makeGuess(self):
        if not self.suspectPredecided:
            self.guess[SUSPECT] = self.checkList.firstUnmarkedSuspect()

        if not self.weaponPredecided:
            self.guess[WEAPON] = self.checkList.firstUnmarkedWeapon()

        if not self.roomPredecided:
            self.guess[ROOM] = self.checkList.firstUnmarkedRoom()

        self.suspectPredecided = self.weaponPredecided = self.roomPredecided = False

        print self, " makes the guess: ", self.guess[SUSPECT], ", ", self.guess[WEAPON], ", ", self.guess[ROOM]
        self.guessPreDecided = False
        return self.guess


    def check(self):
        if self.guess[SUSPECT] not in self.cardList:
            self.checkList.markAsAnswer(-1, self.guess[SUSPECT])

        if self.guess[WEAPON] not in self.cardList:
            self.checkList.markAsAnswer(-1, self.guess[WEAPON])

        if self.guess[ROOM] not in self.cardList:
            self.checkList.markAsAnswer(-1, self.guess[ROOM])

        if self.checkList.answer[SUSPECT] and self.checkList.answer[WEAPON] and self.checkList.answer[ROOM]:
            self.isAccusing = True


    def confirm(self):
        flags = {}
        for key, value in self.checkList.answer.iteritems():
            flags[key] = (value is not None)

        if flags[SUSPECT] and flags[WEAPON] and flags[ROOM]:
            return

        elif flags[SUSPECT] and flags[WEAPON]:
            pass



    def exclaim(self):
        if self.diffLevel < expert:
            print self, " has found something by observation!"


    def observe(self, playersWhoShowed, guess, asker):
        level = self.diffLevel
        nSP = len(playersWhoShowed)

        checkTable = {}
        playerHasCards = {}
        askerHasCards = []

        ''' Kind of card vs. who is marked against it '''
        try:
            for key in guess:
                checkTable[key] = self.checkList.markedAsHaving(guess[key])

        except Exception as e:
            print "Error in ProgrammablePlayer.observe(): ", e

        ''' Which showing player has which cards '''
        try:
            for id in playersWhoShowed:
                playerHasCards[id] = []
            for key, value in checkTable.iteritems():
                if value is not None and value in playersWhoShowed:
                    playerHasCards[value].append(key)

        except Exception as e:
            print "Error in ProgrammablePlayer.observe(): ", e

        ''' Which cards the asker has '''
        try:
            for key in guess:
                if checkTable[key] == asker.ID:
                    askerHasCards.append(key)

        except Exception as e:
            print "Error in ProgrammablePlayer.observe(): ", e

        if level <= 1:
            ''' No observation. '''
            return

        if level >= 2:
            ''' If three players show cards in a turn, none of them can be an answer. '''
            if nSP == 3:
                toMark = str(MAGIC_NUMBER) + "obs"
                for key in guess:
                    if checkTable[key] is None:
                        self.checkList.mark(toMark, guess[key])
                self.exclaim()
                return

        if level >= 3:
            ''' If all players pass in a particular round, then the card(s) I haven't marked as the asker's, could
            be answer(s). '''
            if nSP == 0:
                if self.checkList.markedAsHaving(guess[SUSPECT]) != asker.ID:
                    self.suspectPredecided = True
                    self.guess[SUSPECT] = guess[SUSPECT]

                if self.checkList.markedAsHaving(guess[WEAPON]) != asker.ID:
                    self.weaponPredecided = True
                    self.guess[WEAPON] = guess[WEAPON]

                if self.checkList.markedAsHaving(guess[ROOM]) != asker.ID:
                    self.roomPredecided = True
                    self.guess[ROOM] = guess[ROOM]

                #self.exclaim()
                if level >= 10:
                    self.confirm()
                return

        if level >= 4:
            ''' If two cards are with the asker and one player shows a card, then that is the third card. '''
            if len(askerHasCards) == 2 and nSP == 1:
                key = SUSPECT + WEAPON + ROOM - sum(askerHasCards)
                self.checkList.mark(playersWhoShowed[0], guess[key])
                self.exclaim()
                return

        if level >= 5:
            ''' If asker has one card and two players show cards, then those two are not answers. '''
            if len(askerHasCards) == 1 and nSP == 2:
                toMark = str(MAGIC_NUMBER) + "obs"
                for key in checkTable:
                    if key != askerHasCards[0] and checkTable[key] is None:
                        self.checkList.mark(toMark, guess[key])
                self.exclaim()
                return

        if level >= 6:
            ''' If two players show cards in a turn and one of them is known to have two out of three
            cards in the guess, then the second player has the third card. '''
            if nSP == 2:
                try:
                    list1 = playerHasCards[playersWhoShowed[0]]
                    if len(list1) == 2:
                       key = SUSPECT + WEAPON + ROOM - sum(list1)
                       self.checkList.mark(playersWhoShowed[1], guess[key])
                       self.exclaim()
                       return

                except Exception as e:
                    print "Error in ProgrammablePlayer.observe(): ", e

                try:
                    list1 = playerHasCards[playersWhoShowed[1]]
                    if len(list1) == 2:
                        key = SUSPECT + WEAPON + ROOM - sum(list1)
                        self.checkList.mark(playersWhoShowed[0], guess[key])
                        self.exclaim()
                        return

                except Exception as e:
                    print "Error in ProgrammablePlayer.observe(): ", e

        if level >= 7:
            ''' If two asked cards are known to be answers and one player shows a card, that is the third card.'''
            if nSP == 1:
                if self.checkList.answer[SUSPECT] == guess[SUSPECT] and self.checkList.answer[WEAPON] == guess[WEAPON]:
                    self.checkList.mark(playersWhoShowed[0], guess[ROOM])
                    self.exclaim()
                    return

                elif self.checkList.answer[SUSPECT] == guess[SUSPECT] and self.checkList.answer[ROOM] == guess[ROOM]:
                    self.checkList.mark(playersWhoShowed[0], guess[WEAPON])
                    self.exclaim()
                    return

                elif self.checkList.answer[ROOM] == guess[ROOM] and self.checkList.answer[WEAPON] == guess[WEAPON]:
                    self.checkList.mark(playersWhoShowed[0], guess[SUSPECT])
                    self.exclaim()
                    return

        if level >= 8:
            ''' If one asked card is known to be an answer and two players show cards, those two aren't answers. '''
            if nSP == 2:
                toMark = str(MAGIC_NUMBER) + "obs"

                if self.checkList.answer[SUSPECT] == guess[SUSPECT]:
                    if checkTable[WEAPON] is None:
                        self.checkList.mark(toMark, guess[WEAPON])

                    if checkTable[ROOM] is None:
                        self.checkList.mark(toMark, guess[ROOM])

                    self.exclaim()
                    return

                elif self.checkList.answer[WEAPON] == guess[WEAPON]:
                    if checkTable[SUSPECT] is None:
                        self.checkList.mark(toMark, guess[SUSPECT])

                    if checkTable[ROOM] is None:
                        self.checkList.mark(toMark, guess[ROOM])

                    self.exclaim()
                    return

                elif self.checkList.answer[ROOM] == guess[ROOM]:
                    if checkTable[WEAPON] is None:
                        self.checkList.mark(toMark, guess[WEAPON])

                    if checkTable[SUSPECT] is None:
                        self.checkList.mark(toMark, guess[SUSPECT])

                    self.exclaim()
                    return

        if level >= 9:
            ''' If one asked card is known to be an answer, a second is known to be with the asker, and a player shows
            a card, that is the third card.'''
            if nSP == 1 and len(askerHasCards) == 1:
                try:
                    answerKey = INVALID

                    if self.checkList.answer[SUSPECT] == guess[SUSPECT]:
                        answerKey = SUSPECT

                    elif self.checkList.answer[WEAPON] == guess[WEAPON]:
                        answerKey = WEAPON

                    elif self.checkList.answer[ROOM] == guess[ROOM]:
                        answerKey = ROOM

                    if answerKey is not INVALID:
                        key = SUSPECT + WEAPON + ROOM - answerKey - askerHasCards[0]
                        self.checkList.mark(playersWhoShowed[0], guess[key])
                        self.exclaim()
                        return

                except Exception as e:
                    print "Error in ProgrammablePlayer.observe(): ", e
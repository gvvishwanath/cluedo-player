from game import *
from cmdCard import *
from smartPlayer import *

CANNOT_GUESS = 15

class InteractiveGame(object):
    def __init__(self, numPlayers, diffLevel):
        self.numPlayers = numPlayers
        self.diffLevel = diffLevel

        self.players = []
        for i in range(numPlayers):
            player = ProgrammablePlayer(i, "Nameless", diffLevel)
            self.players.append(player)

        self.suspectCards = SuspectCards
        self.weaponCards = WeaponCards
        self.roomCards = RoomCards
        self.envelope = Confidential()
        self.cardsToDeal = []
        self.currentPlayer = Player(-1, "Nobody")

        print "A CMD game for %d players is ready!\n" % self.numPlayers
        print "Enter their names (your name first):"
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
            id = i % self.numPlayers
            self.players[id].takeCard(self.cardsToDeal[i])
        self.cardsToDeal = []
        print


    def showUserCards(self):
        print "You have received the following cards. Please note them down."
        for card in self.players[0].cardList:
            print card
        print


    def inputGuess(self):
        suspectName = ""
        weaponName = ""
        roomName = ""

        try:
            suspectName = raw_input("Enter suspect you want to guess: ")
            suspectName = findWord(suspectName)

        except Exception as e:
            print "In InteractiveGame.inputGuess(): ", e

        suspectCard = Card(suspectName, SUSPECT)

        while suspectCard not in SuspectCards:
            print "Invalid suspect"
            try:
                suspectName = raw_input("Enter suspect you want to guess: ")
                suspectName = findWord(suspectName)

            except Exception as e:
                print "In InteractiveGame.inputGuess(): ", e

            suspectCard = Card(suspectName, SUSPECT)

        try:
            weaponName = raw_input("Enter weapon you want to guess: ")
        except Exception as e:
            print "In InteractiveGame.inputGuess(): ", e

        weaponCard = Card(weaponName, WEAPON)

        while weaponCard not in WeaponCards:
            print "Invalid weapon"
            try:
                weaponName = raw_input("Enter weapon you want to guess: ")
            except Exception as e:
                print "In InteractiveGame.inputGuess(): ", e

            weaponCard = Card(weaponName, WEAPON)

        try:
            roomName = raw_input("Enter room you want to guess: ")
        except Exception as e:
            print "In InteractiveGame.inputGuess(): ", e

        roomCard = Card(roomName, ROOM)

        while roomCard not in RoomCards:
            print "Invalid room"
            try:
                roomName = raw_input("Enter room you want to guess: ")
            except Exception as e:
                print "In InteractiveGame.inputGuess(): ", e

            roomCard = Card(roomName, ROOM)

        self.players[0].guess[SUSPECT] = suspectCard
        self.players[0].guess[WEAPON] = weaponCard
        self.players[0].guess[ROOM] = roomCard


    def inputCardToShow(self):
        cardName = ""
        cardName2 = ""

        try:
            cardName = raw_input("Enter card you want to show (or pass if no card): ").upper()
            cardName2 = findWord(cardName)

        except Exception as e:
            print "In InteractiveGame.inputCardToShow(): ", e

        try:
            if cardName.lower() == 'pass':
                self.players[0].cardToShow = None

            elif cardName2 is not None and Card(cardName2, SUSPECT) in self.players[0].cardList:
                self.players[0].cardToShow = Card(cardName2, SUSPECT)

            elif cardName in WeaponsList and Card(cardName, WEAPON) in self.players[0].cardList:
                self.players[0].cardToShow = Card(cardName, WEAPON)

            elif cardName in RoomsList and Card(cardName, ROOM) in self.players[0].cardList:
                self.players[0].cardToShow = Card(cardName, ROOM)

            else:
                print "You cannot show this card."
                self.inputCardToShow()

        except Exception as e:
            print "In InteractiveGame.inputCardToShow(): ", e


    def reset(self):
        for player in self.players:
            self.cardsToDeal += (player.returnCards())


    def displayResults(self):
        print
        print "This is what the players had or found: "
        for player in self.players:
            if player != self.players[0]:
                player.checkList.printList()


    def userPlay(self):
        print "It is your turn now."
        self.currentPlayer = self.players[0]

        listeners = self.players[1:self.numPlayers]
        playersWhoShowed = []
        allPassed = True

        if not self.players[0].canGuess:
            print "You cannot guess!\n"
            return CANNOT_GUESS

        self.inputGuess()

        for listener in listeners:
            listener.listen(self.players[0].guess)
            card = listener.showCard()

            if card is not None:
                allPassed = False
                playersWhoShowed.append(listener.ID)
                print listener, " shows you ", card

        if allPassed:
            signal = 'n'
            try:
                signal = raw_input("Do you want to accuse? (y/n) ")
                signal = signal.lower()
            except Exception as e:
                print "Error in userPlay(): ", e

            while signal != 'y' and signal != 'n':
                try:
                    signal = raw_input("Do you want to accuse? (y/n) ")
                    signal = signal.lower()

                except Exception as e:
                    print "Error in userPlay(): ", e

            if signal == 'y':
                self.players[0].isAccusing = True
                result = self.players[0].accuse(self.envelope)

                if result == ACCUSED_CORRECTLY:
                    pass
                else:
                    print "Uh oh! You made a mistake."

                return result

        try:
            for listener in listeners:
                listener.observe(playersWhoShowed, self.players[0].guess, self.players[0])

        except Exception as e:
            print "Exception in listener.observe():", e

        print
        return NO_RESULT


    def othersPlay(self):
        for i in range(1, self.numPlayers):
            self.currentPlayer = self.players[i]
            print "It is ", self.currentPlayer, "'s turn now."

            if not self.currentPlayer.canGuess:
                print self.currentPlayer, " cannot guess!\n"
                continue

            allPassed = True
            playersWhoShowed = []

            guess = self.players[i].makeGuess()
            otherListeners = self.players[1:i] + self.players[i + 1:self.numPlayers]

            self.inputCardToShow()
            card = self.players[0].cardToShow
            self.players[i].seeCard(self.players[0], card)

            if card is not None:
                allPassed = False
                playersWhoShowed.append(0)

            for listener in otherListeners:
                listener.listen(guess)
                card = listener.showCard()
                self.players[i].seeCard(listener, card)

                if card is not None:
                    allPassed = False
                    playersWhoShowed.append(listener.ID)

            if allPassed:
                self.players[i].check()

                if self.players[i].isAccusing:
                    result = self.players[i].accuse(self.envelope)
                    if result == ACCUSED_CORRECTLY:
                        return result

            try:
                for listener in otherListeners:
                    listener.observe(playersWhoShowed, guess, self.players[i])
            except Exception as e:
                print "Exception in listener.observe():", e

            print

        return NO_RESULT


    def play(self):
        self.putAwayAnswers()
        self.deal()
        self.showUserCards()

        rnd = 1
        maxRounds = 15

        while rnd < maxRounds:
            print "Playing round %d" % rnd
            result = self.userPlay()
            if result == ACCUSED_CORRECTLY:
                print "You win the game! Congrats, %s!" % self.players[0].name
                print
                break
            else:
                result = self.othersPlay()
                if result == ACCUSED_CORRECTLY:
                    print self.currentPlayer, " wins the game! Congrats, ", self.currentPlayer.name + "!"
                    print
                    break

            rnd += 1
            print

        flag = raw_input('Do you want to know what the other players had (or found)? (y/n) ')
        if flag.lower() == 'y':
            self.displayResults()

        #self.reset()
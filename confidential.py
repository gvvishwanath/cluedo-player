from cmdCard import SUSPECT, WEAPON, ROOM, INVALID

class Confidential:
    def __init__(self):
        self.cards = {}
        self.cards[SUSPECT] = None
        self.cards[WEAPON] = None
        self.cards[ROOM] = None


    def putInEnvelope(self, answers):
        isValid = False

        if answers is not None:
            if len(answers) == 3:
                if answers[0] != None and answers[1] != None and answers[2] != None:
                    if answers[0].code != INVALID and answers[1].code != INVALID and answers[2].code != INVALID:
                        for card in answers:
                            self.cards[card.code] = card

                        isValid = True
                        for code in self.cards.keys():
                            if self.cards[code] is None:
                                isValid = False

        if isValid:
            print "The suspect, weapon and room for this game have been put away into the envelope."
        else:
            print "Confidential.putInEnvelope(): Please pass a list with 1 suspect, 1 weapon and 1 room as parameter."
            self.cards[SUSPECT] = None
            self.cards[WEAPON] = None
            self.cards[ROOM] = None


    def takeOutOfEnvelope(self):
        cardsCopy = {}
        cardsCopy[SUSPECT] = self.cards[SUSPECT]
        cardsCopy[WEAPON] = self.cards[WEAPON]
        cardsCopy[ROOM] = self.cards[ROOM]
        cards = {}

        print "The answers have been taken out of the envelope."
        return cardsCopy


    def peekIntoEnvelope(self):
        cardsCopy = {}
        cardsCopy[SUSPECT] = self.cards[SUSPECT]
        cardsCopy[WEAPON] = self.cards[WEAPON]
        cardsCopy[ROOM] = self.cards[ROOM]
        return cardsCopy

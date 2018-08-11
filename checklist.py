from cmdCard import SuspectsList, WeaponsList, RoomsList, SUSPECT, WEAPON, ROOM, Card

class CheckList:
    def __init__(self, ownerID=None):
        self.ownerID = ownerID

        self.Suspects = {}
        self.Weapons = {}
        self.Rooms = {}
        self.hash = {SUSPECT: self.Suspects, WEAPON: self.Weapons, ROOM: self.Rooms}

        self.answer = {SUSPECT: None, WEAPON: None, ROOM: None}
        self.count = {SUSPECT: len(SuspectsList), WEAPON: len(WeaponsList), ROOM: len(RoomsList)}

        self.fill()


    def fill(self):
        for name in SuspectsList:
            self.Suspects[name] = None

        for name in WeaponsList:
            self.Weapons[name] = None

        for name in RoomsList:
            self.Rooms[name] = None

    def reset(self):
        self.fill()

        self.answer = {SUSPECT: None, WEAPON: None, ROOM: None}
        self.count = {SUSPECT: len(SuspectsList), WEAPON: len(WeaponsList), ROOM: len(RoomsList)}


    def mark(self, playerID, card):
        if card.name is None:
            print "Invalid card shown by %s to %s" % (playerID, self.ownerID)
            return

        self.hash[card.code][card.name] = playerID

        self.count[card.code] -= 1
        if self.count[card.code] == 1:
            self.answer[card.code] = card


    def unmark(self, card):
        if card.name is None:
            print "Invalid card to unmark for %s " % (self.ownerID)
            return

        self.hash[card.code][card.name] = None

        self.count[card.code] += 1
        self.answer[card.code] = None


    def markedAsHaving(self, card):
        return self.hash[card.code][card.name]


    def markAsAnswer(self, filler, card):
        for key in self.hash[card.code].keys():
            if key == card.name:
                continue
            elif self.hash[card.code][key] is None:
                self.mark(filler, Card(key, card.code))

        self.answer[card.code] = card


    def firstUnmarked(self, code):
        for key in self.hash[code].keys():
            if self.hash[code][key] is None:
                return Card(key, code)

    def firstUnmarkedSuspect(self):
        return self.firstUnmarked(SUSPECT)

    def firstUnmarkedWeapon(self):
        return self.firstUnmarked(WEAPON)

    def firstUnmarkedRoom(self):
        return self.firstUnmarked(ROOM)


    def printSuspects(self):
        print "SUSPECTS:"
        print "-------------------------------------"
        print "\tName\t\t\t|\t\tMarked as"
        print "-------------------------------------"
        for name in self.Suspects:
            owner = self.Suspects[name]
            if owner is None:
                owner = ""
            print "%15s\t\t|\t\t%4s" % (name, owner)
        print "-------------------------------------\n"

    def printWeapons(self):
        print "WEAPONS:"
        print "-------------------------------------"
        print "\tName\t\t\t|\t\tMarked as"
        print "-------------------------------------"
        for name in self.Weapons:
            owner = self.Weapons[name]
            if owner is None:
                owner = ""
            print "%15s\t\t|\t\t%4s" % (name, owner)
        print "-------------------------------------\n"

    def printRooms(self):
        print "ROOMS:"
        print "-------------------------------------"
        print "\tName\t\t\t|\t\tMarked as"
        print "-------------------------------------"
        for name in self.Rooms:
            owner = self.Rooms[name]
            if owner is None:
                owner = ""
            print "%15s\t\t|\t\t%4s" % (name, owner)
        print "-------------------------------------\n"

    def printList(self):
        print "Checklist\t\t\t\tOwner: %s" % (self.ownerID)
        self.printSuspects()
        self.printWeapons()
        self.printRooms()


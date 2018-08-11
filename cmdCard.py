SuspectsList = ["COLONEL MUSTARD", "PROFESSOR PLUM", "MR. GREEN", "MRS. PEACOCK", "MISS SCARLET", "MRS. WHITE"]
WeaponsList = ["KNIFE", "CANDLESTICK", "REVOLVER", "ROPE", "LEAD PIPE", "WRENCH"]
RoomsList = ["HALL", "LOUNGE", "DINING ROOM", "KITCHEN", "BALLROOM", "CONSERVATORY", "BILLIARD ROOM", "LIBRARY",
             "STUDY"]

SUSPECT = 0
WEAPON = 1
ROOM = 2
INVALID = 3

cardInfo = {SUSPECT: SuspectsList, WEAPON: WeaponsList, ROOM: RoomsList}
dictionary = {SUSPECT: "SUSPECT", WEAPON: "WEAPON", ROOM: "ROOM", INVALID: "INVALID"}

synonyms = {"COLONEL MUSTARD": ["COL. MUSTARD", "COL.MUSTARD", "COL MUSTARD", "MUSTARD"],
            "PROFESSOR PLUM": ["PLUM", "PROF. PLUM", "PROF.PLUM", "PROF PLUM"],
            "MR. GREEN": ["MR GREEN", "MR.GREEN", "GREEN"],
            "MRS. PEACOCK": ["MRS.PEACOCK", "MRS PEACOCK", "PEACOCK"],
            "MISS SCARLET": ["MS. SCARLET", "MS SCARLET", "MS.SCARLET", "SCARLET"],
            "MRS. WHITE": ["MRS WHITE", "MRS.WHITE", "WHITE"]}


def findWord(word):
    word = word.upper()
    if word in synonyms.keys():
        return word
    else:
        for name in synonyms:
            if word in synonyms[name]:
                return name

        return None


class Card(object):
    def __init__(self, name, code):
        self.name = name
        self.code = code
        self.isValid = self.validate()

    def __str__(self):
        if self.name is not None:
            string = self.name + ": " + self.wordForCode()
        else:
            string = "INVALID CARD"
        return string

    def validate(self):
        if self.code in cardInfo.keys():
            if self.name is not None and self.name.upper() in cardInfo[self.code]:
                self.name = self.name.upper()
                return True

        self.name = None
        self.code = INVALID
        return False

    def wordForCode(self):
        return dictionary[self.code]

    def __eq__(self, other):
        if other is None:
            return False
        elif type(other) is not Card:
            return False
        return (self.name == other.name) and (self.code == other.code)

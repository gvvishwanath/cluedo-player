from cmdCard import Card, SuspectsList, WeaponsList, RoomsList, SUSPECT, WEAPON, ROOM

SuspectCards = []
WeaponCards = []
RoomCards = []

for name in SuspectsList:
    card = Card(name, SUSPECT)
    SuspectCards.append(card)

for name in WeaponsList:
    card = Card(name, WEAPON)
    WeaponCards.append(card)

for name in RoomsList:
    card = Card(name, ROOM)
    RoomCards.append(card)

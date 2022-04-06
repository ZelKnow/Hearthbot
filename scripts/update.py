import json
from hearthstone import cardxml

with open("./src/plugins/hearthstone_card/translation.json") as file:
    data = json.load(file)

db, _ = cardxml.load()

l = []

for card in db:
    if type(db[card].card_set
            ) is not int and db[card].card_set.name not in data["set"] and db[
                card].card_set.name not in l:
        l.append(db[card].card_set.name)
        print(db[card].name)

print("set", l)

l = []

for card in db:
    if db[card].multi_class_group.name not in data["multiclass"] and db[
            card].multi_class_group.name not in l:
        l.append(db[card].multi_class_group.name)

print("multi_class_group", l)

l = []

for card in db:
    if db[card].race.name not in data["race"] and db[card].race.name not in l:
        l.append(db[card].race.name)
    if db[card].race.name == 'LOCK':
        print(db[card].name)

print("race", l)

for r in l:
    print("\"" + r + "\": \"\",")

l = []

for card in db:
    if db[card].rarity.name not in data["rarity"] and db[
            card].rarity.name not in l:
        l.append(db[card].rarity.name)

print("rarity", l)

l = []

for card in db:
    if db[card].type.name not in data["type"] and db[card].type.name not in l:
        l.append(db[card].type.name)

print("rarity", l)

l = []

for card in db:
    if db[card].card_class.name not in data["class"] and db[
            card].card_class.name not in l:
        l.append(db[card].card_class.name)

print("class", l)

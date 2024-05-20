with open("cards.txt", "r") as cards_file:
    ids = [line.strip().split(',', 1)[0] for line in cards_file]

with open("ids.txt", "w") as ids_file:
    for card_id in ids:
        ids_file.write(card_id + "\n")

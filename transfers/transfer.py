from nsdotpy.session import NSSession
import json

with open("puppets.txt", "r") as file:
    puppets = file.readlines()

with open("config.json", "r") as config:
    config = json.load(config)

UA = config.get("userAgent", '')
passy = config.get("password", '')
amount = config.get("amount", '')

for i in range(len(puppets)):
    puppets[i] = puppets[i].replace('\n', '')

session = NSSession("Mass Bidder", "1.0.0", "Kractero", UA)

with open("cards.txt", "r") as cards_file:
    cards = [line.strip().split(',') for line in cards_file]

if session.login(UA, passy):
    for card_idx, card in enumerate(cards):
        card_id, season, amt = card
        amt = int(amt)
        while amt > 0:
            response = session.request(f"https://www.nationstates.net/template-overall=none/page=deck/card={card_id}/season={season}", {"auction_ask": amount, "auction_submit": "ask"})
            if "has been lodged." not in response.text:
                break
            else:
                print(f"Asking for {amount} on {card_id} season {season}, #{amt}")
                amt -= 1

for card_idx, card in enumerate(cards):
    card_id, season, amt = card
    amt = int(amt)
    while amt > 0:
        if session.login(puppets[0], passy):
            keep_bidding = True
            while keep_bidding:
                response = session.request(f"https://www.nationstates.net/template-overall=none/page=deck/card={card_id}/season={season}", {"auction_bid": amount, "auction_submit": "bid"})
                if "has been lodged." not in response.text:
                    puppets.pop(0)
                    keep_bidding = False
                else:
                    print(f"Putting a bid for {amount} on {card_id} season {season}, #{amt}")
                    amt -= 1
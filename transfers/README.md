Bespoke transfer setup that takes a file of cards formatted like id,season,amt. 

Your UA nation (which is presumably our main) will place bids equal to the amount of asks for each card. Then, the puppets will begin placing asks to match the amount of bids. Puppets will place as many bids as they can to fit within the configured ask/bid amount (for example if they have 25 bank they will place two asks)

1. Put puppets into puppets.txt.

2. Put the cards you want to transfer into cards.txt formatted like id,season,amt. Amount is the amount of times that card will be bidded and asked on.

3. Fill out config.json with userAgent, the ask/bid amount, and the password to login to each nation.

4. Run transfers.py.

5. To transfer back, run cleanup_names.py and copy the list from ids.txt and throw it into Finder.
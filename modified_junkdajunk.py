import requests
from time import sleep
from bs4 import BeautifulSoup
import csv
import os
from colorama import init, Fore, Back, Style
import sys

print("Version 2")
Password = ""
UserAgent="Kractero"
giftto ="Kractero"
names=[]
junk_list=[]
sell_list=[]

init()

names = open('puppets_list.txt').read().split('\n')

count = -1

for nation in names:
    count=count+1
    r = requests.get('https://www.nationstates.net/cgi-bin/api.cgi/', headers={'User-Agent': UserAgent}, params={'nationname':nation, 'q':'cards+deck'})
    print(f"{Fore.BLUE}Grabbing {nation}+{Style.RESET_ALL}")
    sleep(.7)
    soup = BeautifulSoup(r.content, "xml")
    deck = soup.find_all("CARD")
    if len(deck) > 200:
        print (nation + " Deck exceeds 200 cards, running jdj")
        for idx, card in enumerate(deck):
            cardid = card.find("CARDID").text
            season = card.find("SEASON").text
            if season == "1":
                continue

            r2 = requests.get('https://www.nationstates.net/cgi-bin/api.cgi/', headers={'User-Agent': UserAgent}, params={'cardid':cardid,'season':season, 'q':'card+markets+info'})
            sleep(.7)
            soup2 = BeautifulSoup(r2.content, "xml")

            for stuff in soup2.find_all("CARD"):
                CATEGORY = stuff.find("CATEGORY").text
                MARKET_VALUE = stuff.find("MARKET_VALUE").text
                REGION = stuff.find("REGION")
                SEASON = stuff.find("SEASON").text

                highest_bid = 0
                markets = soup2.find_all('MARKET')
                for market in markets:
                    if market.TYPE.string == 'bid' and float(market.PRICE.string) > highest_bid:
                        highest_bid = float(market.PRICE.string)

                isJunk = False
                if CATEGORY == "common" and float(highest_bid) < .50:
                    isJunk=True 
                elif CATEGORY == "uncommon" and float(highest_bid) < 1:
                    isJunk=True 
                elif CATEGORY == "rare" and float(highest_bid) < 1:
                    isJunk=True 
                elif CATEGORY == "ultra-rare" and float(highest_bid) < 1:
                    isJunk=True 
                elif CATEGORY == "epic" and float(highest_bid) < 1:
                    isJunk=True 
                if float(MARKET_VALUE) >= 10:
                    isJunk=False
                if REGION is not None:
                    REGION = REGION.text
                    if REGION == "Ambition":
                        isJunk=False
                        print ("Skipping because region Ambition")
                    if REGION == "Remembrance":
                        isJunk=False
                        print ("Skipping because region Remembrance")
                    if REGION == "The Burning Legion":
                        isJunk=False
                        print ("Skipping because region The Burning Legion")
                    if REGION == "Archive":
                        isJunk=False
                        print ("Skipping because region Archive")
                    if REGION == "World of Beetles":
                        isJunk=False
                        print ("Skipping because region World of Beetles")

                if isJunk:
                    print(f"{idx+1}/{len(deck)} -> {Fore.RED}{cardid} Junk with a MV of: {MARKET_VALUE}, highest_bid: {highest_bid}, rarity:{CATEGORY}")
                    print(Style.RESET_ALL)
                    junk_list.append(f"https://www.nationstates.net/nation={nation}/page=ajax3/a=junkcard/card={cardid}/season={season}/User_agent={UserAgent}Script=JunkDaJunk/Author_Email=NSWA9002@gmail.com/Author_discord=9003/Author_main_nation=9003/autoclose=1"+"\n")
                else:
                    print(f"{Fore.GREEN}{cardid} {idx+1}/{len(deck)} -> noting a needed gift or skip: {MARKET_VALUE}, highest_bid: {highest_bid}, rarity:{CATEGORY}")
                    print(Style.RESET_ALL)
                    if SEASON == "1":
                        print ("Omitting s1 from gifts")
                        continue
                    else:
                        print ("Writing gift")
                        sell_list.append(f"https://www.nationstates.net/page=deck/nation={giftto}/card={cardid}/season={season}?sellmode=1" + "\n")
    else:
        print (nation + " Deck too small, skipping")

chunk_size = 5000
num_chunks = len(junk_list) // chunk_size + 1
for chunk_num in range(num_chunks):
    start_idx = chunk_num * chunk_size
    end_idx = min((chunk_num + 1) * chunk_size, len(junk_list))
    
    html_filename = f'junkable_{start_idx}-{end_idx}.html'
    with open(html_filename, 'w') as links:
        links.write("""
        <html>
        <head>
        <style>
        td.createcol p {
            padding-left: 10em;
        }
        
        a {
            text-decoration: none;
            color: black;
        }
        
        a:visited {
            color: grey;
        }
        
        table {
            border-collapse: collapse;
            display: table-cell;
            max-width: 100%;
            border: 1px solid darkorange;
        }
        
        tr, td {
            border-bottom: 1px solid darkorange;
        }
        
        td p {
            padding: 0.5em;
        }
        
        tr:hover {
            background-color: lightgrey;
        }
        
        </style>
        </head>
        <body>
        <table>
        """)

        chunk_junkables = junk_list[start_idx:end_idx]
        totalcount = len(junk_list)

        for idx, k in enumerate(chunk_junkables, start=start_idx + 1):
            canonical = k.lower().replace(" ", "_")
            links.write("""<tr>""")
            links.write("""<td>{} of {}</td>""".format(idx, totalcount))
            links.write("""<td><p><a target="_blank" href="{}">Link to Junk</a></p></td>""".format(canonical, canonical, canonical))
            links.write("""</tr>\n""")
        
        links.write("""
        <td><p><a target="_blank" href="https://this-page-intentionally-left-blank.org/">Done!</a></p></td>
        <td><p><a target="_blank" href="https://this-page-intentionally-left-blank.org/">Done!</a></p></td>""".format(canonical))
        links.write("""
        </table>
        <script>
        document.querySelectorAll("td").forEach(function(el) {
            el.addEventListener("click", function() {
                let myidx = 0;
                const row = el.parentNode;
                let child = el;
                while((child = child.previousElementSibling) != null) {
                    myidx++;
                }
                row.nextElementSibling.childNodes[myidx].querySelector("p > a").focus();
                row.parentNode.removeChild(row);
            });
        });
        </script>
        </body>
        """)

sellables_html_filename = 'sellables.html'
with open(sellables_html_filename, 'w') as sellables_links:
    sellables_links.write("""
    <html>
    <head>
    <style>
    td.createcol p {
        padding-left: 10em;
    }
    
    a {
        text-decoration: none;
        color: black;
    }
    
    a:visited {
        color: grey;
    }
    
    table {
        border-collapse: collapse;
        display: table-cell;
        max-width: 100%;
        border: 1px solid darkorange;
    }
    
    tr, td {
        border-bottom: 1px solid darkorange;
    }
    
    td p {
        padding: 0.5em;
    }
    
    tr:hover {
        background-color: lightgrey;
    }
    
    </style>
    </head>
    <body>
    <table>
    """)

    for idx, k in enumerate(sell_list):
        each = k.lower().replace(" ", "_")
        sellables_links.write("""<tr>""")
        sellables_links.write("""<td>{} of {}</td>""".format(idx + 1, len(sell_list)))
        sellables_links.write(f'<td><p><a target="_blank" href="{each}">Link to Gift</a></p></td>')
        sellables_links.write("""</tr>\n""")
    
    sellables_links.write("""
    <td><p><a target="_blank" href="https://this-page-intentionally-left-blank.org/">Done!</a></p></td>
    <td><p><a target="_blank" href="https://this-page-intentionally-left-blank.org/">Done!</a></p></td>""")
    sellables_links.write("""
    </table>
    <script>
    document.querySelectorAll("td").forEach(function(el) {
        el.addEventListener("click", function() {
            let myidx = 0;
            const row = el.parentNode;
            let child = el;
            while((child = child.previousElementSibling) != null) {
                myidx++;
            }
            row.nextElementSibling.childNodes[myidx].querySelector("p > a").focus();
            row.parentNode.removeChild(row);
        });
    });
    </script>
    </body>
    """)

print("HTML files generated successfully.")
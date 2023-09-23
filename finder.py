import requests
import time
import xmltodict
import re
import argparse
import config
from pathlib import Path

def sleep(seconds):
    time.sleep(seconds)

matches = [3850880, 3850868, 3850869, 3850870, 3850874, 3850876, 3850875, 3850878, 3850872, 3850873, 3929788, 3929794, 3929795, 3929796, 3929797, 3929800, 3929801, 3929803, 3929804, 3929805, 3929806, 3929807, 3929808, 3929809, 3929810, 3929812, 3929813, 3929814, 3929815, 3929817, 3929818, 3929819, 3929820, 3929823, 3929824, 3929826,
    3929827, 3929829, 3929831, 3929833, 3929834, 3929840, 3929842, 3929844, 3929849, 3929852, 3929854, 3929855, 3929856, 3929857, 3929863, 3929864, 3929865, 3929866, 3929868, 3929869, 3929870, 3929872, 3929873, 3929874, 3929876, 3929877, 3929878, 3929882, 3929883, 3929885, 3929886, 3929888, 3929889, 3929890, 3929891, 3929893,
    3929894, 3929895, 3929898, 3929899, 3929901, 3929902, 3929903, 3929905, 3929907, 3929908, 3929910, 3929913, 3929919, 3929921, 3929922, 3929923, 3929925, 3929926, 3929927, 3929930, 3929931, 3929932, 3929934, 3929936, 3929937, 3929939, 3929940, 3929941, 3929944, 3929945, 3929946, 3929948, 3929951, 3929952, 3929953,
    3929954, 3929956, 3929958, 3929960, 4245891, 3804522, 4074820, 3423507]

def main():
    names = open('puppets_list.txt').read().split('\n')
    if not names:
        raise ValueError("No puppet list.")

    deck_data = []
    headers = {
        'User-Agent': config.user_agent
    }

    if not headers['User-Agent']:
        raise ValueError("User-Agent value is missing or empty.")

    for entry in nation_list:
        try:
            sleep (0.7)
            deck_url = f'https://www.nationstates.net/cgi-bin/api.cgi?q=cards+deck+info;nationname={entry}'
            response = requests.get(deck_url, headers=headers)
            deck_data_xml = xmltodict.parse(response.text)

            if 'CARDS' in deck_data_xml:
                if 'DECK' in deck_data_xml['CARDS'] and deck_data_xml['CARDS']['DECK'] is not None:
                    deck = deck_data_xml['CARDS']['DECK']['CARD']
                    for card in deck:
                        if int(card['CARDID']) in matches:
                            deck_data.append(f"https://www.nationstates.net/page=deck/nation={entry.lower().replace(' ', '_')}/card={card['CARDID']}/season=3/gift=1")
        except Exception as e:
            print(f"Error occurred with {entry}, skipping: {e}")
            continue

    links = open('matches.html', 'w')

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


    if deck_data and len(deck_data) > 0:
        for idx, k in enumerate(deck_data):
            canonical = k.lower().replace(" ", "_")
            links.write("""<tr>""")
            links.write("""<td>{} of {}</td>""".format(idx+1, len(deck_data)))
            links.write("""<td><p><a target="_blank" href="{}">Link to Card</a></p></td>""".format(canonical))
            links.write("""</tr>\n""")
    else:
        print ("no matches")



    links.write("""<td><p><a target="_blank" href="https://this-page-intentionally-left-blank.org/">Done!</a></p></td><td><p><a target="_blank" href="https://this-page-intentionally-left-blank.org/">Done!</a></p></td>""")
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


if __name__ == "__main__":
    main()
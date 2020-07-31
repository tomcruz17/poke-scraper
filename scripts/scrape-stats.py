#!/usr/bin/python3
"""
This module scrapes Serebii.net for basic Pokemon stats.
"""

import requests
import logging
import csv
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)

NUM_KEY = 'num'
NAME_KEY = 'name'
HP_KEY = 'hp'
ATK_KEY = 'atk'
DEF_KEY = 'def'
SPATK_KEY = 'sp_atk'
SPDEF_KEY = 'sp_def'
SPD_KEY = 'spd'
NUM_IDX = 0
NAME_IDX = 3
HP_IDX = 6
ATK_IDX = 7
DEF_IDX = 8
SPATK_IDX = 9
SPDEF_IDX = 10
SPD_IDX = 11


def get_mons(url):
    LOGGER.info(f'Getting Pokemons from {url}...')
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    dex_table = soup.find('table', {'class': 'dextable'})
    rows = dex_table.findAll('tr')

    # add index for stats and consider offset

    mons = []
    for row in rows[2:len(rows) - 1:2]:
        cols = row.findAll('td')
        num_raw = cols[NUM_IDX].text
        num = ''
        for c in list(num_raw):
            if c.isdigit():
                num += c
        name = cols[NAME_IDX].find('a').text
        LOGGER.info(name)
        hp = cols[HP_IDX].text
        atk = cols[ATK_IDX].text
        def_ = cols[DEF_IDX].text
        sp_atk = cols[SPATK_IDX].text
        sp_def = cols[SPDEF_IDX].text
        spd = cols[SPD_IDX].text

        if num and name:
            mon = {NUM_KEY: num, NAME_KEY: name, HP_KEY: hp, DEF_KEY: def_, SPATK_KEY: sp_atk, SPDEF_KEY: sp_def, SPD_KEY: spd}
            mons.append(mon)
        
    LOGGER.info(f'Found {len(mons)}.')
    LOGGER.info(f'Done getting Pokemons for {url}.')

    return mons

mons = get_mons('https://www.serebii.net/pokemon/nationalpokedex.shtml')
with open('output/pokedex.csv', 'w', encoding='utf-8', newline = '') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow([NUM_KEY, NAME_KEY, HP_KEY, ATK_KEY, DEF_KEY, SPATK_KEY, SPDEF_KEY, SPD_KEY])
    for mon in mons:
        writer.writerow([mon[NUM_KEY], mon[NAME_KEY], mon[HP_KEY], mon[DEF_KEY], mon[SPATK_KEY], mon[SPDEF_KEY], mon[SPD_KEY]])



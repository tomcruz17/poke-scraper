#!/usr/bin/python3
"""
This module scrapes https://www.serebii.net/pokemon/nationalpokedex.shtml for the most basic pokemon info: types & stats.
"""

import requests
import logging
import csv
import json
from constants import *
from bs4 import BeautifulSoup
from argparse import ArgumentParser

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)

PARSER = ArgumentParser(description='Pokémon scraper that gets all 893 Pokemon (Gen I to XIII) from Serebii.')
PARSER.add_argument('-o', '--output', action='store', help='Saves the results to an output file: .json or .csv. Format is based on file extension.')
ARGS = PARSER.parse_args()

def get_mons(url):
    LOGGER.info(f'Getting Pokemons from {url}...')
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    dex_table = soup.find('table', class_='dextable')
    rows = dex_table.findAll('tr')

    mons = []
    for index,row in enumerate(rows[2:len(rows) - 1:2]):
        try:
            cols = row.findAll('td')
            num_raw = cols[NUM_IDX].text
            mon = {}
            num = ''
            for c in num_raw:
                if c.isdigit():
                    num += c
            mon[NUM_KEY] = int(num)
            mon[NAME_KEY] = cols[NAME_IDX].find('a').text

            types_tags = cols[TYPES_IDX].findAll('a')
            mon[TYPE_KEY] = []
            for a in types_tags:
                mon[TYPE_KEY].append(a['href'].split('/')[-1])

            mon[HP_KEY] = int(cols[HP_IDX].text)
            mon[ATK_KEY] = int(cols[ATK_IDX].text)
            mon[DEF_KEY] = int(cols[DEF_IDX].text)
            mon[SPATK_KEY] = int(cols[SPATK_IDX].text)
            mon[SPDEF_KEY] = int(cols[SPDEF_IDX].text)
            mon[SPD_KEY] = int(cols[SPD_IDX].text)
            print(mon)
            mons.append(mon)
        except Exception as ex:
            LOGGER.error(f"Can't parse row {index}. {ex}")
        
    LOGGER.info(f'Found {len(mons)}.')
    LOGGER.info(f'Done getting Pokemons from {url}.')

    return mons

def write_to_csv(mons, filename):
    with open(filename, 'w', encoding='utf-8', newline = '') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow([NUM_KEY, NAME_KEY, TYPE_KEY, HP_KEY, ATK_KEY, DEF_KEY, SPATK_KEY, SPDEF_KEY, SPD_KEY])
        for mon in mons:
            writer.writerow([mon[NUM_KEY], mon[NAME_KEY], mon[TYPE_KEY], mon[HP_KEY], mon[ATK_KEY], mon[DEF_KEY], mon[SPATK_KEY], mon[SPDEF_KEY], mon[SPD_KEY]])

def write_to_json(mons, filename):
    with open(filename, mode='w', encoding='utf-8') as output_file:
        json.dump(mons, output_file, indent=4)

if __name__=='__main__':
    url = 'https://www.serebii.net/pokemon/nationalpokedex.shtml'
    mons = get_mons(url)
    if ARGS.output:
        filename = ARGS.output
        filetype = filename[filename.rindex('.')+1:]
        try:
            if filetype == 'csv':
                write_to_csv(mons, filename)
            else:
                write_to_json(mons, filename)
        except Exception as ex:
            LOGGER.error(f'Error writing to {filename}. {ex}')





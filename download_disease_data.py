import requests
from bs4 import BeautifulSoup
import csv
import re
import sys
from multiprocessing import Pool


def get_data(query):
    html = requests.get(f'https://dknet.org/data/source/nlx_154697-1/search?q={query}&l={query}').text
    try:
        soup = BeautifulSoup(html.split('<ul id="collapse-Database" class="collapse">')[1].split('<a href="javascript:void(0)">Species</a>')[0], features='html.parser')
        databases = []
        for token in soup.get_text().split():
            if '(' not in token:
                databases.append(token)
    except IndexError:
        databases = []
    species = []
    try:
        soup = BeautifulSoup(html.split('<a href="javascript:void(0)">Species</a>')[1].split('<a href="javascript:void(0)">')[0], features='html.parser')
        for line in soup.get_text().split('\n'):
            if line.strip():
                species.append(line.strip().split(' (')[0])
    except IndexError:
        species = []
    return databases, species


def extract_data(queries, names, out_file):
    writer = csv.writer(open(out_file, 'w'))
    writer.writerow(['Name', 'DOID', 'Num databases', 'Databases', 'Num species', 'Species'])
    with Pool(5) as pool:
        results = pool.map(get_data, queries)
    for i, (databases, species) in enumerate(results):
        writer.writerow([names[i], doids[i], len(databases), ','.join(databases), len(species), ','.join(species)])


if __name__ == '__main__':
    doids = []
    names = []
    for rows in csv.reader(open(sys.argv[1], 'r', encoding='utf-8')):
        try:
            doid = re.findall('DOID:[0-9]+', rows[0])[0]
        except IndexError:
            continue
        doids.append(doid)
        names.append(rows[1])
    extract_data(doids, names, 'facets.csv')

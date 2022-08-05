import csv
import requests
import xml.etree.ElementTree as ET
import json
from tqdm import tqdm
import sys
import os


csv.field_size_limit(sys.maxsize)
url = 'https://scicrunch.org/api/1/dataservices/federation/facets/nlx_154697-1'
genes = set()
gene_to_disease = {}
for line in csv.reader(open(sys.argv[1], 'r')):
    if line[9]:
        gene = line[9].strip()
        genes.add(gene)
        if gene not in gene_to_disease:
            gene_to_disease[gene] = []
        gene_to_disease[gene].append(line[2])
data = {}
for gene in tqdm(genes):
    data[gene] = {'Database': [], 'Species': [], 'Affected Gene': [], 'Phenotype': []}
    xml = requests.get(url, params={'q': gene, 'key': os.environ['SCICRUNCH_KEY']}).text
    root = ET.fromstring(xml)
    current_category = ''
    for facet in root.iter('facets'):
        if 'category' in facet.attrib:
            current_category = facet.attrib['category']
            continue
        if current_category in data[gene]:
            data[gene][current_category].append({'name': facet.text, 'count': int(facet.attrib['count'])})
json.dump(data, open('genes.json', 'w'))
json.dump(gene_to_disease, open('gene_to_disease.json', 'w'))
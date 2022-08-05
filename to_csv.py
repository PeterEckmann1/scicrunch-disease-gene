import json
import csv


def get_cols(name):
    items = [(item['count'], item['name']) for item in data[gene][name] if item['name'] and item['name'] != '-']
    if items:
        max_count, max_name = max(items)
        total = sum([item[0] for item in items])
        return max_name, max_count, total
    else:
        return '', 0, 0


gene_to_disease = json.load(open('gene_to_disease.json', 'r'))
data = json.load(open('genes.json', 'r'))
writer = csv.writer(open('genes.csv', 'w'))
writer.writerow(['Disease', 'Gene',
                 'Top database', 'Top database count', 'Total database',
                 'Top species', 'Top species count', 'Total species',
                 'Top phenotype', 'Top phenotype count', 'Total phenotype'])
for gene in data:
    disease = ' | '.join(gene_to_disease[gene])
    max_db_name, max_db_count, db_total = get_cols('Database')
    max_s_name, max_s_count, s_total = get_cols('Species')
    max_p_name, max_p_count, p_total = get_cols('Phenotype')
    writer.writerow([disease, gene, max_db_name, max_db_count, db_total, max_s_name, max_s_count, s_total, max_p_name, max_p_count, p_total])
# SciCrunch gene-disease query tool

Extracts counts of various SciCrunch objects related to disease/gene pairs.

## Downloading disease data
For a set of Human Disease Ontology IDs (DOIDs), `download_disease_data.py` downloads database and species information from `dknet.org`. Starting with a CSV containing a set of DOIDs in the first column and disease names in the second column, calling `python download_disease_data.py <filename>` will create a file `facets.csv` with downloaded data, which includes database and species counts. Alternatively, you can call the method `extract_data()` directly for more fine-grained control.

## Joining disease with gene data
`map_disease_to_gene.py` takes a CSV file with both disease and gene information downloaded from the OMIM database, processes it, and combines it with database information from SciCrunch. This files requires the environment variable `SCICRUNCH_KEY` to be set, which is an API key for the SciCrunch API. Calling `python map_disease_to_gene.py <omim_filename>` creates two files, `genes.json` and `gene_to_disease.json`, which include gene-to-database and gene-to-disease information, respectively.

## Exporting to CSV
`to_csv.py` takes the information in `genes.json` and `gene_to_disease.json`, aggregates it, and outputs to a human-readable CSV format. After running `map_disease_to_gene.py`, calling `python to_csv.py` will create a file `genes.csv` with aggregated data.
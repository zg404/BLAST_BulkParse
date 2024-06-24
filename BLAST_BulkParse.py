# BLAST_BulkParse.py
# 2024-06-24
# Zach Geurin

import argparse
import pandas as pd 

def parse_args():
    parser = argparse.ArgumentParser(description='Bulk parse ElasticBLAST output')
    parser.add_argument('--input', type=str, required=True, help='BLAST results file; use outfmt=6')
    parser.add_argument('--output', type=str, required=True, help='Output best match file; tab-delimited format')
    return parser.parse_args()


def main():
    args = parse_args()
    input_file = args.input
    output_file = args.output

    # Define the headers based on what was specified in BLAST outfmt
    headers = "qseqid sscinames sacc stitle qstart qend qlen length pident mismatch gaps evalue bitscore staxids".strip().split()
    
    # Read the BLAST output file to a pandas DataFrame
    blast_table = pd.read_table(input_file, header=None)  # Assuming tab-separated, BLAST outfmt 6
    blast_table.columns = headers  # Add the headers to the DataFrame

    # Sort queryID (col 1, asc), bitscore (col 13, desc), evalue (col 12, asc), percID (col 9, desc)
    blast_table.sort_values(by=['qseqid', 'bitscore', 'evalue', 'pident'], ascending=[True, False, True, False], inplace=True)

    # Group by QueryID and select first as best hit
    grouped = blast_table.groupby('qseqid')
    best_hits = grouped.first()  # Get the first row per query, which is the best hit

    # Find good and bad hits
    good_hits = best_hits[best_hits['pident'] >= 97]
    bad_hits = best_hits[best_hits['pident'] < 97]

    # Print overview
    print("Good hits: ", len(good_hits))
    print("Bad hits: ", len(bad_hits))
    print("Total hits: ", len(good_hits) + len(bad_hits))
    # Sanity check
    if len(good_hits) + len(bad_hits) != len(best_hits):
        print("Warning: Good and bad hits do not add up to total hits")
    
    # Save results, adding back the header row 
    # Write good and bad hits to respective files
    best_hits.to_csv("all_" + output_file, sep="\t", header=True)
    good_hits.to_csv("good_" + output_file, sep="\t", header=True)
    bad_hits.to_csv("bad_" + output_file, sep="\t", header=True)


if __name__ == '__main__':
    main()
#! /usr/bin/env python3

import argparse
import pandas as pd 
import os
import sys
from datetime import datetime

def parse_args():
    parser = argparse.ArgumentParser(
        description='Bulk parse ElasticBLAST output and identify top matches',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument('--input', type=str, required=True, 
                        help='BLAST results file (outfmt=6 format)')
    parser.add_argument('--output', type=str, required=True, 
                        help='Base name for output files (will create all_/good_/bad_ prefixed files)')
    parser.add_argument('--threshold', type=float, default=97.0,
                        help='Percent identity threshold for good/bad hit classification')
    parser.add_argument('--verbose', '-v', action='store_true',
                        help='Print additional processing information')
    return parser.parse_args()


def analyze_blast_data(blast_df, threshold=97.0):
    """
    Analyzes BLAST results and returns categorized dataframes
    
    Args:
        blast_df: Pandas DataFrame with BLAST results
        threshold: Percent identity threshold for good/bad classification
        
    Returns:
        Tuple of (best_hits, good_hits, bad_hits) DataFrames
    """
    # Sort by multiple criteria to find best matches
    blast_df.sort_values(
        by=['qseqid', 'bitscore', 'evalue', 'pident'], 
        ascending=[True, False, True, False], 
        inplace=True
    )
    
    # Group by QueryID and select first as best hit
    best_hits = blast_df.groupby('qseqid').first()
    
    # Categorize hits based on percent identity
    good_hits = best_hits[best_hits['pident'] >= threshold]
    bad_hits = best_hits[best_hits['pident'] < threshold]
    
    return best_hits, good_hits, bad_hits


def main():
    args = parse_args()
    input_file = args.input
    output_file = args.output
    threshold = args.threshold
    verbose = args.verbose
    
    # Validate input file
    if not os.path.exists(input_file):
        print(f"Error: Input file '{input_file}' not found")
        sys.exit(1)
        
    if verbose:
        print(f"Processing BLAST results from: {input_file}")
        print(f"Using identity threshold: {threshold}%")
        start_time = datetime.now()
        
    # Define the headers based on what was specified in BLAST outfmt
    headers = "qseqid sscinames sacc stitle qstart qend qlen length pident mismatch gaps evalue bitscore staxids".strip().split()
    
    # Read the BLAST output file to a pandas DataFrame
    try:
        blast_table = pd.read_table(input_file, header=None)  # Assuming tab-separated, BLAST outfmt 6
        blast_table.columns = headers  # Add the headers to the DataFrame
        
        if verbose:
            print(f"Loaded {len(blast_table)} BLAST hits for {blast_table['qseqid'].nunique()} query sequences")
    except Exception as e:
        print(f"Error reading BLAST file: {e}")
        sys.exit(1)

    # Analyze BLAST data
    best_hits, good_hits, bad_hits = analyze_blast_data(blast_table, threshold)

    # Create timestamp for output files
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Print summary report
    print("\n===== BLAST Parsing Summary =====")
    print(f"Good hits (≥{threshold}% identity): {len(good_hits)}")
    print(f"Bad hits (<{threshold}% identity): {len(bad_hits)}")
    print(f"Total unique queries with hits: {len(best_hits)}")
    
    if verbose:
        print("\nTop 5 highest identity matches:")
        top_hits = best_hits.sort_values('pident', ascending=False).head(5)
        for idx, row in top_hits.reset_index().iterrows():
            print(f"  {row['qseqid']}: {row['sscinames']} ({row['pident']:.2f}% identity, E-value: {row['evalue']:.2e})")
    
    # Save results with descriptive filenames
    output_base = f"{output_file}.tsv"
    all_output = f"all_{output_base}"
    good_output = f"good_{output_base}"
    bad_output = f"bad_{output_base}"
    
    best_hits.to_csv(all_output, sep="\t", index=True)
    good_hits.to_csv(good_output, sep="\t", index=True)
    bad_hits.to_csv(bad_output, sep="\t", index=True)
    
    print(f"\nResults saved to:")
    print(f"  - {all_output} (all hits)")
    print(f"  - {good_output} (good hits)")
    print(f"  - {bad_output} (bad hits)")
    
    if verbose:
        elapsed_time = datetime.now() - start_time
        print(f"\nTotal processing time: {elapsed_time.total_seconds():.2f} seconds")


if __name__ == '__main__':
    main()
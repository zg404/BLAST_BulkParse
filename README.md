# BLAST_BulkParse
Simple script to parse bulk BLAST results, selecting single best match, then classifying as good or bad hit

## Overview

BLAST_BulkParse processes BLAST output files (tabular format) to identify the best match for each query sequence. It categorizes matches as "good" or "bad" based on a percent identity threshold and provides summary statistics.

## Dependencies
1. Python 3 installation
2. pandas module:
   `pip install pandas`

## Features

- Parses BLAST output files in tabular format (outfmt=6)
- Identifies the best match for each query sequence
- Categorizes matches based on a customizable percent identity threshold
- Generates separate output files for all, good, and bad matches
- Provides summary statistics about the analysis

## Instructions:
1. take a fasta with multiple queries (ie, multiple fasta seqs in a single file)

2. BLAST against a database using the following arguments. Modify `-db`, `-query`, and `-num_threads` as needed.
```    
blastn -task megablast -db combined_ITS_db.fasta -query bulk_queries.fasta -num_threads 12 -outfmt "6 qseqid sscinames sacc stitle qstart qend qlen length pident mismatch gaps evalue bitscore staxids" -out blastTable.tsv
```
3. Run this script to parse results:     
```
python BLAST_BulkParse.py --input [BLAST_FILE] --output [OUTPUT_BASE] [options]
```
4. Three resulting files: all hits, good hits (>=97 pident) , and bad hits (<97 pident)

### Required Arguments

- `--input`: Path to the BLAST results file (outfmt=6 format)
- `--output`: Base name for output files

### Optional Arguments

- `--threshold`: Percent identity threshold for good/bad hit classification (default: 97.0)
- `--verbose` or `-v`: Print additional processing information

## Example

```
python BLAST_BulkParse.py --input myblast.out --output results.tsv --threshold 95 --verbose
```

This will generate:
- `all_results.tsv`: All best hits
- `good_results.tsv`: Hits with ≥95% identity
- `bad_results.tsv`: Hits with <95% identity

## Output Format
The output files are tab-delimited and contain the following columns:
- qseqid: Query sequence ID
- sscinames: Scientific name
- sacc: Subject accession
- stitle: Subject title
- qstart: Query start position
- qend: Query end position
- qlen: Query length
- length: Alignment length
- pident: Percent identity
- mismatch: Number of mismatches
- gaps: Number of gaps
- evalue: E-value
- bitscore: Bit score
- staxids: Subject taxonomy IDs
# BLAST_BulkParse
Simple script to parse bulk BLAST results, selecting single best match, then classifying as good or bad hit
# Dependencies
1. Python 3 installation
2. pandas module:
   `pip install pandas`

# Instructions:
1. take a fasta with multiple queries (ie, multiple fasta seqs in a single file)

2. BLAST against a database using the following arguments. Modify `-db`, `-query`, and `-num_threads` as needed.    
	`blastn -task megablast -db combined_ITS_db.fasta -query bulk_queries.fasta -num_threads 12 -outfmt "6 qseqid sscinames sacc stitle qstart qend qlen length pident mismatch gaps evalue bitscore staxids" -out blastTable.tsv`

3. Run this script to parse results:     
	`BLAST_BulkParse.py --input blastTable.tsv --output bestHitsTable.tsv`

4. Three resulting files: all hits, good hits (>=97 pident) , and bad hits (<97 pident)

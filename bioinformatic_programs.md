1. conda install -c bioconda blast-legacy
2. formatdb -i GCF_000005845.2_ASM584v2_protein.faa
3. blastdbcmd -db build/ecoli -entry NP_414608.1 > query.faa
4. blastall -p blastp -d GCF_000005845.2_ASM584v2_protein.faa -i query.faa -e 1e-5 -m 8 -o results.txt
5. cat results.txt

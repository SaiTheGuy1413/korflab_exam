import sys
import mcb185

k = int(sys.argv[2])
kmer_location = {}
for defline, seq in mcb185.read_fasta(sys.argv[1]):
    for i in range(len(seq)-k+1):
        kmer = seq[i:i+k]
        if kmer not in kmer_location:
            kmer_location[kmer] = []
        kmer_location[kmer].append(i)
        
    for kmer, locations in kmer_location.items():
        print(kmer, locations)
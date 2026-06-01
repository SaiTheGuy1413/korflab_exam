import sys
import mcb185

both_strands = '-both' in sys.argv

def reverse_complement(seq):
    complement = {'A':'T', 'T':'A', 'G':'C', 'C':'G'}
    result = []
    for nt in reversed(seq):
        result.append(complement[nt])
    return ''.join(result)

k = int(sys.argv[2])
kmer_location = {}
for defline, seq in mcb185.read_fasta(sys.argv[1]):
    for i in range(len(seq)-k+1):
        kmer = seq[i:i+k]
        if kmer not in kmer_location:
            kmer_location[kmer] = []
        kmer_location[kmer].append(i+1)
    
    if both_strands:
        rc = reverse_complement(seq)
        for i in range(len(rc)-k+1):
            kmer = rc[i:i+k]
            if kmer not in kmer_location:
                kmer_location[kmer] = []
            kmer_location[kmer].append(-(i+1))
        
    for kmer, locations in kmer_location.items():
        print(kmer, locations)
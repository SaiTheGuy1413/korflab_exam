import sys
import mcb185
import math

for defline, seq in mcb185.read_fasta(sys.argv[1]):
    converted = list(seq)
    for i in range(len(seq)- 11 + 1):
        window = seq[i:i+11]

        freq = {}
        for nt in window:
            if nt not in freq:
                freq[nt] = 0
            freq[nt] += 1

        h = 0
        for count in freq.values():
            p = count / 11
            h += -p * math.log2(p)
        
        if h < 1.4:
            for j in range(i, i + 11):
                converted[j] = converted[j].lower()
            
    print(defline)
    print(''.join(converted))
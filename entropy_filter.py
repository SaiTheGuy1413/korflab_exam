import sys
import mcb185
import math
import gzip

def read_fasta(filename):
	if   filename == '-':          fp = sys.stdin
	elif filename.endswith('.gz'): fp = gzip.open(filename, 'rt')
	else:                          fp = open(filename)
	name = None
	seqs = []
	while True:
		line = fp.readline()
		if line == '': break
		line = line.rstrip()
		if line.startswith('>'):
			if len(seqs) > 0:
				yield(name, ''.join(seqs))
				name = line[1:]
				seqs = []
			else:
				name = line[1:]
		else:
			seqs.append(line)

	yield(name, ''.join(seqs))
	fp.close()

for defline, seq in read_fasta(sys.argv[1]):
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
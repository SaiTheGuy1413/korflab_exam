import sys
import gzip

def reverse_complement(seq):
    complement = {'A':'T', 'T':'A', 'G':'C', 'C':'G',
                  'a':'t', 't':'a', 'g':'c', 'c':'g'}
    return ''.join(complement[nt] for nt in reversed(seq))

genome = {}
with gzip.open(sys.argv[1], 'rt') as f: #makes dict for chr and seq
    name = None
    seqs = []
    for line in f:
        line = line.rstrip()
        if line.startswith('>'):
            if name is not None:
                genome[name] = ''.join(seqs)
            name = line[1:].split()[0]  #first word after =
            seqs = []
        else:
            seqs.append(line)
    genome[name] = ''.join(seqs)  

mrnas = {}
with gzip.open(sys.argv[2], 'rt') as f: #makes dict for mrna info
    for line in f:
        if line.startswith('#'): 
            continue
        parts = line.rstrip().split('\t')
        if parts[2] == 'CDS':
            chrom  = parts[0]
            start  = int(parts[3]) - 1  
            end    = int(parts[4])      
            direction = parts[6]
            ident  = parts[8]
            
            parent = None
            for identification in ident.split(';'):
                if identification.startswith('Parent='):
                    parent = identification.split('=')[1].split(',')[0]  #grabs only the first id
            
            if parent not in mrnas:
                mrnas[parent] = {'chrom': chrom, 'direction': direction, 'cds': []}
            mrnas[parent]['cds'].append((start, end))

for mrna_id, info in mrnas.items():
    cds_seq = ''
    for start, end in sorted(info['cds']):  
        cds_seq += genome[info['chrom']][start:end] 
    if info['direction'] == '-':
        cds_seq = reverse_complement(cds_seq)
    print('>' + mrna_id)
    print(cds_seq)
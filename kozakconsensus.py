import re
import gzip
import sys
import json

canonical_only = '-can' in sys.argv

cds_list = [] 
seq = []
in_sequence = False

def reverse_complement(seq):
    complement = {'A':'T', 'T':'A', 'G':'C', 'C':'G', 'a':'t', 't':'a', 'g':'c', 'c':'g'}
    result = []
    for nt in reversed(seq):
        result.append(complement[nt])
    return ''.join(result)

'''def reverse_complement(seq):
    complement = {'A':'T', 'T':'A', 'G':'C', 'C':'G', 'a':'t', 't':'a', 'g':'c', 'c':'g'}
    return ''.join(complement[nt] for nt in reversed(seq))'''
    
with gzip.open(sys.argv[1], 'rt') as file:
    for line in file:
        if re.match(r'\s+CDS\s+', line): #checks for whitespace around CDS just in case
            if 'complement' not in line:
                match = re.search(r'(\d+)\.\.(\d+)', line) #finds location in sequence of forward strand
                if match:
                    start = int(match.group(1)) - 1
                    cds_list.append((start, '+'))
            else:
                match = re.search(r'(\d+)\.\.(\d+)', line) #finds location of backwards strand
                if match:
                    start = int(match.group(2)) - 1
                    cds_list.append((start, '-'))

        if line.startswith('ORIGIN'):  
            in_sequence = True
        elif in_sequence:              
            seq.append(''.join(line.split()[1:])) #splits origin by whitespace

genome = ''.join(seq) #joins all seq sections of origin together

window = 10
pwm = { #initializes window zeroes for each nt (+3 for ATG)        
    'A': [0] * (window*2 + 3),
    'T': [0] * (window*2 + 3),
    'G': [0] * (window*2 + 3),
    'C': [0] * (window*2 + 3)
}
for start, strand in cds_list:
    if strand == '+':
        context = genome[start-window : start+3+window].upper() #starts at A so +3 to get past G
    else:
        context = reverse_complement(genome[start-2-window : start+1+window]).upper() #starts at G in reverse so -2 to get to A
    if canonical_only and context[window:window+3] != 'ATG': #skips non canonical
        continue
    for i, nt in enumerate(context):
        if nt in pwm:
            pwm[nt][i] += 1 #increments at specific position


for nt in 'AGCT':
    print(nt, pwm[nt]) #prints results

with open('kozak.json', 'w') as f:
    json.dump(pwm, f, indent=4)
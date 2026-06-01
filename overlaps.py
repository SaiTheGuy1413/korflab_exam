import sys

def parse(filename):
    features = []
    with open(filename) as f:
        for line in f:
            parts = line.split()
            features.append((parts[0], int(parts[1]), int(parts[2])))
    return features

def overlaps(a, b):
    return a[0] == b[0] and a[1] < b[2] and a[2] > b[1]

f1 = parse(sys.argv[1])
f2 = parse(sys.argv[2])

for a in f1:
    for b in f2:
        if overlaps(a, b):
            print(a, b)
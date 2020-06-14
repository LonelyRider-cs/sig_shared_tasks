#!/usr/bin/env python3

"""
Data augmentation system for the CoNLL-SIGMORPHON 2020 Shared Task 1.

Last Update: 06/13/2020
"""

import align, getopt, sys, random, cvOCP

def cleantuple(s):
    """Remove '_'-entries and convert list to tuple."""
    return(tuple(x for x in s if x != "_"))
    
def getsubstrings(word1, word2):
    """Gets all substring pairs from aligned word1 and word2."""
    word1 = ["#"] + word1 + ["#"]
    word2 = ["#"] + word2 + ["#"]
    substrings1 = [word1[i:j] for i in range(len(word1)) for j in range(i+1,len(word1)+1)]
    substrings2 = [word2[i:j] for i in range(len(word2)) for j in range(i+1,len(word2)+1)]
    return substrings1, substrings2

def main(argv):
    
    RANDOM_SEED = 42
    INAMOUNT = 100
    OUTAMOUNT = 50000
    INCLUDEORIGINAL = False
    LENCUTOFF = 15    
    HELP = False
    CONFIDENCE = 0.98
    
    options, remainder = getopt.gnu_getopt(argv[1:], 'r:hi:o:dm:c:', ['random-seed', 'help', 'in=', 'out=', 'duplicate', 'maxlen', 'confidence'])
    OUTPUT, HELP, PATH = False, False, './../all/'
    for opt, arg in options:
        if opt in ('-r', '--random-seed'):
            RANDOM_SEED = int(arg)
        elif opt in ('-h', '--help'):
            HELP = True
        elif opt in ('-i', '--in'):
            INAMOUNT = int(arg)
        elif opt in ('-o', '--out'):
            OUTAMOUNT = int(arg)
        elif opt in ('-d', '--duplicate'):
            INCLUDEORIGINAL = True
        elif opt in ('-m', '--maxlen'):
            LENCUTOFF = int(arg)
          
    if HELP:
            print("\n*** Data augmentation for g2p data (SIGMORPHON 2020 task 1) ***\n")
            print("Usage: g2paugment.py [OPTIONS] tsvfile")
            print("Prints augmented data to stdout.")
            print("OPTIONS:")
            print(" -o NUM     How many output examples to create (default: 50000)")
            print(" -i NUM     How many input examples to use when augmenting (default: 100)")
            print(" -r NUM     Set random seed (default: 42)")
            print(" -m NUM     maximum length words to create when augmenting (default: 15)")
            print(" -c NUM     Cutoff for confidence in in-out mapping slices (default: 0.98)")
            print(" -d         Duplicate the original examples used in the output (default: no)")
            quit()  
    
    random.seed(RANDOM_SEED)

    lines = [l.rstrip('\n') for l in open(sys.argv[1])]
    random.shuffle(lines)
    lines = lines[:INAMOUNT]

    substringmappings = {}
    substringmappingsup = {}

    prons = []
    wordpairs = []
    for l in lines:
        graph, pron = l.split('\t')
        prons.append((tuple(pron.split(' ')), 1))
        plist = pron.split(' ')
        glist = list(graph)
        wordpairs.append((glist,plist))

    ap = align.Aligner(wordpairs, '_', iterations = 50) # Call the aligner

    for graph, phon in ap.alignedpairs: 
        s1, s2 = getsubstrings(graph, phon)
        for i in range(len(s1)):
            s1wd = ''.join(s1[i])
            s1wd = s1wd.replace('_','')
            s2wd = cleantuple(s2[i])          # Remove _ and convert to tuple
            if s1wd not in substringmappings: # collect substring-pair counts
                substringmappings[s1wd] = {}
            substringmappings[s1wd][s2wd] = substringmappings[s1wd].get(s2wd, 0) + 1
            if s2wd not in substringmappingsup:
                substringmappingsup[s2wd] = {}
            substringmappingsup[s2wd][s1wd] = substringmappingsup[s2wd].get(s1wd, 0) + 1 

    goodmaps = [] 
    for subin in substringmappings.keys(): # pick out the useful slices
        thisset = substringmappings[subin]
        thesum = sum(thisset.values())
        probs = [(subout, count/thesum) for subout, count in thisset.items()]
        bestmap = max(probs, key = lambda x: x[1])
        if bestmap[1] >= CONFIDENCE:
            goodmaps.append((subin, bestmap[0], bestmap[1]))

    frontmaps = []
    backmaps = []
    for g in goodmaps: # collect word-initial and word-final slices to be used for augmentation
        ins = g[0]
        if len(ins) > 0:
            if '#' in ins[0] and '#' not in ins[-1]:
                frontmaps.append(g)
            if '#' in ins[-1] and '#' not in ins[0]:
                backmaps.append(g)
        
    random.shuffle(frontmaps)
    random.shuffle(backmaps)

    C,V = cvOCP.candv(prons, random_seed = RANDOM_SEED) # figure out which phonemes are C and V

    augmented = []
    for f in frontmaps: # main augmentation loop
        for b in backmaps:
            newcand = (f[0] + b[0], f[1] + b[1])
            if len(newcand[0]) > LENCUTOFF:
                continue
            if (f[1][-1] in C and b[1][0] in C) or (f[1][-1] in V and b[1][0] in V):
                continue
            augmented.append(newcand)

    if INCLUDEORIGINAL:
        for l in lines:
            print(l)

    random.shuffle(augmented)
    for aug in augmented[:OUTAMOUNT]:
        graph = aug[0].replace('#','')
        pron = ' '.join(aug[1])
        pron = pron.replace('#', '')
        print(graph + '\t' + pron)

if __name__ == "__main__":
    main(sys.argv)


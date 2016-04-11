from __future__ import print_function
import pickle

dictfile = '../csw12.txt'

fh = open(dictfile, 'r')
wordlist = [w.replace("\n", "").upper() for w in fh.readlines()]
lwordlists = {}
for i in range(2,16):
    lwordlists[i]=[w for w in wordlist if len(w) == i]
fh.close()

pickle.dump(wordlist, open("fulldictionary.p", "wb"))
pickle.dump(lwordlists, open("lengthwisedictionary.p", "wb"))

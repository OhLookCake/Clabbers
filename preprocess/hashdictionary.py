from __future__ import print_function
import pickle

dictfile = '../csw12.txt'
numrows = 15
numcols = 15

fh = open(dictfile, 'r')
wordlist = [w.replace("\n", "").upper() for w in fh.readlines()]
fh.close()

hashedwordstring = ""
for w in wordlist:
    hashedwordstring+=('#'*14) + w

hashedwordstring+=('#'*14)

print("hashed")
pickle.dump(hashedwordstring, open("hashedwordstring.p", "wb"))
print("dumped")
readhashedwordstring = pickle.load(open("hashedwordstring.p", "rb"))
print("read")
print(readhashedwordstring[0:100])




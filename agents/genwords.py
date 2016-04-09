# -*- coding: utf-8 -*-
"""
Created on Sat Apr 09 03:10:19 2016

@author: Eeshan
"""

import re

dictfile = '../csw12.txt'

fh = open(dictfile, 'r')
wordlist = [w.replace("\n", "").upper() for w in fh.readlines()]
fh.close()
hashedwordlist = ['#'*14 + w + '#'*14 for w in wordlist]

AZ = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
##TODO: if num touchpoints in row == 0, then ditch

rack = "RECDNAV"

row = ['.','.','.','.','.','.','.','.','.','.','E','.','.','.','.']
anchorconstraints = [AZ,AZ,AZ,AZ,AZ,AZ,AZ,'PQS',AZ,'RST',AZ,'P',AZ,AZ,AZ]
anchorpoints = [False,False,False,False,False,False,False,False,False,False,False,True,False,False,False]

def strIntersection(str1, str2):
    for i in str1:
        str3 = ''
        str3 = str3.join(i for i in str1 if i in str2 not in str3)
    return str3
    

regstring = ""
for i in range(15):
    if row[i]!='.':
        regstring+='[' + row[i] + '#]'
    else:
        regstring+='[' + strIntersection(anchorconstraints[i],rack) + '#]'

regstring = '#' + regstring + '#'
#print regstring

checker = re.compile(r'(?=(' + regstring + '))')

results = []

for w in hashedwordlist:
    found = checker.finditer(w)
    
    for match in found:
        w = match.group(1)
        if max([a!='#' and b for a,b in zip(w,anchorpoints)]): #if it touches at least one anchor point:
#            print ctr, w, '|', wordlist[ctr], hashedwordlist[ctr]
            results+=[w]
            
        







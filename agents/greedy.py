from __future__ import print_function
import ConfigParser
from collections import Counter

import re

dictfile = '../csw12.txt'
numrows = 15
numcols = 15

fh = open(dictfile, 'r')
wordlist = [w.replace("\n", "").upper() for w in fh.readlines()]
lwordlists = {}
for i in range(2,16):
    lwordlists[i]=[w for w in wordlist if len(w) == i]

    
fh.close()
hashedwordlist = ['#'*14 + w + '#'*14 for w in wordlist]
AZ = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

board_anchorpoints = [[False]*15]*15
board_anchorconstraints = [[AZ]*15]*15

#inputsring = 


boardstring = "...............................................................................................................TONE.............................................................................................................."
rack = "COPERTV"
board = [list(boardstring)[i:i+numcols] for i in range(0, numrows*numcols,numcols)]
    


def showboard(board):
    #board is a numrows*numcols list    
    
    print('   |  A |  B |  C |  D |  E |  F |  G |  H |  I |  J |  K |  L |  M |  N |  O |')
    print('   ============================================================================')
    
    rownum = 1
    for row in board:
        if rownum < 10:
            print(' ', end = '')
        print(str(rownum) + ' |  ', end = '')
        rownum +=1
        
        for col in row:
            print(col, end=' |  ')
        print('')
        print('   ----------------------------------------------------------------------------')
    
    #print('----------------------------------------------------------------------------')
    
###### MOVE GENERATION #########

def strIntersection(str1, str2):
    for i in str1:
        str3 = ''
        str3 = str3.join(i for i in str1 if i in str2 not in str3)
    return str3
    
def calculateAnchors(board):
    #TODO: Do this via an update mechanism
    
    global board_anchorpoints# = [[False]*15]*15
    global board_anchorconstraints# = [[AZ]*15]*15
    
    for i in range(15):
        board_anchorpoints[i] = [False]*15
        board_anchorconstraints[i] = [AZ]*15
        
        for j in range(15):
            board_anchorpoints[i][j] = False
            if ( (i-1)<0 or board[i-1][j]=='.' ) and \
            ( (i+1)>=15 or board[i+1][j]=='.'  ) and \
            ( (j-1)<0 or board[i][j-1]=='.'    ) and \
            ( (j+1)>=15 or board[i][j+1]=='.'  ):
                continue
            if board[i][j]!='.':
                board_anchorpoints[i][j] = False
                board_anchorconstraints[i][j] =  board[i][j]
                continue
    
            
            leftstring = ""
            rightstring = ""
            upstring = ""
            downstring =""
            
            ci = i - 1
            while ci >= 0 and board[ci][j]!='.':
                leftstring = board[ci][j] + leftstring
                ci-=1
                
            ci = i + 1
            while ci < 15 and board[ci][j]!='.':
                rightstring = rightstring + board[ci][j]
                ci+=1
                
            cj = j - 1
            while cj >= 0 and board[i][cj]!='.':
                upstring = board[i][cj] + upstring
                cj-=1
                
            cj = j + 1
            while cj < 15 and board[i][cj]!='.':
                downstring = downstring + board[i][cj]
                cj+=1
            
            
            hpattern = re.compile(leftstring + '([A-Z])' + rightstring)
            vpattern = re.compile(upstring + '([A-Z])' + downstring)
            
            if len(leftstring + rightstring) > 0:
                hcandidates = ''.join([m.group(1) for m in [hpattern.match(w) for w in lwordlists[len(leftstring + rightstring) + 1]] if m])
            else:
                hcandidates = AZ
                
            if len(upstring + downstring) > 0:
                vcandidates = ''.join([m.group(1) for m in [vpattern.match(w) for w in lwordlists[len(upstring + downstring) + 1]] if m])
            else:
                vcandidates = AZ
            
            board_anchorconstraints[i][j] = strIntersection(hcandidates, vcandidates)
            #print(i,j,hcandidates,vcandidates)
            if len(board_anchorconstraints[i][j])>0:
                board_anchorpoints[i][j] = True
                
    #return (board_anchorpoints, board_anchorconstraints)    


def genRowWords(rack, row, anchorpoints, anchorconstraints):
    """
    eg:
        rack = "RECDNAV"
        row = ['.','.','.','.','.','.','.','.','.','.','E','.','.','.','.']
        anchorconstraints = [AZ,AZ,AZ,AZ,AZ,AZ,AZ,'PQS',AZ,'RST',AZ,'P',AZ,AZ,AZ]
        anchorpoints = [False,False,False,False,False,False,False,False,False,False,False,True,False,False,False]
    """

    actualrack = rack
    if '?' in rack:
        rack = AZ
        
    if sum(anchorpoints) ==0:
        return []
    
    regstring = ""
    for i in range(15):
        if row[i]!='.':
            regstring+='[' + row[i] + '#]'
        else:
            regstring+='[' + strIntersection(anchorconstraints[i],rack) + '#]'
    
    regstring = '#' + regstring + '#'
    
    checker = re.compile(r'(?=(' + regstring + '))')

    results = []
    
    for w in hashedwordlist:
        found = checker.finditer(w)
        
        for match in found:
            w = match.group(1)
            w= w[1:-1]
            start = len(re.search('^#*',w).group(0))
            end = 14 - len(re.search('#*$',w).group(0))
            
            rightbit = ""
            x = end + 1
            while x < 15 and row[x] != '.':
                rightbit = rightbit + row[x]
                x+=1
            leftbit =""
            x = start - 1
            while x >= 0 and row[x] != '.':
                leftbit = row[x] + leftbit
                x-=1
                
            actualword = leftbit + w[start:end+1] + rightbit
            
            if not actualword in lwordlists[len(actualword)]: # the effective word is not a word
                continue
            
            if not max([a!='#' and b for a,b in zip(w,anchorpoints)]): # does not touch any anchor point
                continue
            
            lettersadded = [w[i] for i in range(len(w)) if w[i]!='#' and row[i]=='.']
            diffneededtoavailable =  Counter(lettersadded) - Counter(actualrack)       
            numblanks = sum([i=='?' for i in actualrack])
            if len(diffneededtoavailable) > numblanks:
                continue
            
            anno_col = start - len(leftbit)
            anno_word = ""
            ctr = 0
            for letter in actualword:
                pos = start - len(leftbit) + ctr
                if row[pos]=='.':
                    anno_word = anno_word + actualword[ctr]
                else:
                    anno_word = anno_word + '(' + actualword[ctr] + ')'
                ctr+=1
            
            #TODO: Optional:
            anno_word = re.sub('\)\(', '', anno_word)

            results+=[(anno_col,anno_word,''.join(lettersadded))]
    return list(set(results))

def genAllWords(board):
    calculateAnchors(board)
    movelist = []
    #vmovelist = []
    #ACROSS
    for i in range(numrows):
        row = board[i]
        movelist= movelist + [(i,genRowWords(rack, row, board_anchorpoints[i], board_anchorconstraints[i]))]

    #TODO: translate move.
    
    
    return movelist

showboard(board)


hpossiblemoves = genAllWords(board)
flippedboard = map(list, zip(*board))
vpossiblemoves = genAllWords(flippedboard) #TODO: stuff will be overwritten here! We don't care, but beware!


totalmoves = 0
#print(hpossiblemoves)
for i in range(numrows):
#    print(hpossiblemoves[i])
    totalmoves+=len(hpossiblemoves[i][1]) + len(vpossiblemoves[i][1])
    print(i,len(hpossiblemoves[i][1]), len(vpossiblemoves[i][1]))
    
print('Total possible moves: ', totalmoves)

    
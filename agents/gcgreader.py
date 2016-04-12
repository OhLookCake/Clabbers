from __future__ import print_function
import re
import sys
from collections import Counter
#changes added by vivek

QUACKLELPLAYER = 1
#bag = 'AAAAAAAAABBCCDDDDEEEEEEEEEEEEFFGGGHHIIIIIIIIIJKLLLLMMNNNNNNOOOOOOOOPPQRRRRRRSSSSTTTTTTUUUUVVWWXYYZ'
numrows = 15
numcols = 15
centresquare = (numrows // 2, numcols //2) #This is effectively rounded up in 0-index

initialboardstring = ['.']*225
initialboard = [initialboardstring[i:i+numcols] for i in range(0, numrows*numcols,numcols)]

score = [0,0,0]
rack = [None, None, None]

cols = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O']
colDict = dict(zip(cols,range(len(cols))))

def gameFromGcg(lines):
    #get player names
    pName = [' ',lines[0].split()[1], lines[1].split()[1]]
    pDict = dict(zip(pName,range(len(pName))))
    moves = lines[2:]
    
    return [pName,pDict,[fromString2Move(moves,i) for i in range(len(moves))]] 
        

def fromString2Move(moves,i):
    # >p2: INETTOD 8D DITTO 16 16
    headerList = ['player','rack','loc','move','moveScore','totalScore']

    moveDict = dict(zip(headerList,range(len(headerList))))
    moveElemList = moves[i][1:].split()
    currentMove = [moveElemList[moveDict['player']][:-1],'','-','',0,0]
    if moveElemList[2]=='-':
    	pass
    else:
	    currentMove = [moveElemList[moveDict[item]]for item in headerList]
	    # print moveDict
	    # currentMove = [ moveDict[item] for item in headerList]
	    #updateRack
	    currentMove[moveDict['player']] = currentMove[moveDict['player']][:-1]
	    if(i+2 > len(moves)-1):
	        rack = list(moveElemList[moveDict['rack']])
	        move = list(moveElemList[moveDict['move']])
	        currentMove[moveDict['rack']] =  [x for x in rack if x not in move]
	    else:
	        currentMove[moveDict['rack']] = list(moves[i+2].split()[moveDict['rack']])
    return dict(zip(headerList,currentMove))  


def translateLoc(loc):
	"""changes loc to 2d array indices"""
	if(loc[0].isalpha()):	
		return [int(loc[1:])-1,colDict[loc[0]],'V']
	else:
		return [int(loc[:-1])-1, colDict[loc[-1]],'H']

def preparemessage(gamefile, rack1):
	bag = bag = 'AAAAAAAAABBCCDDDDEEEEEEEEEEEEFFGGGHHIIIIIIIIIJKLLLLMMNNNNNNOOOOOOOOPPQRRRRRRSSSSTTTTTTUUUUVVWWXYYZ'
	initialboardstring = ['.']*225
	initialboard = [initialboardstring[i:i+numcols] for i in range(0, numrows*numcols,numcols)]
	pName,pDict,data = gameFromGcg(gamefile)

	for item in data:
		if item['loc']=='-':
			pass
		else:
			loc = translateLoc(item['loc'])
			move = item['move']
			if loc[-1]=='H':
				for i in range(len(move)):
					if move[i]=='.':
						pass
					else:
						initialboard[loc[0]][loc[1]+i] = move[i]
			else:
					for i in range(len(move)):  
						if move[i]=='.':
							pass
						else:
							initialboard[loc[0]+i][loc[1]] = move[i]			
	#fill player scores and racks

	score[pDict[data[-2]['player']]] = data[-2]['totalScore']
	score[pDict[data[-1]['player']]] = data[-1]['totalScore']
 
	boardletters = re.sub('\.','',"".join(["".join(item) for item  in initialboard]))
 
 
	bag = sum(dict(Counter(bag) - Counter(boardletters)).values())
	# {"status": {"moverequired": true, "endofgame": false}, "secondstogo": 1500, "errcode": 0, "score": {"me": 0, "opponent": 0}, "board": ".................................................................................................................................................................................................................................", "rack": ["I", "N", "E", "T", "T", "O", "D"]}
	ret = '{"status": {"moverequired": true, "endofgame": false}, "secondstogo": 1500, "errcode": 0, "score": {"me": '+ str(score[pDict[data[-2]['player']]]) + ', "opponent": ' + str(score[pDict[data[-1]['player']]]) + '}, "board": "' + "".join(["".join(item) for item  in initialboard])+ '", "rack":'+ str(list(rack1))+'}'
	return (ret, bag)

#message = preparemessage(sys.argv[1], sys.argv[2])
#showboard(initialboard)
#print(score,rack)
#print(message)
#print(bag)




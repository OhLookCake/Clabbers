# Move tester
import os
import re
import csv
import gcgreader
import commands
import json

"""
for fullgcg in list of gcg files:
    Reads in fullgcg file
    for gcg in all possible first k lines of full gcg:
        Check:
            calculate bag.
            if bag not empty, and rack!=full: ditch this!
            This is because some gcg files miss annotating the complete rack
        
        testinggcg = gcg-1line
        Converts testinggcg to a messageformat (including rack)
        
        quacklemove, quacklescore = Calls the quackleinterface(testinggcg)
        greedymove, greedyscore = Calls greedyagent(message)
        
        writes out data in format:
        (
         gameid (=gcgname),
         movenumber,
         numtilesinbag,
         blankinrack?
         gcgmove,
         gcgscore,
         quacklemove,
         quacklescore
         greedymove,
         greedyscore
         ... <more agents, if there> ... 2 cols per agent
        )
        Appends it to movecomparison.csv




NOTE: Interface is not involved here
"""

"""
For analysis;
  quacklemove==greedymove?
  quacklescore-greedyscore
  
Calculate fraction where these two variables (individually) take value 1 (true)
"""


#fh = open("MoveTestingResults.csv", "w")
gcglist = os.listdir('gcgfiles')
gcglist = gcglist[:100]


for filename in gcglist:
#    print(filename)
    rawgcgcontents =  [line.rstrip('\n') for line in open('gcgfiles/' + filename)]
    gcgcontents = []
    
    ctr = 0
    for line in rawgcgcontents:
        if re.findall('^\s*$', line):
            continue
        elif re.findall('^\s*#', line) and ctr>2:
            continue
        else:
            if line.split(' ')[2][0]=='-':
                line = re.sub('-', '- ',line)
            gcgcontents.append(line)
            ctr+=1
    
    totmovesplayed = len(gcgcontents) - 2
    
    for truncpoint in range(4, totmovesplayed - 1):
#        print(truncpoint)
        truncatedgcg = gcgcontents[:truncpoint]
        nextline = gcgcontents[truncpoint].split(' ')
#        print nextline
        rack = nextline[1]
        gcgloc = nextline[2]
        gcgword = nextline[3]
        gcgscore = int(nextline[-2])
        #bag = 'AAAAAAAAABBCCDDDDEEEEEEEEEEEEFFGGGHHIIIIIIIIIJKLLLLMMNNNNNNOOOOOOOOPPQRRRRRRSSSSTTTTTTUUUUVVWWXYYZ'
        #edit gcgreader to also return bag
        message, numtilesinbag = gcgreader.preparemessage(truncatedgcg, rack)
	message = re.sub('\'','\"',message)
	jsonmessage = json.loads(message)

        if numtilesinbag > 14 and len(rack) < 7:
            continue
        
        fh = open('temp.gcg', 'w')
	for item in truncatedgcg:
		fh.write("%s\n" % item)
	fh.close()
	gameid = filename
        movenumber = truncpoint - 1
        blankinrack = '?' in rack
        
	quacklecommand = "python extension.py /home/shaurya/develop/Clabbers1/agents/temp.gcg "+ "".join(jsonmessage["rack"])
	print(quacklecommand)
	quackleoutput = commands.getoutput(quacklecommand)
	
	quackleoutput = re.sub('-','- ',quackleoutput)
	quackleoutput = quackleoutput.split(' ')
	quackleloc = quackleoutput[0]
	quackleword = quackleoutput[1]
        quacklescore = quackleoutput[2]
        

	cmd = "python greedy.py '"+ re.sub('\'', '\"', message) + "'"
        print(cmd)
        greedyoutput = commands.getoutput(cmd)
        #greedyoutput = os.system(cmd)
	greedyoutput = greedyoutput.split(' ')
	greedyloc = greedyoutput[0]
	greedyword = greedyoutput[1]
        greedyscore = greedyoutput[2]
        
        datatuple = [gameid,
                     movenumber,
                     numtilesinbag,
                     blankinrack,
                     gcgloc,
                     gcgword,
                     gcgscore,
                     quackleloc,
                     quackleword,
                     quacklescore,
                     greedyloc,
                     greedyword,
                     greedyscore]
        
        with open('MoveTestingResults.csv', 'ab') as csvfile:
            tuplewriter = csv.writer(csvfile, delimiter=',')
            tuplewriter.writerow(datatuple)
    print(filename, " complete")























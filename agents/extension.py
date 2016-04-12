import commands
import re
import sys

headerList = ['player','rack','loc','move','moveScore','totalScore']
moveDict = dict(zip(headerList,range(len(headerList))))

def formatMove(move):
    """changes quackle move format move to interface move format"""
    #handle for exchanges
    move = move.replace('.','#',len(move))
    return move

def quackle(gameFile,rack):
    #./test mode='positions' --position='temp.gcg' --report --rack="ABCDEFG"
    
    command  = 'cd /home/shaurya/develop/quackle/test/; ./test mode="positions" --position="' + gameFile + '" --lexicon="csw12" '+ '--report --rack="' + ''.join(rack) + '" | tail -1 | cut -d, -f 1'

    output = commands.getoutput(command)
    scoreoutput = re.sub('^.*\=\ ','',output)
    output = re.sub('\(.*','',output)

    if(output[0]=='-' and output[1]==' '):
        return 'pass'
    elif(output[0]=='-' and output[1].isalpha()):
        return 'exch '+output[1:]
    else:
        return formatMove(output) + scoreoutput

def translateMove(move):
    """Translates move to quackle format
    """
    cols = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O']
    if move[2]=='H':
        move  = ''.join([str(move[0]+1),cols[move[1]]])
    else:
        move = ''.join([cols[move[1]],str(move[0]+1)])
    return move

def prepGcgHeader(file):
    out = open(file,"w")
    out.write('#player1 p1 p1\n')
    out.write('#player2 p2 p2\n')
    out.close()

def write2gcg(file,move):
    """writes translated move to gcg file"""
    out =  open(file, "a")
    out.write(move+'\n')
    out.close()

pName = []
pDict = []



# main 
if __name__ == '__main__':
    # out = gameFromGcg('logan.gcg')
    out = quackle(sys.argv[1],sys.argv[2])
    print(out)

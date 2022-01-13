#Code for having user select folder/file
#from tkinter.filedialog import askopenfilename
#filename = askopenfilename()

import time
start_time = time.time()

import re

#For now you just have to put a path in here to select the file
file = open('D:\Binghamton University\Research Project\Python Parsing Code\Hands.txt')

newlineCount = 0
for line in file:
    #hand info
    if re.search("^(PokerStars)", line):
        title = re.match("^[^ ]*", line).group()
        handNumber = re.search("(?<=#)[0-9]*(?=:)", line).group()
        handType = re.search("(?<=\ \ )[^.]*(?=\ )", line).group()
        lowBet = re.search("(?<=\$)[0-9|.]*(?=\/)",line).group()
        highBet = re.search("(?<=\$)[0-9|.]*(?=\ )", line).group()
        dateAndTime = re.search("(?<=- )[^\n]*", line).group()
        #print(title + handNumber + " " + handType + " " + lowBet + " " + highBet)
        
    #Table information
    elif re.search("^(Table)", line):
        tableName = re.search("(?<=')[^\n]*(?=')", line).group()
        tableMax = re.search("([0-9]*(?=-max))", line).group()
        buttonNumber = re.search("((?<=#)[0-9](?= is the button))", line).group()
        #print(tableName + " " + tableMax + " " + buttonNumber)

    #For collecting player Names and their seats
    elif re.search("^(Seat [1-9]:[^(]* \(\$)", line) and not re.search("showed", line) and not re.search("collected", line):
        seatNumber = re.search("((?<=Seat )[0-9](?=:))", line).group()
        playerName = re.search("((?<=: )[^ ]*(?= \())", line).group()
        playerBalance = re.search("((?<=\$)[^ ]*(?= in chips))", line).group()
        #print(seatNumber + " " + playerName + " " + playerBalance)

    #for all player Actions...
    elif re.search("^([^:])*:", line) and not re.search("^(Seat)", line):
        #Needed so that you add the action to the correct player
        tempPlayerName = re.search("^[^:]", line)
        
        #fold
        if re.search("([^: ]*folds)", line):
            folded = True
            print("**Fold Added to Action List**")
            
        #raise
        if re.search("([^: ]*raises)", line):
            raiseFrom = re.search("(?<=\$)[^ ]*(?= to)", line).group()
            raiseTo = re.search("(?<=to )[^ |\n]*", line).group()
            print("**Raise Added to Action List**")
            
            #If Player is all-in
            if raiseTo == playerBalance:
                allIn = True
                print("**All in Added to Action List**")
                
        #checks
        if re.search("([^: ]*checks)", line):
            print("**Check Added to Action List**")
            
        #calls
        if re.search("([^: ]*calls)", line):
            print("calls added to list")
            
        #small blind bet
        if re.search("([^: ]*posts small)", line):
            smallBlind = True
            print("smallBlind added")
            
        #big blind bet
        if re.search("([^: ]*posts big)", line):
            bigBlind = True
            print("bigBlind added to list")
            
        #bet
        if re.search("([^: ]*bets)", line):
            print("bet added to list")
            
        #show
        if re.search("shows", line):
            pCard1 = re.search("((?<=\[)[^ ]*) ([^\]]*)", line).group(1)
            pCard2 = re.search("((?<=\[)[^ ]*) ([^\]]*)", line).group(2)
            print("Player Cards added to action list")
            
        #mucks
        if re.search("mucks hand", line):
            print("Muck added to player action")

    #for Streets, updated in player object to show which actions are being taken in which street
    elif re.search("^(\*\*\*)", line):
        
        #flop
        if re.search("(FLOP)", line):
            print("now in flop")
            cardOne = re.search("((?<=\[)[^ ]*) ([^ ]*) ([^]]*)", line).group(1)
            cardTwo = re.search("((?<=\[)[^ ]*) ([^ ]*) ([^]]*)", line).group(2)
            cardThree = re.search("((?<=\[)[^ ]*) ([^ ]*) ([^]]*)", line).group(3)

        #turn
        if re.search("(TURN)", line):
            print("Now in Turn")
            turnCard = re.search("(?<=\[)[^ ]*(?=\])", line)
            
        #river
        if re.search("RIVER", line):
            print("Now in River")
            riverCard = re.search("(?<=\[)[^ ]*(?=\])", line)
            
        #show down
        if re.search("(SHOW)", line):
            print("Now in Show Down")
            
    #For summary information including doesnt show
    elif re.search("^(Board|Total|[^ ]* collected|Uncalled)", line):
        
        #winner/win ammount
        if re.search("collected", line):
            amountCollected = re.search("(?<=\$)[^ ]*", line).group()
            
        #final total pot
        if re.search("^(Total pot)", line):
            totalPot = re.search("(?<=pot \$)[^ ]*", line).group()
            rakeAmount = re.search("(?<=Rake \$)[^\n]*", line).group()
        
        #player with uncalled bet
        if re.search("^(Uncalled)", line):
            returnedTo = re.search("(?<= to )[^\n]*", line).group()
            amountReturned = re.search("(?<=\(\$)[^\)]*", line).group()

    #when newlineCount equals 2 then we start a new hand object
    elif re.search("^(\n)", line):
        newlineCount+=1

    

#time of execution
print(newlineCount)
print("--- %s seconds ---" % (time.time() - start_time))

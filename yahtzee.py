#!python3
import pyinputplus as pyip
from random import randint
import time

# this is a multiplayer yahtzee game
# instructions: https://www.hasbro.com/common/instruct/Yahtzee.pdf

# game, player, dice attributes
games=0
playerDict={} # {player#, {playerName,{scoreTop},{scoreBottom},{totalScore]}, ...}
dice=[0, 0, 0, 0, 0, 0]
round=1

# score keeping dictionaries
scoreTop={'Ones':0,'Twos':0,'Threes':0,'Fours':0,'Fives':0,'Sixes':0}
scoreBottom={'Three of a kind':0,'Four of a kind':0,'Full house':0,
				'Small straight':0,'Large straight':0,'Yahtzee':0,'Chance':0,'Yahtzee bonus':0}
totalScore={'Sum of upper':0,'Bonus':0,'Total upper':0,'Total bottom':0,'Grand total':0}

print('Welcome to Yahtzee!')

#set number of players (1-4) and enter names
playerCount=pyip.inputInt(prompt='Enter number of players (1-4):\n', min=1, max=4)
for x in range(playerCount):
	playerDict[pyip.inputStr(prompt='Enter name of player '+str(x+1)+':\n')] = scoreTop, scoreBottom, totalScore

#show current player score card

while True:
	for x in playerDict:
		print('Here we go! Round ' + str(round) + '. ' + x + ' your turn.')

#random roll dice, player select dice, random roll remaining dice, final dice
		
		for i in range(len(dice)):
			dice[i]=randint(1,6)


#show remaining score card options for current dice (if applicable)
#choose score card option (if applicable)
#next player

#end of available rounds show player score, next player (if applicable)
		
	round=round+1
	break

#end of game show player scores, ranking (winner), and games won tally
#play again?



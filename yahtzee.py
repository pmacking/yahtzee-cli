#!python3
import pyinputplus as pyip
from random import randint
import time

# this is a multiplayer yahtzee game
# instructions: https://www.hasbro.com/common/instruct/Yahtzee.pdf

# general attributes
games=0
playerDict={} # {'playerName':({scoreTopDict},{scoreBottomDict},{totalScoreDict}), ...}
dice={1:{'keeper':False,'result':0}, 2:{'keeper':False,'result':0}, 3:{'keeper':False,'result':0}, 4:{'keeper':False,'result':0}, 5:{'keeper':False,'result':0}, 6:{'keeper':False,'result':0}}
round=1

# score keeping dictionaries
scoringDict={'scoreTop':{'Ones':0,'Twos':0,'Threes':0,'Fours':0,'Fives':0,'Sixes':0},
			'scoreBottom':{'Three of a kind':0,'Four of a kind':0,'Full house':0,'Small straight':0, 'Large straight':0,'Yahtzee':0,'Chance':0,'Yahtzee bonus':0},
			'totalScore':{'Sum of upper':0,'Bonus':0,'Total upper':0,'Total bottom':0,'Grand total':0}}

print('Welcome to Yahtzee!')

#set number of players (1-4) and enter names
playerCount=pyip.inputInt(prompt='Enter number of players (1-4):\n', min=1, max=4)
for x in range(playerCount):
	playerDict[pyip.inputStr(prompt='Enter name of player '+str(x+1)+':\n')] = scoringDict

#show current player score card

#roll dice function
def rollDice(dict):
	for i in range(len(dice)):
		if dice[i+1]['keeper']==False:
			dice[i+1]['result']=randint(1,6)
		else:
			dice[i+1]['keeper']==False
	return dice

#keep dice function
def keepDice(dict):
	keepAll = pyip.inputYesNo(prompt='Do you want to keep all of these dice?\n')
	if keepAll == 'no':
		for i in range(len(dice)):
			selectKeepers = pyip.inputYesNo(prompt='Do you want to keep the %s?\n' % (dice[i+1]['result']))
			if selectKeepers == 'no':
				dice[i+1]['keeper']=False
			else:
				dice[i+1]['keeper']=True
	else:
		for i in range(len(dice)):
			dice[i+1]['keeper']=True
	return dice

#each players turn
for player in playerDict:
	print('HERE WE GO! ROUND %s.\n%s your turn. Your current Total Score: %s' % (str(round), player, str(playerDict.get(player,{}).get('totalScore',{}).get('Grand total'))))

	#rollDice, player select dice, second diceRoll of 'keeper'==False dice, get final dice
	rollDice(dice)
	print('FIRST ROLL: %s %s %s %s %s %s' % (dice[1]['result'], dice[2]['result'], dice[3]['result'], dice[4]['result'], dice[5]['result'], dice[6]['result']))
	keepDice(dice)

	rollDice(dice)
	print('SECOND ROLL: %s %s %s %s %s %s' % (dice[1]['result'], dice[2]['result'], dice[3]['result'], dice[4]['result'], dice[5]['result'], dice[6]['result']))
	keepDice(dice)
	
	rollDice(dice)
	print('FINAL ROLL: %s %s %s %s %s %s' % (dice[1]['result'], dice[2]['result'], dice[3]['result'], dice[4]['result'], dice[5]['result'], dice[6]['result']))

#show remaining score card options for current dice (if applicable)
#choose score card option (if applicable)
#reset for next player

#end of available rounds show player score, next player (if applicable)
#end of game show player scores, ranking (winner), and games won tally
#play again?
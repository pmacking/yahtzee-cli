#!python3
import pyinputplus as pyip
import numpy as np
from random import randint
import time

# this is a multiplayer yahtzee game
# instructions: https://www.hasbro.com/common/instruct/Yahtzee.pdf

# general attributes
playerDict={} # {'playerName':({scoreTopDict},{scoreBottomDict},{totalScoreDict}), ...}
dice={1:{'keeper':False,'result':0}, 2:{'keeper':False,'result':0}, 3:{'keeper':False,'result':0}, 4:{'keeper':False,'result':0}, 5:{'keeper':False,'result':0}, 6:{'keeper':False,'result':0}}
scoringDict={'scoreTop':{'Ones':{'ref':1,'score':False},'Twos':{'ref':2,'score':False},'Threes':{'ref':3,'score':False},'Fours':{'ref':4,'score':False},'Fives':{'ref':5,'score':False},'Sixes':{'ref':6,'score':False}},
			'scoreBottom':{'Three of a kind':False,'Four of a kind':False,'Full house':False,'Small straight':False, 'Large straight':False,'Yahtzee':False,'Chance':False,'Yahtzee bonus':False},
			'totalScore':{'Sum of upper':False,'Bonus':False,'Total upper':False,'Total bottom':False,},'Grand total':False}
hyperlink_format = '<a href="{link}">{text}</a>'
scoreSelected=''

# create player dictionary
def createPlayerDict(n):
	for x in range(numberOfPlayers):
		playerDict[pyip.inputStr(prompt='\nEnter name of player '+str(x+1)+':\n')] = scoringDict
	return playerDict

#roll dice function
def rollDice(dice):
	for i in range(len(dice)):
		if dice[i+1]['keeper']==False:
			dice[i+1]['result']=randint(1,6)
		else:
			dice[i+1]['keeper']==False
	return dice

#keep dice function (would be nice to have UI for this)
def keepDice(dice):
	keepAll = pyip.inputYesNo(prompt=('%s do you want to keep ALL of these dice?\n' % (player)))
	if keepAll == 'no':
		for i in range(len(dice)):
			selectKeepers = pyip.inputYesNo(prompt='%s do you want to keep the %s?\n' % (player, dice[i+1]['result']))
			if selectKeepers == 'no':
				dice[i+1]['keeper']=False
			else:
				dice[i+1]['keeper']=True
	else:
		for i in range(len(dice)):
			dice[i+1]['keeper']=True
	return dice

#select scoring after final dice roll of current player
def selectScore(player, diceDict):
	#display only False scoring options
	global scoreSelected
	scoreOptions = []
	for k in playerDict[player]['scoreTop']:
		if playerDict[player]['scoreTop'][k]['score'] == False:
			scoreOptions.append(k)
	for k in playerDict[player]['scoreBottom']:
		if playerDict[player]['scoreBottom'][k] == False:
			scoreOptions.append(k)
	scoreSelected = pyip.inputMenu(scoreOptions)
	#confirm option
	if pyip.inputYesNo(prompt='\n%s are you sure you want to select %s?\n' % (player, scoreSelected)) == 'no':
		selectScore(player, dice)
	return scoreSelected

def calcScore(player, playerDict, diceResults):
	#calculate score based on scoreSelected in selectScore()
	if scoreSelected in playerDict[player]['scoreTop']:
		for n in diceResults:
			if n == playerDict[player]['scoreTop'][scoreSelected]['ref']:
				playerDict[player]['scoreTop'][scoreSelected]['score']+=n
			else:
				playerDict[player]['scoreTop'][scoreSelected]['score']=0

	if scoreSelected == 'Chance':
		playerDict[player]['scoreBottom']['Chance'] = np.sum(diceResults)

	#TODO handle error state where player selects and score is 0
	# Three of a kind
	# Four of a kind
	# Full house
	# Small straight
	# Large straight
	# Yahtzee
	# Yahtzee bonus
	#TODO how to handle totalScore recalculation each round?
	#playerDict[player]['totalScore']['Sum of upper']= #some kind of numpy summation of playerDict[player][scoreTop][x]['score']
	#playerDict[player]['totalScore']['Grand total'] = #some kind of numpy summation of playerDict[player][totalScore][x- Grand Total]
	return playerDict

#YAHTZEE ROUNDS CODE
print('WELCOME TO YAHTZEE!\n %s for the newbs.' % (hyperlink_format.format(link='https://www.hasbro.com/common/instruct/Yahtzee.pdf', text='Yahtzee Rules')))

#set number of players (1-4) and enter names
numberOfPlayers=pyip.inputInt(prompt='\nEnter number of players (1-4):\n', min=1, max=4)
createPlayerDict(numberOfPlayers)

round=1
gameComplete=False
while gameComplete != True:
	print('\nHERE WE GO! ROUND %s.' % (str(round)))
	scoreSelected=''
	for player in playerDict:
		print('\n%s your turn. Your current Total Score: %s.' % (player, str(int(playerDict.get(player,{}).get('Grand total')))))

		#First roll
		time.sleep(1)
		rollDice(dice)
		print('\nFIRST ROLL: %s %s %s %s %s %s' % (dice[1]['result'], dice[2]['result'], dice[3]['result'], dice[4]['result'], dice[5]['result'], dice[6]['result']))
		keepDice(dice)

		#Second roll
		rollDice(dice)
		print('\nSECOND ROLL: %s %s %s %s %s %s' % (dice[1]['result'], dice[2]['result'], dice[3]['result'], dice[4]['result'], dice[5]['result'], dice[6]['result']))
		keepDice(dice)

		#Third and final roll
		rollDice(dice)
		print('\nFINAL ROLL: %s %s %s %s %s %s\n' % (dice[1]['result'], dice[2]['result'], dice[3]['result'], dice[4]['result'], dice[5]['result'], dice[6]['result']))
		diceResults=[dice[1]['result'], dice[2]['result'], dice[3]['result'], dice[4]['result'], dice[5]['result'], dice[6]['result']]
		selectScore(player, dice)
		calcScore(player, playerDict, diceResults)
		print(playerDict)

		for i in range(len(dice)):
			dice[i+1]['keeper']=False
		time.sleep(1)

	round=round+1

#show remaining score card options for current dice (if applicable)
#choose score card option (if applicable)
#reset for next player

#end of available rounds show player score, next player (if applicable)
#end of game show player scores, ranking (winner), and games won tally
#play again?

'''
{'Taya': {'scoreTop': {'Ones': {'ref': 1, 'score': False}, 'Twos': {'ref': 2, 'score': 4},
'Threes': {'ref': 3, 'score': False}, 'Fours': {'ref': 4, 'score': False},
'Fives': {'ref': 5, 'score': False}, 'Sixes': {'ref': 6, 'score': False}},
'scoreBottom': {'Three of a kind': False, 'Four of a kind': False, 'Full house': False,
'Small straight': False, 'Large straight': False, 'Yahtzee': False, 'Chance': False,
'Yahtzee bonus': False}, 'totalScore': {'Sum of upper': False, 'Bonus': False,
'Total upper': False, 'Total bottom': False}, 'Grand total': False},
'Paul': {'scoreTop': {'Ones': {'ref': 1, 'score': False}, 'Twos': {'ref': 2, 'score': 4},
'Threes': {'ref': 3, 'score': False}, 'Fours': {'ref': 4, 'score': False},
'Fives': {'ref': 5, 'score': False}, 'Sixes': {'ref': 6, 'score': False}},
'scoreBottom': {'Three of a kind': False, 'Four of a kind': False, 'Full house': False,
'Small straight': False, 'Large straight': False, 'Yahtzee': False, 'Chance': False,
'Yahtzee bonus': False}, 'totalScore': {'Sum of upper': False, 'Bonus': False,
'Total upper': False, 'Total bottom': False}, 'Grand total': False}}
'''

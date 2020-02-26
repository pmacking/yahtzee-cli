#!python3
import pyinputplus as pyip
import numpy as np
from random import randint
import time

# this is a multiplayer yahtzee game
# instructions: https://www.hasbro.com/common/instruct/Yahtzee.pdf

# general attributes
playerDict={}
diceDict={1:{'keeper':False,'result':0}, 2:{'keeper':False,'result':0}, 3:{'keeper':False,'result':0}, 4:{'keeper':False,'result':0}, 5:{'keeper':False,'result':0}, 6:{'keeper':False,'result':0}}
scoringDict={'scoreTop':{'Ones':{'ref':1,'score':False},'Twos':{'ref':2,'score':False},'Threes':{'ref':3,'score':False},'Fours':{'ref':4,'score':False},'Fives':{'ref':5,'score':False},'Sixes':{'ref':6,'score':False}},
			'scoreBottom':{'Three of a kind':False,'Four of a kind':False,'Full house':False,'Small straight':False, 'Large straight':False,'Yahtzee':False,'Chance':False,'Yahtzee bonus':False},
			'totalScore':{'Sum of upper':False,'Bonus':False,'Total upper':False,'Total bottom':False,},'Grand total':False}
hyperlink_format = '<a href="{link}">{text}</a>'

# create player dictionary via numbers and names of players
def createPlayerDict():
	numberOfPlayers=pyip.inputInt(prompt='\nEnter number of players (1-4):\n', min=1, max=4)
	for x in range(numberOfPlayers):
		playerDict[pyip.inputStr(prompt='\nEnter name of player '+str(x+1)+':\n')] = scoringDict
	return playerDict

#roll dice function
def rollDice(diceDict):
	for i in range(len(diceDict)):
		if diceDict[i+1]['keeper']==False:
			diceDict[i+1]['result']=randint(1,6)
		else:
			diceDict[i+1]['keeper']==False
	return diceDict

#keep diceDict function (would be nice to have UI for this)
def keepDice(diceDict, player):
	keepAll = pyip.inputYesNo(prompt=('%s do you want to keep ALL of these dice?\n' % (player)))
	if keepAll == 'no':
		for i in range(len(diceDict)):
			selectKeepers = pyip.inputYesNo(prompt='%s do you want to keep the %s?\n' % (player, diceDict[i+1]['result']))
			if selectKeepers == 'no':
				diceDict[i+1]['keeper']=False
			else:
				diceDict[i+1]['keeper']=True
	else:
		for i in range(len(diceDict)):
			diceDict[i+1]['keeper']=True
	return diceDict

#select scoring after final dice roll of current player
def selectScore(player, playerDict, diceDict):
	#display only available (False) scoring options in playerDict
	scoreOptions = []
	for k in playerDict[player]['scoreTop']:
		if playerDict[player]['scoreTop'][k]['score'] == False:
			scoreOptions.append(k)
	for k in playerDict[player]['scoreBottom']:
		if playerDict[player]['scoreBottom'][k] == False:
			scoreOptions.append(k)
	scoreSelected = pyip.inputMenu(scoreOptions)
	print(scoreSelected)
	#confirm option
	if pyip.inputYesNo(prompt='\n%s are you sure you want to select %s?\n' % (player, scoreSelected)) == 'no':
		selectScore(player, playerDict, diceDict)
	return playerDict, scoreSelected, diceDict

def calcScore(player, playerDict, scoreSelected, diceResults):
	#calculate score based on scoreSelected in selectScore()
	print(player)
	print(playerDict)
	print(scoreSelected)
	print(diceResults)
	if scoreSelected in playerDict[player]['scoreTop']:
		for n in diceResults:
			if n == playerDict[player]['scoreTop'][scoreSelected]['ref']:
				playerDict[player]['scoreTop'][scoreSelected]['score']+=n
			else:
				playerDict[player]['scoreTop'][scoreSelected]['score']=0

	if scoreSelected == 'Chance':
		playerDict[player]['scoreBottom']['Chance'] = np.sum(diceResults)

	#TODO handle error state where player selects and score is 0 for all options below
	#TODO create below scoring options
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

def resetDice(diceDict):
	for i in range(len(diceDict)):
		diceDict[i+1]['keeper']=False
	time.sleep(1)
	print(diceDict)
	return diceDict

#main yahtzee rounds code
print('WELCOME TO YAHTZEE!\n %s for the newbs.' % (hyperlink_format.format(link='https://www.hasbro.com/common/instruct/Yahtzee.pdf', text='Yahtzee Rules')))

def yahtzeeRounds(playerDict, diceDict, scoringDict): #TODO which argument(s) to pass to this main function?
	round=1
	gameComplete=False
	createPlayerDict()
	while gameComplete != True:
		print('\nHERE WE GO! ROUND %s.' % (str(round)))
		for player in playerDict:
			print('\n%s your turn. Your current Total Score: %s.' % (player, str(int(playerDict.get(player,{}).get('Grand total')))))

			#First roll
			time.sleep(1)
			rollDice(diceDict)
			print('\nFIRST ROLL: %s %s %s %s %s %s' % (diceDict[1]['result'], diceDict[2]['result'], diceDict[3]['result'], diceDict[4]['result'], diceDict[5]['result'], diceDict[6]['result']))
			keepDice(diceDict, player)

			#Second roll
			rollDice(diceDict)
			print('\nSECOND ROLL: %s %s %s %s %s %s' % (diceDict[1]['result'], diceDict[2]['result'], diceDict[3]['result'], diceDict[4]['result'], diceDict[5]['result'], diceDict[6]['result']))
			keepDice(diceDict, player)

			#Third and final roll
			rollDice(diceDict)
			print('\nFINAL ROLL: %s %s %s %s %s %s\n' % (diceDict[1]['result'], diceDict[2]['result'], diceDict[3]['result'], diceDict[4]['result'], diceDict[5]['result'], diceDict[6]['result']))

			diceResults=[diceDict[1]['result'], diceDict[2]['result'], diceDict[3]['result'], diceDict[4]['result'], diceDict[5]['result'], diceDict[6]['result']]

			selectScore(player, playerDict, diceDict)
			calcScore(player, playerDict, scoreSelected, diceResults)
			print(playerDict)
			resetDice(diceDict)

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
yahtzeeRounds(playerDict, diceDict, scoringDict)

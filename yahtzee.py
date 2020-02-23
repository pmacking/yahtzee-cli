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

print('WELCOME TO YAHTZEE!\n %s for the newbs.' % (hyperlink_format.format(link='https://www.hasbro.com/common/instruct/Yahtzee.pdf', text='Yahtzee Rules')))

#set number of players (1-4) and enter names
playerCount=pyip.inputInt(prompt='\nEnter number of players (1-4):\n', min=1, max=4)
for x in range(playerCount):
	playerDict[pyip.inputStr(prompt='\nEnter name of player '+str(x+1)+':\n')] = scoringDict

#show current player score card

#roll dice function
def rollDice(diceDict):
	for i in range(len(dice)):
		if dice[i+1]['keeper']==False:
			dice[i+1]['result']=randint(1,6)
		else:
			dice[i+1]['keeper']==False
	return dice

#keep dice function (would be nice to have UI for this)
def keepDice(diceDict):
	keepAll = pyip.inputYesNo(prompt='\nDo you want to keep all of these dice?\n')
	if keepAll == 'no':
		for i in range(len(dice)):
			selectKeepers = pyip.inputYesNo(prompt='\nDo you want to keep the %s?\n' % (dice[i+1]['result']))
			if selectKeepers == 'no':
				dice[i+1]['keeper']=False
			else:
				dice[i+1]['keeper']=True
	else:
		for i in range(len(dice)):
			dice[i+1]['keeper']=True
	return dice

#function to select scoring for the final dice roll of the current player
def selectScore(diceDict):
	#display only False scoring options
	scoreOptions = []
	for k in playerDict[player]['scoreTop']:
		if playerDict[player]['scoreTop'][k]['score'] == False:
			scoreOptions.append(k)
	for k in playerDict[player]['scoreBottom']:
		if playerDict[player]['scoreBottom'][k] == False:
			scoreOptions.append(k)
	scoreSelect = str(pyip.inputMenu(scoreOptions))
	
	#confirm option
	if pyip.inputYesNo(prompt='\nAre you sure you want to select %s?\n' % (scoreSelect)) == 'no':
		selectScore(dice)
	
	#calculate score based on scoring type selected
	if scoreSelect in playerDict[player]['scoreTop']:
		for n in diceResults:
			if n == playerDict[player]['scoreTop'][scoreSelect]['ref']:
				playerDict[player]['scoreTop'][scoreSelect]['score']+=n
	if scoreSelect == 'Chance':
		playerDict[player]['scoreBottom']['Chance'] = np.sum(diceResults)

	#TODO how to handle totalScore recalculation each round?
	#playerDict[player]['totalScore']['Sum of upper']= #some kind of numpy summation of playerDict[player][scoreTop][x]['score']
	#playerDict[player]['totalScore']['Grand total'] = #some kind of numpy summation of playerDict[player][totalScore][x- Grand Total]

	'''
	* Three of a kind
	* Four of a kind
	* Full house
	* Small straight
	* Large straight
	* Yahtzee
	* Yahtzee bonus
	'''
	#TODO remove below, which is used to check saving scoreSelect to playerDict
	print(playerDict)


	#return score in playerDict

#{'scoreTop':{'Ones':False,'Twos':False,'Threes':False,'Fours':False,'Fives':False,'Sixes':False},
#		'scoreBottom':{'Three of a kind':False,'Four of a kind':False,'Full house':False,
#		'Small straight':False, 'Large straight':False,'Yahtzee':False,'Chance':False,'Yahtzee bonus':False},

#yahtzee rounds code
round=1
roundComplete=False
while roundComplete != True:
	print('\nHERE WE GO! ROUND %s.' % (str(round)))
	for player in playerDict:
		print('%s your turn. Your current Total Score: %s.' % (player, str(int(playerDict.get(player,{}).get('Grand total')))))

		#rollDice, player select dice, second diceRoll of 'keeper'==False dice, get final dice
		time.sleep(1)
		rollDice(dice)
		print('\nFIRST ROLL: %s %s %s %s %s %s' % (dice[1]['result'], dice[2]['result'], dice[3]['result'], dice[4]['result'], dice[5]['result'], dice[6]['result']))
		keepDice(dice)

		rollDice(dice)
		print('\nSECOND ROLL: %s %s %s %s %s %s' % (dice[1]['result'], dice[2]['result'], dice[3]['result'], dice[4]['result'], dice[5]['result'], dice[6]['result']))
		keepDice(dice)
		
		rollDice(dice)
		print('\nFINAL ROLL: %s %s %s %s %s %s\n' % (dice[1]['result'], dice[2]['result'], dice[3]['result'], dice[4]['result'], dice[5]['result'], dice[6]['result']))
		diceResults=[dice[1]['result'], dice[2]['result'], dice[3]['result'], dice[4]['result'], dice[5]['result'], dice[6]['result']]
		selectScore(dice)

		for i in range(len(dice)):
			dice[i+1]['keeper']=False
	
	round=round+1
	time.sleep(1)
#show remaining score card options for current dice (if applicable)
#choose score card option (if applicable)
#reset for next player

#end of available rounds show player score, next player (if applicable)
#end of game show player scores, ranking (winner), and games won tally
#play again?
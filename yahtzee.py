#!python3
import pyinputplus as pyip
import numpy as np
from random import randint
import time

# this is a multiplayer yahtzee game
# instructions: https://www.hasbro.com/common/instruct/Yahtzee.pdf

# global objects
playerDict = {}
diceDict = {1: {'keeper': False, 'result': 0}, 2: {'keeper': False, 'result': 0}, 3: {'keeper': False, 'result': 0}, 4: {'keeper': False, 'result': 0}, 5: {'keeper': False, 'result': 0}, 6: {'keeper': False, 'result': 0}}
scoringDict = {'scoreTop': {'Ones': {'ref': 1, 'score': False}, 'Twos': {'ref': 2, 'score': False}, 'Threes': {'ref': 3, 'score': False}, 'Fours': {'ref': 4, 'score': False}, 'Fives': {'ref': 5, 'score': False}, 'Sixes': {'ref': 6, 'score': False}}, 'scoreBottom': {'Three of a kind': False, 'Four of a kind': False, 'Full house': False, 'Small straight': False, 'Large straight': False, 'Yahtzee': False, 'Chance': False, 'Yahtzee bonus': False}, 'totalScore': {'Sum of upper': False, 'Bonus': False, 'Total upper': False, 'Total bottom': False, }, 'Grand total': False}
hyperlink_format = '<a href="{link}">{text}</a>'
numberOfPlayers = 0
gameComplete = False
scoreSelected = ''


# create player dictionary via numbers and names of players
def createPlayerDict():
    numberOfPlayers = pyip.inputInt(prompt='\nEnter number of players (1-4):\n', min=1, max=4)
    for _ in range(numberOfPlayers):
        playerDict[pyip.inputStr(prompt='\nEnter name of player '+str(_+1)+':\n')] = scoringDict
    return playerDict


# roll dice function
def rollDice(diceDict):
    for i in range(len(diceDict)):
        if diceDict[i+1]['keeper'] is False:
            diceDict[i+1]['result'] = randint(1,6)
    return diceDict


# keep diceDict function (would be nice to have UI for this)
def keepDice(diceDict, player):
    keepAll = pyip.inputYesNo(prompt=(f'{player} do you want to KEEP ALL of these dice?\n'))
    if keepAll == 'no':
        rerollAll = pyip.inputYesNo(prompt=(f'{player} do you want to REROLL ALL of these dice?'))
        if rerollAll == 'no':
            for i in range(len(diceDict)):
                selectKeepers = pyip.inputYesNo(prompt='%s do you want to keep the %s?\n' % (player, diceDict[i+1]['result']))
                if selectKeepers == 'no':
                    diceDict[i+1]['keeper'] = False
                else:
                    diceDict[i+1]['keeper'] = True
        else:
            for i in range(len(diceDict)):
                diceDict[i+1]['keeper'] = False
    else:
        for i in range(len(diceDict)):
            diceDict[i+1]['keeper'] = True
    return diceDict


# select scoring after final dice roll of current player
def selectScore(player, playerDict, diceDict, scoreSelected):
    # present and select available (False) scoring options in playerDict
    scoreOptions = []
    for k in playerDict[player]['scoreTop']:
        if playerDict[player]['scoreTop'][k]['score'] is False:
            scoreOptions.append(k)
    for k in playerDict[player]['scoreBottom']:
        if playerDict[player]['scoreBottom'][k] is False:
            scoreOptions.append(k)
    scoreSelected = pyip.inputMenu(scoreOptions)
    # confirm selection
    if pyip.inputYesNo(prompt='\n%s are you sure you want to select %s?\n' % (player, scoreSelected)) == 'no':
        selectScore(player, playerDict, diceDict, scoreSelected)
    return playerDict, scoreSelected, diceDict


def calcScore(player, playerDict, scoreSelected, diceResults):
    # calculate score based on scoreSelected in selectScore()
    print('print before calcScore')
    print(player)
    print(playerDict)
    print(diceResults)
    print(scoreSelected)
    if scoreSelected in playerDict[player]['scoreTop']:
        print(playerDict[player]['scoreTop'])
        for n in diceResults:
            if n == playerDict[player]['scoreTop'][scoreSelected]['ref']:
                playerDict[player]['scoreTop'][scoreSelected]['score'] += n
                print('if statmement')
                print(playerDict)
            else:
                playerDict[player]['scoreTop'][scoreSelected]['score'] += 0
                print('else statmement')
                print(playerDict)

    if scoreSelected == 'Chance':
        playerDict[player]['scoreBottom']['Chance'] = np.sum(diceResults)

    # TODO handle err state where player selects & score is 0 for options below
    # TODO create below scoring options
    # Three of a kind
    # Four of a kind
    # Full house
    # Small straight
    # Large straight
    # Yahtzee
    # Yahtzee bonus
    # TODO how to handle totalScore recalculation each round?
    # playerDict[player]['totalScore']['Sum of upper']= #some kind of numpy summation of playerDict[player][scoreTop][x]['score']
    # playerDict[player]['totalScore']['Grand total'] = #some kind of numpy summation of playerDict[player][totalScore][x- Grand Total]
    print('playerDict and diceResults AFTER calcScore')
    print(player)
    print(playerDict)
    print(diceResults)
    return playerDict


def resetDice(diceDict):
    for i in range(len(diceDict)):
        diceDict[i+1]['keeper'] = False
    time.sleep(1)
    return diceDict


# main yahtzee rounds code for managing rolls, dice, players, scores
def yahtzeeRounds():  # rm for arg testing: playerDict, diceDict, scoringDict
    round = 1
    while gameComplete is not True:
        print(f'HERE WE GO! ROUND {round}.')
        for player in playerDict:
            print('\n%s your turn. Your current Total Score: %s.' % (player, str(int(playerDict.get(player, {}).get('Grand total')))))

            # First roll
            time.sleep(1)
            diceDict = rollDice(diceDict)
            print('\nFIRST ROLL: %s %s %s %s %s %s' % (diceDict[1]['result'], diceDict[2]['result'], diceDict[3]['result'], diceDict[4]['result'], diceDict[5]['result'], diceDict[6]['result']))
            diceDict = keepDice(diceDict, player)

            # Second roll
            diceDict = rollDice(diceDict)
            print('\nSECOND ROLL: %s %s %s %s %s %s' % (diceDict[1]['result'], diceDict[2]['result'], diceDict[3]['result'], diceDict[4]['result'], diceDict[5]['result'], diceDict[6]['result']))
            diceDict = keepDice(diceDict, player)

            # Third and final roll
            diceDict = rollDice(diceDict)
            print('\nFINAL ROLL: %s %s %s %s %s %s\n' % (diceDict[1]['result'], diceDict[2]['result'], diceDict[3]['result'], diceDict[4]['result'], diceDict[5]['result'], diceDict[6]['result']))

            diceResults = [diceDict[1]['result'], diceDict[2]['result'], diceDict[3]['result'], diceDict[4]['result'], diceDict[5]['result'], diceDict[6]['result']]

            playerDict, scoreSelected, diceDict = selectScore(player, playerDict, diceDict, scoreSelected)
            playerDict = calcScore(player, playerDict, scoreSelected, diceResults)

            # cleanup and reset for next player (or round if 1 player)
            print('yahtzeeRounds() cleanup')
            print(playerDict)
            diceDict = resetDice(diceDict)
            scoreSelected = ''

        round = round+1
# show remaining score card options for current dice (if applicable)
# choose score card option (if applicable)
# reset for next player
# end of available rounds show player score, next player (if applicable)
# end of game show player scores, ranking (winner), and games won tally
# play again?


# main game init
yahtzeeRulesUrl = hyperlink_format.format(link='https://www.hasbro.com/common/instruct/Yahtzee.pdf', text='Yahtzee Rules')
print(f'WELCOME TO YAHTZEE!\n {yahtzeeRulesUrl} for the newbs.')

print(playerDict)
createPlayerDict()
print(playerDict)
yahtzeeRounds()  # rm args for testing: playerDict, diceDict, scoringDict

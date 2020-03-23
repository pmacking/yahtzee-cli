#!python3

import pyinputplus as pyip
from random import randint
import time

# Usage: this is a multiplayer yahtzee game

# global objects
playerDict = {}
diceDict = {1: {'keeper': False, 'result': 0}, 2: {'keeper': False, 'result': 0}, 3: {'keeper': False, 'result': 0}, 4: {'keeper': False, 'result': 0}, 5: {'keeper': False, 'result': 0},}
hyperlink_format = '<a href="{link}">{text}</a>'
numberOfPlayers = 0
gameComplete = False


# create player dictionary via numbers and names of players
def createPlayerDict(playerDict):
    '''
    Creates playerDict containing player(s) scoring dictionary
    Args: None
    Returns: playerDict
    '''
    numberOfPlayers = pyip.inputInt(prompt='\nEnter number of players (1-4):\n', min=1, max=4)
    for _ in range(numberOfPlayers):
        playerDict[pyip.inputStr(prompt='\nEnter name of player '+str(_+1)+':\n')] = {'scoreTop': {'Ones': {'ref': 1, 'score': False}, 'Twos': {'ref': 2, 'score': False}, 'Threes': {'ref': 3, 'score': False}, 'Fours': {'ref': 4, 'score': False}, 'Fives': {'ref': 5, 'score': False}, 'Sixes': {'ref': 6, 'score': False}}, 'scoreBottom': {'Three of a kind': False, 'Four of a kind': False, 'Full house': False, 'Small straight': False, 'Large straight': False, 'Yahtzee': False, 'Chance': False, 'Yahtzee bonus': False}, 'totalScore': {'Sum of upper': False, 'Bonus': False, 'Total upper': False, 'Total bottom': False, }, 'Grand total': False}
    return playerDict


# roll dice function
def rollDice():
    '''
    Generate random value between 1 and 6 for each non keeper dice
    Args: None
    Returns: diceDict
    '''
    for i in range(len(diceDict)):
        if diceDict[i+1]['keeper'] is False:
            diceDict[i+1]['result'] = randint(1, 6)
    return diceDict


# keep diceDict function (would be nice to have UI for this)
def keepDice(diceDict, player):
    '''
    Allows player to select which dice they would like to keep or reroll
    Args: diceDict, player
    Returns: diceDict
    '''
    keepAll = pyip.inputYesNo(prompt=(f'{player} do you want to KEEP ALL of these dice?\n'))
    if keepAll == 'no':
        rerollAll = pyip.inputYesNo(prompt=(f'{player} do you want to REROLL ALL of these dice?\n'))
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
    '''
    Allows player to select which scoring option to apply dice results to within calcScore.
    Args: player, playerDict, diceDict, scoreSelected
    Returns: playerDict, scoreSelected, diceDict
    '''
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


def calcScore(player, playerDict, scoreSelected, diceDict):
    """
    Calculates score based on the score option in selectScore() and dice result
    Args: player, playerDict, scoreSelected, diceDict
    Returns: playerDict
    """
    diceList = [diceDict[1]['result'], diceDict[2]['result'], diceDict[3]['result'], diceDict[4]['result'], diceDict[5]['result'], ]

    # calc all 'ScoreTop' options
    if scoreSelected in playerDict[player]['scoreTop']:
        for d in diceDict.values():
            if d['result'] == playerDict[player]['scoreTop'][scoreSelected]['ref']:
                playerDict[player]['scoreTop'][scoreSelected]['score'] += d['result']
            else:
                playerDict[player]['scoreTop'][scoreSelected]['score'] += 0
        print(f"\nScore for {scoreSelected}: {playerDict[player]['scoreTop'][scoreSelected]['score']}")

    # calculate score for 'Three of a kind'
    elif scoreSelected == 'Three of a kind':
        if len(set(diceList)) <= (len(diceList)-2):
            print(f'\nScore for {scoreSelected}: {sum(diceList)}')
            playerDict[player]['scoreBottom'][scoreSelected] = sum(diceList)
        else:
            print(f'\nYou did not roll {scoreSelected}, your score for {scoreSelected}: 0')
            playerDict[player]['scoreBottom'][scoreSelected] = 0

    # calculate score for 'Four of a kind'
    elif scoreSelected == 'Four of a kind':
        if len(set(diceList)) <= (len(diceList)-3):
            print(f'\nScore for {scoreSelected}: {sum(diceList)}')
            playerDict[player]['scoreBottom'][scoreSelected] = sum(diceList)
        else:
            print(f'\nYou did not roll {scoreSelected}, your score for {scoreSelected}: 0')
            playerDict[player]['scoreBottom'][scoreSelected] = 0

    # calculate score for 'Full house'
    elif scoreSelected == 'Full house':
        if len(set(diceList)) == 2 and len([d for d in diceList if diceList.count(d) == 3]) == 3:
            print(f"\nScore for {scoreSelected}: 25")
            playerDict[player]['scoreBottom'][scoreSelected] = 25
        else:
            print(f"\nYou did not roll {scoreSelected}, your score for {scoreSelected}: 0")
            playerDict[player]['scoreBottom'][scoreSelected] = 0

    # calculate score for 'Small straight'
    elif scoreSelected == 'Small straight':
        if len(set(diceList)) == 4:
            print(f"\nScore for {scoreSelected}: 30")
            playerDict[player]['scoreBottom'][scoreSelected] = 30
        else:
            print(f"\nYou did not roll {scoreSelected}, your score for {scoreSelected}: 0")
            playerDict[player]['scoreBottom'][scoreSelected] = 0

    # calculate score for 'Large straight'
    elif scoreSelected == 'Large straight':
        if len(set(diceList)) == 5:
            print(f"\nScore for {scoreSelected}: 40")
            playerDict[player]['scoreBottom'][scoreSelected] = 40
        else:
            print(f"\nYou did not roll {scoreSelected}, your score for {scoreSelected}: 0")
            playerDict[player]['scoreBottom'][scoreSelected] = 0

    # calculate score for 'Yahtzee'
    elif scoreSelected == 'Yahtzee':
        if len(set(diceList)) == 1:
            print(f"\nScore for {scoreSelected}: 50")
            playerDict[player]['scoreBottom'][scoreSelected] = 50
        else:
            print(f"\nYou did not roll {scoreSelected}, your score for {scoreSelected}: 0")
            playerDict[player]['scoreBottom'][scoreSelected] = 0
    # calculate score for 'Chance'
    elif scoreSelected == 'Chance':
        print(f"\nScore for {scoreSelected}: {sum(diceList)}")
        playerDict[player]['scoreBottom'][scoreSelected] = sum(diceList)

    # TODO: fix yahtzee bonus so user cannot select until after yahtzee has been selected first (and not a 0 entry for yahtzee)
    # Yahtzee bonus
    elif scoreSelected == 'Yahtzee bonus':
        if len(set(diceList)) == 1:
            print(f"\nScore for {scoreSelected}: 100")
            playerDict[player]['scoreBottom'][scoreSelected] = 100
        else:
            print(f"\nYou did not roll {scoreSelected}, your score for {scoreSelected}: 0")
            playerDict[player]['scoreBottom'][scoreSelected] = 0

    # TODO: how to handle totalScore recalculation each round?
    #     'totalScore': {'Sum of upper': False, 'Bonus': False, 'Total upper': False, 'Total bottom': False}, 'Grand total': False},
    return playerDict


def resetDice(diceDict):
    '''
    Resets dice to keeper = False before next player (or round if one player)
    Args: diceDict
    Returns: diceDict
    '''
    for i in range(len(diceDict)):
        diceDict[i+1]['keeper'] = False
    time.sleep(1)
    return diceDict


# main yahtzee rounds code for managing rolls, dice, players, scores
def yahtzeeRounds(playerDict, diceDict):
    '''
    Main block dictating series of events for each round
    Args: playerDict, diceDict
    Returns: None
    '''
    round = 1
    while gameComplete is not True:
        print(f'\nHERE WE GO! ROUND {round}.')
        for player in playerDict:
            scoreSelected = ''
            print('\n%s your turn. Your current Total Score: %s.' % (player, str(int(playerDict.get(player, {}).get('Grand total')))))

            # TODO: Display scoringDict values so player aware of options

            # First roll
            time.sleep(1)
            diceDict = rollDice()
            print(f"\nFIRST ROLL: {diceDict[1]['result']}, {diceDict[2]['result']}, {diceDict[3]['result']}, {diceDict[4]['result']}, {diceDict[5]['result']}")
            diceDict = keepDice(diceDict, player)

            # Second roll
            diceDict = rollDice()
            print(f"\nSECOND ROLL: {diceDict[1]['result']}, {diceDict[2]['result']}, {diceDict[3]['result']}, {diceDict[4]['result']}, {diceDict[5]['result']}")
            diceDict = keepDice(diceDict, player)

            # Third and final roll
            diceDict = rollDice()
            print(f"\nFINAL ROLL: {diceDict[1]['result']}, {diceDict[2]['result']}, {diceDict[3]['result']}, {diceDict[4]['result']}, {diceDict[5]['result']}")

            # REMOVE WHEN FINISHED TESTING: forcing dice results for calcScore
            # diceDict = {1: {'keeper': True, 'result': 1}, 2: {'keeper': True, 'result': 1}, 3: {'keeper': True, 'result': 1}, 4: {'keeper': True, 'result': 1}, 5: {'keeper': True, 'result': 6}, }

            playerDict, scoreSelected, diceDict = selectScore(player, playerDict, diceDict, scoreSelected)
            playerDict = calcScore(player, playerDict, scoreSelected, diceDict)
            print(playerDict)
            print(diceDict)

            # reset dice for next player (or next round if 1 player)
            diceDict = resetDice(diceDict)

        round = round+1
# TODO: end of available rounds show player score, next player (if applicable)
# TODO: play again
# TODO: end of game show player scores, ranking (winner), and games won tally


# Starting the game stack
if __name__ == "__main__":
    yahtzeeRulesUrl = hyperlink_format.format(link='https://www.hasbro.com/common/instruct/Yahtzee.pdf', text='Yahtzee Rules')
    print(f'WELCOME TO YAHTZEE!\n {yahtzeeRulesUrl} for first timers.')

    createPlayerDict(playerDict)
    yahtzeeRounds(playerDict, diceDict)

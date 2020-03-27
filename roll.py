#! python3

from random import randint
import pyinputplus as pyip


class Roll:
    def __init__(self, name):
        '''
        Class containing diceDict, and methods for rolling/keeping dice
        '''
        self.name = name
        self._currentDiceList = []
        self._keeperDiceList = []

    # This section outlines dice roll actions
    def rollDice(self):
        '''
        Method that determines the first dice roll
        '''
        self._keeperDiceList.clear()
        self._currentDiceList = [randint(1, 6) for d in range(5)]
        print(f'First roll: {self._currentDiceList}\n')
        return self._currentDiceList

    def keepDice(self):
        '''
        Method that keeps particular dice from current rolled dice
        '''
        keepAll = pyip.inputYesNo(prompt=(f'Do you want to KEEP ALL dice?\n'))

        if keepAll == 'no':
            reRollAll = pyip.inputYesNo(prompt=(f'Do you want to REROLL ALL dice?\n'))

            if reRollAll == 'no':
                keepSome = input('Enter the dice you would like to keep (ex: 4, 5):\n')
                if keepSome == '':
                    return self._currentDiceList

                keepSomeSplit = keepSome.split(', ')
                keepSomeSplitInt = [int(d) for d in keepSomeSplit]

                for d in keepSomeSplitInt:
                    if d in self._currentDiceList:
                        self._currentDiceList.remove(d)
                        self._keeperDiceList.append(d)

                return self._currentDiceList

            else:
                return self._currentDiceList

        else:
            self._keeperDiceList = [d for d in self._currentDiceList]
            self._currentDiceList.clear()
            return self._currentDiceList

    def reRollDice(self, diceList):
        '''
        Method that rolls another time
        '''
        self._currentDiceList = [randint(1,6) for d in range(0, (len(diceList)))]
        # adds the rerolled current dice to the keepers and clears keepers
        self._currentDiceList = self._currentDiceList + self._keeperDiceList
        self._keeperDiceList.clear()
        print(f'\nSecond roll: {self._currentDiceList}\n')
        return self._currentDiceList

    def finalRollDice(self, diceList):
        '''
        Method that rolls dice a final time
        '''
        self._currentDiceList = [randint(1,6) for d in range(0, (len(diceList)))]
        # adds the rerolled current dice to the keepers and clears keepers
        self._currentDiceList = self._currentDiceList + self._keeperDiceList
        self._keeperDiceList.clear()
        print(f'\nFinal roll: {self._currentDiceList}\n')

        # makes keepers list identical to current list
        for d in diceList:
            self._keeperDiceList.append(d)

    def getCurrentDice(self):
        '''
        Returns the current dice restuls
        '''
        return self._currentDiceList

    def getKeeperDice(self):
        '''
        Returns keeper dice list
        '''
        return self._keeperDiceList

    # This section of methods checks scoring of rolled dice

    def checkSingles(self, diceList, referenceValue):
        '''
        Checks the value of selected singles and updates scoring dictionary
        returns bool
        '''
        checkSinglesScore = 0
        for dice in diceList:
            if dice == referenceValue:
                checkSinglesScore += dice
        return checkSinglesScore

    def checkThreeOfAKind(self, diceList):
        '''
        Checks if there are three of a kind, and adds all dice total to score
        returns bool
        '''
        if len(set(diceList)) <= (len(diceList)-2):
            return True
        return False

    def checkFourOfAKind(self, diceList):
        '''
        Checks if there are four of a kind, and adds all dice total to score
        returns bool
        '''
        if len(set(diceList)) <= (len(diceList)-3):
            return True
        return False

    def checkFullHouse(self, diceList):
        '''
        Checks for full house (triple, double), and adds 25 to score
        returns bool
        '''
        if len(set(diceList)) == 2 and len([d for d in diceList if diceList.count(d) == 3]) == 3:
            return True
        return False

    def checkSmallStraight(self, diceList):
        '''
        Checks for small straight (4 sequential), and adds 30 to score
        returns bool
        '''
        if len(set(diceList)) == 4:
            return True
        return False

    def checkLargeStraight(self, diceList):
        '''
        Checks for large straight (5 sequential), and adds 35 to score
        returns bool
        '''
        if len(set(diceList)) == 5:
            return True
        return False


    def checkYahtzee(self, diceList):
        '''
        Checks for yahtzee (five of a kind), and adds 50 to score
        '''
        if len(set(diceList)) == 1:
            return True
        return False

    def addChance(self, diceList):
        '''
        Adds the total dice score to scoring Dict
        returns bool
        '''
        return sum(diceList)


    def checkYahtzeeBonus(self, diceList):
        '''
        If yahtzee has been scored, adds 50 to score
        returns bool
        '''
        # TODO: implement check for first yahtzee before bonus
        if len(set(diceList)) == 1:
            return True
        return False

# THIS SECTION CONTAINS OLD CODE TO SKETCH FROM

# keep diceDict function (would be nice to have UI for this)
# def keepDice(diceDict, player):
#     '''
#     Allows player to select which dice they would like to keep or reroll
#     Args: diceDict, player
#     Returns: diceDict
#     '''
#     keepAll = pyip.inputYesNo(prompt=(f'{player} do you want to KEEP ALL of these dice?\n'))
#     if keepAll == 'no':
#         rerollAll = pyip.inputYesNo(prompt=(f'{player} do you want to REROLL ALL of these dice?\n'))
#         if rerollAll == 'no':
#             diceList = [diceDict[1], diceDict[2], diceDict[3], diceDict[4], diceDict[5], ]
#             keepSome = input('Enter the dice you would like to keep (ex: 4, 5):')
#             keepSomeSplit = keepSome.split(', ')
#             if keepSome = '':
#                 for i in range(len(diceDict)):
#                     diceDict[i+1]['keeper'] = False
#             keepSomeSplitInt = [int(d) for d in keepSomeSplit]
#             for keep in keepSomeSplitInt:
#                 for dice in diceList:
#                     if keep == dice['result']:
#                         dice['keeper'] = True
#         else:
#             for i in range(len(diceDict)):
#                 diceDict[i+1]['keeper'] = False
#     else:
#         for i in range(len(diceDict)):
#             diceDict[i+1]['keeper'] = True
#     return diceDict

def calcScore(player, playerDict, scoreSelected, diceDict):
    """
    Calc score based on the score option in selectScore() and diceDict result
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
    # elif scoreSelected == 'Three of a kind':
    #     if len(set(diceList)) <= (len(diceList)-2):
    #         print(f'\nScore for {scoreSelected}: {sum(diceList)}')
    #         playerDict[player]['scoreBottom'][scoreSelected] = sum(diceList)
    #     else:
    #         print(f'\nYou did not roll {scoreSelected}, your score for {scoreSelected}: 0')
    #         playerDict[player]['scoreBottom'][scoreSelected] = 0

    # calculate score for 'Four of a kind'
    # elif scoreSelected == 'Four of a kind':
    #     if len(set(diceList)) <= (len(diceList)-3):
    #         print(f'\nScore for {scoreSelected}: {sum(diceList)}')
    #         playerDict[player]['scoreBottom'][scoreSelected] = sum(diceList)
    #     else:
    #         print(f'\nYou did not roll {scoreSelected}, your score for {scoreSelected}: 0')
    #         playerDict[player]['scoreBottom'][scoreSelected] = 0

    # calculate score for 'Full house'
    # elif scoreSelected == 'Full house':
    #     if len(set(diceList)) == 2 and len([d for d in diceList if diceList.count(d) == 3]) == 3:
    #         print(f"\nScore for {scoreSelected}: 25")
    #         playerDict[player]['scoreBottom'][scoreSelected] = 25
    #     else:
    #         print(f"\nYou did not roll {scoreSelected}, your score for {scoreSelected}: 0")
    #         playerDict[player]['scoreBottom'][scoreSelected] = 0

    # calculate score for 'Small straight'
    # elif scoreSelected == 'Small straight':
    #     if len(set(diceList)) == 4:
    #         print(f"\nScore for {scoreSelected}: 30")
    #         playerDict[player]['scoreBottom'][scoreSelected] = 30
    #     else:
    #         print(f"\nYou did not roll {scoreSelected}, your score for {scoreSelected}: 0")
    #         playerDict[player]['scoreBottom'][scoreSelected] = 0

    # calculate score for 'Large straight'
    # elif scoreSelected == 'Large straight':
    #     if len(set(diceList)) == 5:
    #         print(f"\nScore for {scoreSelected}: 40")
    #         playerDict[player]['scoreBottom'][scoreSelected] = 40
    #     else:
    #         print(f"\nYou did not roll {scoreSelected}, your score for {scoreSelected}: 0")
    #         playerDict[player]['scoreBottom'][scoreSelected] = 0

    # calculate score for 'Yahtzee'
    # elif scoreSelected == 'Yahtzee':
    #     if len(set(diceList)) == 1:
    #         print(f"\nScore for {scoreSelected}: 50")
    #         playerDict[player]['scoreBottom'][scoreSelected] = 50
    #         # introduce 'Yahtzee bonus' as new selectScore option
    #         playerDict[player]['scoreBottom']['Yahtzee bonus'] = False
    #     else:
    #         print(f"\nYou did not roll {scoreSelected}, your score for {scoreSelected}: 0")
    #         playerDict[player]['scoreBottom'][scoreSelected] = 0

    # # calculate score for 'Chance'
    # elif scoreSelected == 'Chance':
    #     print(f"\nScore for {scoreSelected}: {sum(diceList)}")
    #     playerDict[player]['scoreBottom'][scoreSelected] = sum(diceList)

    # Yahtzee bonus (only available when player scores a Yahtzee)
    # elif scoreSelected == 'Yahtzee bonus':
    #     if len(set(diceList)) == 1:
    #         print(f"\nScore for {scoreSelected}: 100")
    #         playerDict[player]['scoreBottom'][scoreSelected] = 100
    #     else:
    #         print(f"\nYou did not roll {scoreSelected}, your score for {scoreSelected}: 0")
    #         playerDict[player]['scoreBottom'][scoreSelected] = 0

    # TODO: how to handle totalScore recalculation each round?
    #     'totalScore': {'Sum of upper': False, 'Bonus': False, 'Total upper': False, 'Total bottom': False},
    # 'Grand total': False},
    return playerDict

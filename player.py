#! python3


class Player:
    def __init__(self, name):
        self.name = name

        self._topScore = 0
        self._topBonusScore = 0
        self._totalTopScore = 0
        self._totalBottomScore = 0
        self._grandTotalScore = 0

    def addScoreDict(self, scoreSelected, score):
        '''
        Adds score to the scoring dictionary for the player
        '''
        self._scoreDict[scoreSelected] = score

    def addTopScore(self, score):
        '''
        Adds rolled score to the top score
        '''
        self._topScore += score

    def addTopBonusScore(self):
        '''
        Checks the top score and if at the bonus threshold 63, adds bonus of 50
        '''
        bonusThreshold = 63

        if self.getTopScore() >= bonusThreshold:
            self._scoreDict['bonus'] = 50
        else:
            self._scoreDict['bonus'] = 0

        self._topBonusScore = self._scoreDict['bonus']

    def getTopScore(self):
        '''
        Returns current top score
        '''
        return self._topScore

    def printScoreDict(self):
        '''
        Prints the scoring dictionary for the player
        '''
        for key, value in self._scoreDict.items():
            print(f'{key}: {value}')

#     def createPlayerDict(playerDict):
#     '''
#     Creates playerDict containing player(s) scoring dictionary
#     Args: None
#     Returns: playerDict
#     '''
#     numberOfPlayers = pyip.inputInt(prompt='\nEnter number of players (1-4):\n', min=1, max=4)
#     for _ in range(numberOfPlayers):
#         playerDict[pyip.inputStr(prompt='\nEnter name of player '+str(_+1)+':\n')] = {'scoreTop': {'Ones': {'ref': 1, 'score': False}, 'Twos': {'ref': 2, 'score': False}, 'Threes': {'ref': 3, 'score': False}, 'Fours': {'ref': 4, 'score': False}, 'Fives': {'ref': 5, 'score': False}, 'Sixes': {'ref': 6, 'score': False}}, 'scoreBottom': {'Three of a kind': False, 'Four of a kind': False, 'Full house': False, 'Small straight': False, 'Large straight': False, 'Yahtzee': False, 'Chance': False, 'Yahtzee bonus': 0}, 'totalScore': {'Sum of upper': False, 'Bonus': False, 'Total upper': False, 'Total bottom': False, }, 'Grand total': 0}
#     return playerDict

#     # select scoring after final dice roll of current player
# def selectScore(player, playerDict, diceDict, scoreSelected):
#     '''
#     Allows player to select which scoring option to apply dice results to within calcScore.
#     Args: player, playerDict, diceDict, scoreSelected
#     Returns: playerDict, scoreSelected, diceDict
#     '''
#     # present and select available (False) scoring options in playerDict
#     doubleCheck = 0
#     while doubleCheck == 0:
#         scoreOptions = []
#         for k in playerDict[player]['scoreTop']:
#             if playerDict[player]['scoreTop'][k]['score'] is False:
#                 scoreOptions.append(k)
#         for k in playerDict[player]['scoreBottom']:
#             if playerDict[player]['scoreBottom'][k] is False:
#                 scoreOptions.append(k)
#         scoreSelected = pyip.inputMenu(scoreOptions, numbered=True)
#         # confirm selection
#         if pyip.inputYesNo(prompt=f"\n{player} are you sure you want to select {scoreSelected}?\n") == 'yes':
#             doubleCheck = 1
#     return playerDict, scoreSelected, diceDict

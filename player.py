#! python3
import pyinputplus as pyip


class Player:
    def __init__(self, name):
        self.name = name
        # scoring dictionaries
        self._scoreDict = {
            'ones': False, 'twos': False, 'threes': False, 'fours': False,
            'fives': False, 'sixes': False, 'three of a kind': False,
            'four of a kind': False, 'full house': False,
            'small straight': False, 'large straight': False, 'yahtzee': False,
            'chance': False, 'yahtzee bonus': False,
            }

        self._topScore = 0
        self._topBonusScore = 0
        self._totalTopScore = 0
        self._totalBottomScore = 0
        self._grandTotalScore = 0

    def selectScore(self):
        '''
        Allows player to select the scoring option for final dice roll
        '''
        scoreOptions = []
        doubleCheck = False

        # build list of scoring options from player's scoring dictionary
        while doubleCheck is False:

            for i, option in enumerate(self._scoreDict):
                if self._scoreDict[option] is False:
                    scoreOptions.append(option)

            checkYahtzeeBonus = False

            while checkYahtzeeBonus is False:
                scoreSelected = pyip.inputMenu(scoreOptions, numbered=True, blank=True)

                # inputMenu outputs single list item if keyword blank=True.
                # The below validates user doesn't input blank
                if scoreSelected == '':
                    print('\nPlease select a valid score option:\n')

                # validates yahtzee is selected before yahtzee bonus
                else:
                    if scoreSelected == 'yahtzee bonus' and self._scoreDict['yahtzee'] is False:
                        print('\nYou must score yahtzee before yahtzee bonus. Please select another option:\n')
                    else:
                        checkYahtzeeBonus = True

            # confirm option selection
            if pyip.inputYesNo(prompt=f"\n{self.name.upper()} are you sure you want to select {scoreSelected}?\n") == 'yes':
                doubleCheck = True

        return scoreSelected

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

        if self._topScore >= bonusThreshold and self._topBonusScore == 0:
            self._topBonusScore = 35

    def printStackedScoreDict(self):
        '''
        Prints the scoring dictionary for the player
        '''
        for key, value in self._scoreDict.items():
            if value is False:
                print(f'{key.rjust(15)}: -')
            else:
                print(f'{key.rjust(15)}: {value*1}')

    def getTopScore(self):
        '''
        Prints the top score (before bonus)
        '''
        return f'Top Score: '.rjust(20) + f'{self._topScore}'

    def getTopBonusScore(self):
        '''
        Prints the top bonus score
        '''
        return f'Top Bonus Score: '.rjust(20) + f'{self._topBonusScore}'

    def getTotalTopScore(self):
        '''
        Prints the total top score for the player
        '''
        return f'Total Top Score: '.rjust(20) + f'{self._totalTopScore}'

    def getTotalBottomScore(self):
        '''
        Prints the total top score for the player
        '''
        return f'Total Bottom Score: '.rjust(20) + f'{self._totalBottomScore}'

    def getGrandTotalScore(self):
        '''
        Prints the total top score for the player
        '''
        return f'GRAND TOTAL: '.rjust(20) + f'{self._grandTotalScore}\n'

    def getNameAndGrandTotalScore(self):
        '''
        returns player name and grand total score
        '''
        return f'{self.name}', f'{self._grandTotalScore}'

    def resetAllScores(self):
        '''
        clears all scores for new round
        '''

        # resets scoreDict values to False
        for i, k in enumerate(self._scoreDict):
            self._scoreDict[k] = False

        # resets scores to 0
        self._topScore = 0
        self._topBonusScore = 0
        self._totalTopScore = 0
        self._totalBottomScore = 0
        self._grandTotalScore = 0

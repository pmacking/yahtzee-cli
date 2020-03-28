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

            # remove yahtzee bonus if yahtzee hasn't been scored yet
            if self._scoreDict['yahtzee'] is False:
                scoreOptions.remove('yahtzee bonus')

            # let player select option
            scoreSelected = pyip.inputMenu(scoreOptions, numbered=True)
            # confirm selection
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

    def printScoreDict(self):
        '''
        Prints the scoring dictionary for the player
        '''
        for key, value in self._scoreDict.items():
            if value is False:
                print(f'{key.rjust(15)}: -')
            else:
                print(f'{key.rjust(15)}: {value*1}')

    def printTopScore(self):
        '''
        Prints the top score (before bonus)
        '''
        print(f'Top Score: '.rjust(20) + f'{self._topScore}')

    def printTopBonusScore(self):
        '''
        Prints the top bonus score
        '''
        print(f'Top Bonus Score: '.rjust(20) + f'{self._topBonusScore}')

    def printTotalTopScore(self):
        '''
        Prints the total top score for the player
        '''
        print(f'Total Top Score: '.rjust(20) + f'{self._totalTopScore}')

    def printTotalBottomScore(self):
        '''
        Prints the total top score for the player
        '''
        print(f'Total Bottom Score: '.rjust(20) + f'{self._totalBottomScore}')

    def printGrandTotalScore(self):
        '''
        Prints the total top score for the player
        '''
        print(f'GRAND TOTAL: '.rjust(20) + f'{self._grandTotalScore}\n')

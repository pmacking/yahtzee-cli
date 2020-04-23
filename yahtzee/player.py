#! python3

"""
This module controls player instantiation and score keeping.

github.com/pmacking/player.py
"""

import pyinputplus as pyip


class Player:
    """
    Objects instantiated by the :class:`Player <Player>` can be called to
    create players and influence scores.
    """
    def __init__(self, name):
        self.name = name
        self.scoreDict = {
            'ones': False, 'twos': False, 'threes': False, 'fours': False,
            'fives': False, 'sixes': False, 'three of a kind': False,
            'four of a kind': False, 'full house': False,
            'small straight': False, 'large straight': False, 'yahtzee': False,
            'chance': False, 'yahtzee bonus': False,
            }
        self.topScore = 0
        self.topBonusScore = 0
        self.topBonusScoreDelta = 0
        self.totalTopScore = 0
        self.totalBottomScore = 0
        self.grandTotalScore = 0

        self.scoreOptions = []

    def __repr__(self):
        return (f"{self.__class__.__name__}("
                f"{self.name}, {self.scoreDict!r}, "
                f"{self.topScore!r}, {self.topBonusScore!r}, "
                f"{self.totalBottomScore!r}, {self.grandTotalScore!r})")

    def getScoreOptions(self):
        """
        Gets list of non-False scoring options from scoreDict.

        :returns: Score options list.
        """
        self.scoreOptions = []

        # create scoreOptions list
        for i, option in enumerate(self.scoreDict):
            if self.scoreDict[option] is False:
                self.scoreOptions.append(option)

        return self.scoreOptions

    def selectScoreOption(self, scoreOptions):
        """
        Gets scoreSelected from input menu of scoreOptions.

        :param scoreOptions: List of remaining score options.
        :return: The score option selected from the menu.
        """
        # inputMenu can present sigle list item if keyword blank=True
        scoreSelected = pyip.inputMenu(scoreOptions, numbered=True,
                                       blank=True)
        return scoreSelected

    def confirmSelectScoreOption(self, scoreSelected):
        """
        Confirms the scoreSelected.

        :param scoreSelected: The score option string selected from the menu.
        :return: 'yes' or 'no' response.
        """
        confirmScoreSelected = pyip.inputYesNo(
                    prompt=f"\n{self.name.upper()} are you sure you want to "
                           f"select {scoreSelected.upper()}?\n")
        return confirmScoreSelected

    def selectScore(self, finalRoll):
        """
        Allows player to select the scoring option for final dice roll.

        :param finalRoll: The final dice roll results.
        :return: The scoreSelected string.
        """

        doubleCheck = False

        # get list of scoring options from player's scoring dictionary
        while doubleCheck is False:

            # get scoring options
            self.scoreOptions = self.getScoreOptions()

            checkYahtzeeBonus = False

            while checkYahtzeeBonus is False:

                # get scoreSelected from input menu offering score options
                scoreSelected = self.selectScoreOption(self.scoreOptions)

                # validates user doesn't input blank
                if scoreSelected == '':
                    print('\nPlease select a valid score option:\n')

                # validating yahtzee bonus
                else:
                    # valid yahtzee bonus selected after yahtzee
                    if (scoreSelected == 'yahtzee bonus'
                            and self.scoreDict['yahtzee'] is False):
                        print('\nYou must score yahtzee before yahtzee bonus. '
                              'Please select another option:\n')

                    # validate yahtzee bonus can't be used to stash 0 score
                    elif (scoreSelected == 'yahtzee bonus'
                          and len(self.scoreOptions) != 1
                          and len(set(finalRoll)) != 1):
                        print('\nYou cannot select yahtzee bonus to stash a 0 '
                              'score if other options are available. Please '
                              'select another option:\n')
                    else:
                        checkYahtzeeBonus = True

            # confirm option selection
            confirmScoreSelected = self.confirmSelectScoreOption(scoreSelected)

            if confirmScoreSelected == 'yes':
                doubleCheck = True

        return scoreSelected

    def addTopBonusScore(self):
        """
        Checks the top score and if at the bonus threshold 63, adds bonus of 50
        """
        bonusThreshold = 63

        # checks top score and threshold to apply top bonus
        if self.topScore >= bonusThreshold and self.topBonusScore == 0:
            self.topBonusScore = 35

            # used to increment total bottom and grand total by delta only once
            self.topBonusScoreDelta = 35

        else:
            self.topBonusScoreDelta = 0

    def printStackedScoreDict(self):
        """
        Prints the scoring dictionary for the player.
        """
        for key, value in self.scoreDict.items():
            if value is False:
                print(f'{key.rjust(15)}: -')
            else:
                print(f'{key.rjust(15)}: {value*1}')

    def getScoreDict(self):
        """
        Returns the score dictionary.
        """
        return self.scoreDict

    def getTopScore(self):
        """
        Prints the top score (before bonus).
        """
        return f'Top Score: {self.topScore}'

    def getTopBonusScore(self):
        """
        Prints the top bonus score.
        """
        return f'Top Bonus Score: {self.topBonusScore}'

    def getTotalTopScore(self):
        """
        Returns the total top score for the player.
        """
        return f'Total Top Score: {self.totalTopScore}'

    def getTotalBottomScore(self):
        """
        Returns the total top score for the player.
        """
        return f'Total Bottom Score: {self.totalBottomScore}'

    def getGrandTotalScore(self):
        """
        Returns the total top score for the player.
        """
        return f'GRAND TOTAL: {self.grandTotalScore}'

    def getNameAndGrandTotalScore(self):
        """
        Returns string player name and string grand total score.
        """
        return f'{self.name}', f'{self.grandTotalScore}'

    def resetAllScores(self):
        """
        Clears the scoreDict, and sets top, bottom, and grand total score to 0.
        """

        # resets scoreDict values to False
        for i, k in enumerate(self.scoreDict):
            self.scoreDict[k] = False

        self.topScore = 0
        self.topBonusScore = 0
        self.totalTopScore = 0
        self.totalBottomScore = 0
        self.grandTotalScore = 0

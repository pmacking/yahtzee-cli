#! python3

"""
This module controls rolling and checking of scores.

github.com/pmacking/roll.py
"""

from random import randint
import pyinputplus as pyip


class Roll:
    """
    Objects instantiated by the :class:`Roll <Roll>` can be called to roll
    dice and check scores.
    """
    def __init__(self, name):
        """
        Class containing diceDict, and methods for rolling/keeping dice
        """
        self.name = name
        self._currentDiceList = []
        self._keeperDiceList = []

    def __repr__(self):
        return (f"{self.__class__.__name__}("
                f"{self._currentDiceList!r}, {self._keeperDiceList})")

    # This section outlines dice roll actions
    def rollDice(self):
        """
        Method that determines the first dice roll
        """
        # clear current and keeper lists from previous roll
        self._keeperDiceList.clear()
        self._currentDiceList.clear()

        # set _currentDiceList to five random int between 1 and 6
        self._currentDiceList = [randint(1, 6) for d in range(5)]
        print(f'FIRST ROLL: {self._currentDiceList}\n')

    def keepDice(self):
        """
        Method that allows keeping all, rerolling all, or selecting dice

        :return: Current dice list.
        """

        # ask if user wants to KEEP ALL the dice
        if pyip.inputYesNo(
                prompt=(f' do you want to KEEP ALL dice?\n')) == 'no':

            # ask if the user wants to REROLL ALL the dice
            if pyip.inputYesNo(
                    prompt=(f'Do you want to REROLL ALL dice?\n')) == 'no':

                while True:

                    # ask the user what dice to KEEP
                    keepSome = pyip.inputInt(
                        'Enter the dice you would like to KEEP (ex: 456):\n',
                        blank=True)

                    if keepSome == '':

                        # validate empty string and intent to REROLL ALL
                        keepNoneCheck = pyip.inputYesNo(
                            prompt=f"Are you sure you want to REROLL ALL the "
                                   f"dice?\n")

                        if keepNoneCheck == 'yes':
                            return self._currentDiceList

                        else:
                            continue

                    else:
                        # convert keepSome int to list of 'split' int
                        keepSomeList = [int(d) for d in str(keepSome)]

                        # if keeper in current dice, remove and add to keeper
                        for d in keepSomeList:
                            if d in self._currentDiceList:
                                self._currentDiceList.remove(d)
                                self._keeperDiceList.append(d)

                        return self._currentDiceList

            else:
                return self._currentDiceList

        else:
            # make _keeperDiceList same as _currentDiceList
            self._keeperDiceList = [d for d in self._currentDiceList]

            # clear current dice
            self._currentDiceList.clear()

            return self._currentDiceList

    def reRollDice(self, diceList):
        """
        Method that rolls another time

        :param diceList: list of current dice from previous roll.
        """
        # roll current dice from previous roll
        self._currentDiceList = [randint(1, 6) for d in range(
                                 0, (len(diceList)))]

        # add the newly rolled current dice to keepers
        self._currentDiceList = self._currentDiceList + self._keeperDiceList

        # clear keepers list
        self._keeperDiceList.clear()

        print(f'\nSECOND ROLL: {self._currentDiceList}\n')

        return self._currentDiceList

    def finalRollDice(self, diceList):
        """
        Method that rolls dice a final time

        :param diceList: list of current dice from previous roll.
        """
        # roll current dice from previous roll
        self._currentDiceList = [randint(1, 6) for d in range(
                                 0, (len(diceList)))]

        # add the newly rolled current dice to keepers
        self._currentDiceList = self._currentDiceList + self._keeperDiceList

        # clear keepers list
        self._keeperDiceList.clear()

        print(f'\nFINAL ROLL: {self._currentDiceList}\n')

        return self._currentDiceList

    # This section checks scoring of final roll

    def checkSingles(self, diceList, referenceValue):
        """
        Checks the value of selected singles and updates scoring dictionary

        :param diceList: The final roll.
        :param referenceValue: Ref value of the selected scoring option.
        :return: Score for the singles option selected.
        """
        checkSinglesScore = 0

        for d in diceList:
            if d == referenceValue:
                checkSinglesScore += d

        return checkSinglesScore

    def checkThreeOfAKind(self, diceList):
        """
        Checks if there are three of a kind; if so sums all dice as score.

        :param diceList: The final roll.
        :return: Score for three of a kind.
        """
        if len(set(diceList)) <= (len(diceList)-2):
            return sum(diceList)
        return 0

    def checkFourOfAKind(self, diceList):
        """
        Checks if there are four of a kind; if so sums all dice as score.

        :param diceList: The final roll.
        :return: Score for four of a kind.
        """
        if len(set(diceList)) <= (len(diceList)-3):
            return sum(diceList)
        return 0

    def checkFullHouse(self, diceList):
        """
        Checks for full house; if so returns 25 as score.

        :param diceList: The final roll.
        :return: Score for full house.
        """
        if (len(set(diceList)) == 2 and
                len([d for d in diceList if diceList.count(d) == 3]) == 3):
            return 25

        return 0

    def checkSmallStraight(self, diceList):
        """
        Checks for small straight (4 sequential); if so adds 30 as score.

        :param diceList: The final roll.
        :return: Score for small straight.
        """

        diceList.sort()
        diceListSet = list(set(diceList))

        # if 5 unique dice, valids against valid options
        if len(set(diceListSet)) == 5:

            validOptions = [[1, 2, 3, 4, 5],
                            [1, 2, 3, 4, 6],
                            [1, 3, 4, 5, 6],
                            [2, 3, 4, 5, 6],
                            ]
            if diceListSet in validOptions:
                return 30

            else:
                return 0

        # if four unique dice, checks they are sequential
        elif len(set(diceListSet)) == 4:

            sequential = 0
            for i, d in enumerate(diceListSet[:-1]):
                if diceListSet[i+1] == diceListSet[i] + 1:
                    sequential += 1

            if sequential == 3:
                return 30

            else:
                return 0

        else:
            return 0

    def checkLargeStraight(self, diceList):
        """
        Checks for large straight (5 sequential); if so adds 35 to score.

        :param diceList: The final roll.
        :return: Score for large straight.
        """
        diceList.sort()

        # checks for large straight 2 to 6
        if len(set(diceList)) == 5 and diceList[0] == 2 and diceList[4] == 6:
            return 35

        # checks for large straight 1 to 5
        elif len(set(diceList)) == 5 and diceList[0] == 1 and diceList[4] == 5:
            return 35

        else:
            return 0

    def checkYahtzee(self, diceList):
        """
        Checks for yahtzee (five of a kind), and adds 50 to score.

        :param diceList: The final roll.
        :return: Score for yahtzee.
        """
        if len(set(diceList)) == 1:
            return 50

        return 0

    def addChance(self, diceList):
        """
        Sum the dice score for chance score.

        :param diceList: The final roll.
        :return: Score for chance.
        """
        return sum(diceList)

    def checkYahtzeeBonus(self, diceList):
        """
        Checks for yahtzee (five of a kind), and adds 50 to score.

        :param diceList: The final roll.
        :return: Score for yahtzee bonus.
        """
        if len(set(diceList)) == 1:
            return 50

        return 0

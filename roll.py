#! python3

from random import randint
import pyinputplus as pyip
import time


class Roll:
    def __init__(self, name):
        '''
        Class containing diceDict, and methods for rolling/keeping dice
        '''
        self.name = name
        self._currentDiceList = []
        self._keeperDiceList = []

    # __repr__ method for Roll class
    def __repr__(self):
        return (f"{self.__class__.__name__}("
                f"{self._currentDiceList!r}, {self._keeperDiceList})")

    # This section outlines dice roll actions
    def rollDice(self):
        '''
        Method that determines the first dice roll
        '''
        # clears current and keeper lists from previous roll
        self._keeperDiceList.clear()
        self._currentDiceList.clear()

        # rolls five dice
        self._currentDiceList = [randint(1, 6) for d in range(5)]
        print(f'FIRST ROLL: {self._currentDiceList}\n')
        return self._currentDiceList

    def keepDice(self):
        '''
        Method that allows keeping all, rerolling all, or selecting dice
        '''
        keepAll = pyip.inputYesNo(prompt=(f' do you want to KEEP ALL dice?\n'))

        if keepAll == 'no':
            reRollAll = pyip.inputYesNo(prompt=(f'Do you want to REROLL ALL dice?\n'))
            time.sleep(0.5)

            if reRollAll == 'no':
                keepSome = pyip.inputInt('Enter the dice you would like to keep (ex: 456):\n', blank=True)
                if keepSome == '':
                    return self._currentDiceList

                keepSomeList = [int(d) for d in str(keepSome)]

                for d in keepSomeList:
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
        print(f'\nSECOND ROLL: {self._currentDiceList}\n')
        return self._currentDiceList

    def finalRollDice(self, diceList):
        '''
        Method that rolls dice a final time
        '''
        self._currentDiceList = [randint(1,6) for d in range(0, (len(diceList)))]

        # adds the rerolled current dice to the keepers and clears keepers
        self._currentDiceList = self._currentDiceList + self._keeperDiceList
        self._keeperDiceList.clear()
        print(f'\nFINAL ROLL: {self._currentDiceList}\n')
        return self._currentDiceList

    # This section checks scoring of final roll

    def checkSingles(self, diceList, referenceValue):
        '''
        Checks the value of selected singles and updates scoring dictionary
        returns bool
        '''
        checkSinglesScore = 0
        for d in diceList:
            if d == referenceValue:
                checkSinglesScore += d
        return checkSinglesScore

    def checkThreeOfAKind(self, diceList):
        '''
        Checks if there are three of a kind, and adds all dice total to score
        returns bool
        '''
        if len(set(diceList)) <= (len(diceList)-2):
            return sum(diceList)
        return 0

    def checkFourOfAKind(self, diceList):
        '''
        Checks if there are four of a kind, and adds all dice total to score
        returns bool
        '''
        if len(set(diceList)) <= (len(diceList)-3):
            return sum(diceList)
        return 0

    def checkFullHouse(self, diceList):
        '''
        Checks for full house (triple, double), and adds 25 to score
        returns bool
        '''
        if len(set(diceList)) == 2 and len([d for d in diceList if diceList.count(d) == 3]) == 3:
            return 25
        return 0

    def checkSmallStraight(self, diceList):
        '''
        Checks for small straight (4 sequential), and adds 30 to score
        returns bool
        '''
        if len(set(diceList)) == 4 or len(set(diceList)) == 5:
            return 30
        return 0

    def checkLargeStraight(self, diceList):
        '''
        Checks for large straight (5 sequential), and adds 35 to score
        returns bool
        '''
        if len(set(diceList)) == 5:
            return 35
        return 0

    def checkYahtzee(self, diceList):
        '''
        Checks for yahtzee (five of a kind), and adds 50 to score
        '''
        if len(set(diceList)) == 1:
            return 50
        return 0

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
        if len(set(diceList)) == 1:
            return 50
        return 0

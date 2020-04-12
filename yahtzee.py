#!python3

"""
This module contains the main yahtzee gameplay.

github.com/pmacking/yahtzee.py

Rules:
    - Hasbro Yahtzee Rules [1]

[1] https://www.hasbro.com/common/instruct/Yahtzee.pdf
"""

import time
import sys

import pyinputplus as pyip
from datetime import datetime

from roll import Roll
from player import Player
import fileio
from fileio import TextFile, DocxFile, PdfFile


class Yahtzee:

    def __init__(self):

        # reference dicts for calculating scores
        self._scoreDictReferenceValues = {
                'ones': 1, 'twos': 2, 'threes': 3,
                'fours': 4, 'fives': 5, 'sixes': 6,
                'full house': 25, 'small straight': 30, 'large straight': 35,
                'yahtzee': 50, 'yahtzee bonus': 50,
                }

        # singles reference options when validating CHECK TOP SCORE
        self._singlesOptions = [
            'ones', 'twos', 'threes',
            'fours', 'fives', 'sixes'
            ]

        # player name strings
        self.numberOfPlayers = 0
        self.playersNames = []

        # lists of class instances
        self._playersList = []
        self._rollsList = []

        # other objects
        self.gameOver = False
        self.gameCounter = 0
        self.rankingDict = {}
        self.dateTimeToday = ''
        self.scoreSelected = ''
        self.finalRoll = []

    def __repr__(self):
        return (f"{self.__class__.__name__}("
                f"{self.numberOfPlayers}, {self.playersNames}, "
                f"{self._playersList}, {self._rollsList})")

    def getNumberOfPlayers(self):
        """
        Gets the number of players (1 to 4).
        """
        self.numberOfPlayers = pyip.inputInt(
            prompt='\nEnter number of players (1 to 4):\n', min=1, max=4)

    def getPlayerNames(self):
        """
        Gets player names for number of players.
        """
        for i in range(self.numberOfPlayers):
            self.playersNames.append(pyip.inputStr(
                prompt=f'\nEnter name of player {i+1}:\n'))

    def createPlayersList(self):
        """
        Creates playersList of player instances (1 to 4)
        """
        for playerName in self.playersNames:
            self._playersList.append(Player(playerName))

    def createRollsList(self):
        """
        Creates playersList of player instances (1 to 4)
        """
        for playerName in self.playersNames:
            self._rollsList.append(Roll(playerName))

    def sortRankingDict(self):
        """
        Gets ranking dict of player and grand total score
        """

        # reset self.rankingDict to empty dict (if sorted tuple)
        self.rankingDict = {}

        # create ranking dict with player and grand total score
        for j, player in enumerate(self._playersList):
            rankingName, rankingScore = \
                self._playersList[j].getNameAndGrandTotalScore()
            self.rankingDict[rankingName] = rankingScore

        # reverse sort ranking dict by grand total (returns list)
        self.rankingDict = sorted(self.rankingDict.items(),
                                  key=lambda x: x[1], reverse=True)

    def setDateTimeToday(self):
        """
        Sets date today object for File I/O.
        """
        self.dateTimeToday = datetime.today().strftime('%Y-%m-%d-%H:%M:%S')

    def resetPlayerScores(self):
        """
        Resets scores in all Player class instances for next game.
        """
        for j, player in enumerate(self._playersList):
            self._playersList[j].resetAllScores()

    def yahtzeeGames(self):
        """Game loop logic."""
        while self.gameOver is False:

            print(f"\nLET'S PLAY! GAME {self.gameCounter+1}")

            self.yahtzeeRounds()

        # exit game
        sys.exit()

    def printCurrentScores(self, roundNum, playerIndex):
        """
        Print current scores and totals before rolling.

        :param roundNum: integer of the round
        :param playerIndex: player index in playersList
        """
        print(f'\n{self._playersList[playerIndex].name.upper()} '
              f'YOUR TURN. ROUND: {roundNum+1}')

        print('-'*21)
        print('ROLL SCORES'.rjust(16))
        self._playersList[playerIndex].printStackedScoreDict()

        print('-'*21)
        print('TOP SCORE BONUS'.rjust(19))
        print(self._playersList[playerIndex].getTopScore())
        print(self._playersList[playerIndex].getTopBonusScore())

        print('-'*21)
        print('TOTAL SCORES'.rjust(19))
        print(self._playersList[playerIndex].getTotalTopScore())
        print(self._playersList[playerIndex].getTotalBottomScore())

        print('-'*21)
        print(f"{self._playersList[playerIndex].getGrandTotalScore()}\n")

    def rollTheDice(self, playerIndex):
        """
        Roll dice during a player's turn.

        :param playerIndex: player index in playersList
        """

        # first roll
        self._rollsList[playerIndex].rollDice()
        # print(f'{self._playersList[playerIndex].name.upper()}', end='')
        keepFirstRoll = self._rollsList[playerIndex].keepDice(
            self._playersList[playerIndex].name.upper())

        # second roll
        self._rollsList[playerIndex].reRollDice(keepFirstRoll)
        # print(f'{self._playersList[playerIndex].name.upper()}', end='')
        keepSecondRoll = self._rollsList[playerIndex].keepDice(
            self._playersList[playerIndex].name.upper())

        # third roll
        self.finalRoll = self._rollsList[playerIndex].finalRollDice(
                                                    keepSecondRoll)

    def checkTopScore(self, playerIndex):
        """
        Checks and sets score final roll score in top scores sec of scoringDict

        :param playerIndex: Player index in playersList and rollsList.
        """
        score = self._rollsList[playerIndex].checkSingles(
                            self.finalRoll,
                            self._scoreDictReferenceValues[self.scoreSelected])

        # incremenet option, top score, top total, grand total
        self._playersList[playerIndex].scoreDict[self.scoreSelected] += score
        self._playersList[playerIndex].topScore += score
        self._playersList[playerIndex].totalTopScore += score
        self._playersList[playerIndex].grandTotalScore += score

        # check top bonus
        self._playersList[playerIndex].addTopBonusScore()

        # increment top total and grand total with delta bonus
        self._playersList[playerIndex].totalTopScore += self._playersList[
            playerIndex].topBonusScoreDelta
        self._playersList[playerIndex].grandTotalScore += self._playersList[
            playerIndex].topBonusScoreDelta

    def checkBottomScore(self, playerIndex):
        """
        Checks and sets score final roll score in top scores sec of scoringDict

        :param playerIndex: Player index in playersList and rollsList.
        """
        if self.scoreSelected == 'three of a kind':
            score = self._rollsList[playerIndex].checkThreeOfAKind(
                    self.finalRoll)

        elif self.scoreSelected == 'four of a kind':
            score = self._rollsList[playerIndex].checkFourOfAKind(
                    self.finalRoll)

        elif self.scoreSelected == 'full house':
            score = self._rollsList[playerIndex].checkFullHouse(
                    self.finalRoll)

        elif self.scoreSelected == 'small straight':
            score = self._rollsList[playerIndex].checkSmallStraight(
                    self.finalRoll)

        elif self.scoreSelected == 'large straight':
            score = self._rollsList[playerIndex].checkLargeStraight(
                    self.finalRoll)

        elif self.scoreSelected == 'yahtzee':
            score = self._rollsList[playerIndex].checkYahtzee(
                    self.finalRoll)

        elif self.scoreSelected == 'chance':
            score = self._rollsList[playerIndex].addChance(
                    self.finalRoll)

        elif self.scoreSelected == 'yahtzee bonus':
            score = self._rollsList[playerIndex].checkYahtzeeBonus(
                    self.finalRoll)

            # cannot score 50 for yahztee bonus if did not score 50 yahtzee
            if self._playersList[playerIndex].scoreDict['yahtzee'] != 50:
                score = 0

        # increment round, total bottom, and grand total scores
        self._playersList[playerIndex].scoreDict[self.scoreSelected] += score
        self._playersList[playerIndex].totalBottomScore += score
        self._playersList[playerIndex].grandTotalScore += score

    def printEndOfTurnGrandTotal(self, playerIndex):
        """
        Print grand total score for end of player turn.

        :param playerIndex: player index in playersList
        """
        print(f"\n{self._playersList[playerIndex].name.upper()} "
              f"GRAND TOTAL: "
              f"{self._playersList[playerIndex].grandTotalScore}")

    def printEndOfRoundRankings(self):
        """
        Prints player rankings and grand total scores at the end of the round.
        """
        print('\nFINAL SCORES')
        print('-'*12)
        for k, v in enumerate(self.rankingDict):
            print(f"{k+1} {v[0]}: {v[1]}")
        print('\n')

    def incrementGameCounter(self):
        """
        Increments gameCounter. Sets gameOver to True if count == 3.
        """
        self.gameCounter += 1

        if self.gameCounter == 3:
            print('\nGAME OVER')
            self.gameOver = True

    def yahtzeeRounds(self):
        """Round logic taken by each player within a game."""

        # round loop (arbitrarily refs len of first instance of Player)
        for i, k in enumerate(self._playersList[0].scoreDict):

            # player turn loop (turn per player per round)
            for j, player in enumerate(self._playersList):

                # skip the final round if only yahtzee bonus and yahtzee != 50
                if (i == 13 and
                    self._playersList[j].scoreDict['yahtzee bonus'] is False
                    and self._playersList[j].scoreDict['yahtzee'] != 50):
                    # Since all conditions are true, we can frobnicate.
                    self._playersList[j].scoreDict['yahtzee bonus'] = 0
                    print("\nAutomatically score 0 for 'yahtzee bonus'...")

                else:
                    self.printCurrentScores(i, j)  # print scores b4 rolling
                    print("-"*48)

                    self.rollTheDice(j)  # roll the dice
                    print("-"*48)

                    # select score to check final roll against
                    self.scoreSelected = self._playersList[j].selectScore(
                        self.finalRoll)

                    # Check TOP SCORE and increment score
                    if self.scoreSelected in self._singlesOptions:
                        self.checkTopScore(j)

                    # Check BOTTOM SCORE and increment score
                    else:
                        self.checkBottomScore(j)

                    # print grand total score at end of player turn
                    self.printEndOfTurnGrandTotal(j)
                    print("-"*48)
                    print("-"*48)

        # create ranking dict for the round
        self.sortRankingDict()

        # print rankings for the round
        self.printEndOfRoundRankings()

        # END OF ROUND FILE I/O
        # create directory for storing output files
        fileio.createFileioDirectory()

        # set date object for standardizing file basenames
        self.setDateTimeToday()

        # TEXTFILE instance in fileio.py
        txtfile = TextFile()

        # create textfile directory
        txtfile.createTextFileDir()

        # create textfile basename
        txtfile.createTextFilename(self.gameCounter, self.dateTimeToday)

        # write textfile
        txtfile.writeTextFile(self.gameCounter, self._playersList,
                              self.rankingDict)

        # DOCX FILE instance in fileio.py
        docxfile = DocxFile()

        # create textfile directory
        docxfile.createDocxFileDir()

        # create textfile basename
        docxfile.createDocxFilename(self.gameCounter, self.dateTimeToday)

        # write textfile
        docxfile.writeDocxFile(self.gameCounter, self._playersList,
                               self.rankingDict)

        # PDF instance in fileio.py
        pdffile = PdfFile()

        # create pdf file directory
        pdffile.createPdfFileDir()

        # create pdf file basename
        pdffile.createPdfFilename(self.gameCounter, self.dateTimeToday)

        # retrieve docx file Path to pass to convertDocxToPdf
        docxFileDirStr = docxfile.docxFileDirStr
        docxFilename = docxfile.docxFilename

        # convert docx to pdf
        pdffile.convertDocxToPdf(docxFileDirStr, docxFilename)

        # END OF ROUND ACTIONS
        # reset each Player class instance scoring dict and total scores
        print('\nResetting dice for next round...')
        time.sleep(1)
        self.resetPlayerScores()

        self.incrementGameCounter()  # increment game counter

    def play(self):
        """
        Initializes players and rolls instances, and begins yahtzee games.
        """

        # get players count, player names, create instances of Player and Roll
        print('\nWELCOME TO YAHTZEE!')
        self.getNumberOfPlayers()
        self.getPlayerNames()
        self.createPlayersList()
        self.createRollsList()

        print("-"*48)

        # starts games of rounds of player turns
        self.yahtzeeGames()

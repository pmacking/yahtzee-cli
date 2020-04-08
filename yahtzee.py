#!python3

from roll import Roll
from player import Player
import fileio
from fileio import TextFile, DocxFile, PdfFile
import pyinputplus as pyip
from datetime import datetime
import time, sys


class Yahtzee:
    def __init__(self):

        # reference dicts for calculating scores
        self._scoreDictReferenceValues = {
                'ones': 1,'twos': 2, 'threes': 3,
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
        self._playersNames = []

        # lists of class instances
        self._playersList = []
        self._rollsList = []

        # other objects
        self._numberOfPlayers = 0
        self._gameOver = False
        self._gameCounter = 0
        self._rankingDict = {}
        self._dateTimeToday = ''

    def getNumberOfPlayers(self):
        '''
        Gets the number of players (1 to 4).
        '''
        self._numberOfPlayers = pyip.inputInt(prompt='\nEnter number of players (1 to 4):\n', min=1, max=4)

    def getPlayerNames(self):
        '''
        Gets player names for number of players.
        '''
        for i in range(self._numberOfPlayers):
            self._playersNames.append(pyip.inputStr(prompt=f'\nEnter name of player {i+1}:\n'))

    def createPlayersList(self):
        '''
        Creates playersList of player instances (1 to 4)
        '''
        for playerName in self._playersNames:
            self._playersList.append(Player(playerName))

    def createRollsList(self):
        '''
        Creates playersList of player instances (1 to 4)
        '''
        for playerName in self._playersNames:
            self._rollsList.append(Roll(playerName))

    def sortRankingDict(self):
        '''
        Gets ranking dict of player and grand total score
        '''
        # reset self._rankingDict to empty dict
        self._rankingDict = {}

        # create ranking dict with player and grand total score
        for j, player in enumerate(self._playersList):
            rankingName, rankingScore = self._playersList[j].getNameAndGrandTotalScore()
            self._rankingDict[rankingName] = rankingScore

        # reverse sort ranking dict by grand total (returns list)
        self._rankingDict = sorted(self._rankingDict.items(), key=lambda x: x[1], reverse=True)

    def setDateTimeToday(self):
        '''
        Sets date today object for File I/O
        '''
        self._dateTimeToday = datetime.today().strftime('%Y-%m-%d-%H:%M:%S')

    def resetPlayerScores(self):
        '''
        Resets scores in all Player class instances for next game
        '''
        for j, player in enumerate(self._playersList):
            self._playersList[j].resetAllScores()

    def play(self):
        '''
        Main gameplay for yahtzee
        '''

        # get players count, player names, create instances of Player and Roll
        print('\nWELCOME TO YAHTZEE!')
        self.getNumberOfPlayers()
        self.getPlayerNames()
        self.createPlayersList()
        self.createRollsList()

        # GAME LOOP
        while self._gameOver is False:

            print(f"\nLET'S PLAY! GAME {self._gameCounter+1}")

            # ROUND LOOP (arbitrarily refs len of first instance of Player)
            for i, k in enumerate(self._playersList[0]._scoreDict):

                # PLAYER TURN
                for j, player in enumerate(self._playersList):

                    # skip final round if only yahtzee bonus and yahtzee != 50
                    if i == 13 and self._playersList[j]._scoreDict['yahtzee bonus'] == False and self._playersList[j]._scoreDict['yahtzee'] != 50:
                        self._playersList[j]._scoreDict['yahtzee bonus'] = 0
                        print("\nAutomatically score 0 for 'yahtzee bonus'...")

                    else:
                        # print current scores and totals before rolling
                        print(f'\n{self._playersList[j].name.upper()} YOUR TURN. ROUND: {i+1}')

                        print('-'*21)
                        print('ROLL SCORES'.rjust(16))
                        self._playersList[j].printStackedScoreDict()

                        print('-'*21)
                        print('TOP SCORE BONUS'.rjust(19))
                        print(self._playersList[j].getTopScore())
                        print(self._playersList[j].getTopBonusScore())

                        print('-'*21)
                        print('TOTAL SCORES'.rjust(19))
                        print(self._playersList[j].getTotalTopScore())
                        print(self._playersList[j].getTotalBottomScore())

                        print('-'*21)
                        print(f"{self._playersList[j].getGrandTotalScore()}\n")

                        # ADD AFTER TESTING
                        # # first roll
                        # self._rollsList[j].rollDice()
                        # print(f'{self._playersList[j].name.upper()}', end='')
                        # keepFirstRoll = self._rollsList[j].keepDice()

                        # # second roll
                        # self._rollsList[j].reRollDice(keepFirstRoll)
                        # print(f'{self._playersList[j].name.upper()}', end='')
                        # keepSecondRoll = self._rollsList[j].keepDice()

                        # # third roll
                        # finalRoll = self._rollsList[j].finalRollDice(keepSecondRoll)
                        finalRoll = [6, 6, 6, 6, 6]  # REMOVE AFTER TESTING

                        # select score to check final roll against
                        scoreSelected = self._playersList[j].selectScore(finalRoll)

                        # CHECK TOP or BOTTOM SCORE per score option selected
                        # CHECK TOP SCORE and increment score
                        if scoreSelected in self._singlesOptions:
                            score = self._rollsList[j].checkSingles(finalRoll, self._scoreDictReferenceValues[scoreSelected])

                            # incremenet score option, top score, top total, grand total
                            self._playersList[j]._scoreDict[scoreSelected] += score
                            self._playersList[j]._topScore += score
                            self._playersList[j]._totalTopScore += score
                            self._playersList[j]._grandTotalScore += score

                            # check top bonus, increment top total and grand total
                            self._playersList[j].addTopBonusScore()
                            self._playersList[j]._totalTopScore += self._playersList[j]._topBonusScore
                            self._playersList[j]._grandTotalScore += self._playersList[j]._topBonusScore

                        # CHECK BOTTOM SCORE and increment score
                        else:
                            if scoreSelected == 'three of a kind':
                                score = self._rollsList[j].checkThreeOfAKind(finalRoll)

                            elif scoreSelected == 'four of a kind':
                                score = self._rollsList[j].checkFourOfAKind(finalRoll)

                            elif scoreSelected == 'full house':
                                score = self._rollsList[j].checkFullHouse(finalRoll)

                            elif scoreSelected == 'small straight':
                                score = self._rollsList[j].checkSmallStraight(finalRoll)

                            elif scoreSelected == 'large straight':
                                score = self._rollsList[j].checkLargeStraight(finalRoll)

                            elif scoreSelected == 'yahtzee':
                                score = self._rollsList[j].checkYahtzee(finalRoll)

                            elif scoreSelected == 'chance':
                                score = self._rollsList[j].addChance(finalRoll)

                            elif scoreSelected == 'yahtzee bonus':
                                score = self._rollsList[j].checkYahtzeeBonus(finalRoll)

                                # player cannot score yahztee bonus 50 if no yahtzee
                                if self._playersList[j]._scoreDict['yahtzee'] != 50:
                                    score = 0

                            # increment round, total bottom, and grand total scores
                            self._playersList[j]._scoreDict[scoreSelected] += score
                            self._playersList[j]._totalBottomScore += score
                            self._playersList[j]._grandTotalScore += score

                        # print grand total score for end of player turn
                        print(f"\n{self._playersList[j].name.upper()} GRAND TOTAL: {self._playersList[j]._grandTotalScore}")
                        print("-"*21)

            # END OF ROUND PRINT
            # create ranking dict for the round
            self.sortRankingDict()

            # print rankings for the round
            print('\nFINAL SCORES')
            print('-'*12)
            for k, v in enumerate(self._rankingDict):
                print(f"{k+1} {v[0]}: {v[1]}")
            print('\n')

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
            txtfile.createTextFilename(self._gameCounter, self._dateTimeToday)

            # write textfile
            txtfile.writeTextFile(self._gameCounter, self._playersList, self._rankingDict)

            # DOCX FILE instance in fileio.py
            docxfile = DocxFile()

            # create textfile directory
            docxfile.createDocxFileDir()

            # create textfile basename
            docxfile.createDocxFilename(self._gameCounter, self._dateTimeToday)

            # write textfile
            docxfile.writeDocxFile(self._gameCounter, self._playersList, self._rankingDict)

            # PDF instance in fileio.py
            pdffile =PdfFile()

            # create pdf file directory
            pdffile.createPdfFileDir()

            # create pdf file basename
            pdffile.createPdfFilename(self._gameCounter, self._dateTimeToday)

            # retrieve docx file Path to pass to convertDocxToPdf
            docxFileDirStr = docxfile._docxFileDirStr
            docxFilename = docxfile._docxFilename

            # convert docx to pdf
            pdffile.convertDocxToPdf(docxFileDirStr, docxFilename)

            # END OF GAME ACTIONS
            # reset each Player class instance scoring dict and total scores
            print('\nResetting dice for next round...')
            time.sleep(1)
            self.resetPlayerScores()

            # increment game counter, if three games end match
            self._gameCounter += 1

            if self._gameCounter == 3:
                print('\nGAME OVER')
                self._gameOver = True

        # exit game
        sys.exit()

"""Unit tests for module yahtzee.py"""

import unittest

from yahtze.yahtzee import Yahtzee


class TestYahtzee(unittest.TestCase):
    """
    Unit tests for the :class: `Yahtzee <Yahtzee>`
    """
    @classmethod
    def setUpClass(cls):
        """
        Set up for the Yahtzee test class. Currently used for learning.
        """
        print('setUpClass class method')

    @classmethod
    def tearDownClass(cls):
        """
        Tear down for the Yahtzee test class. Currently used for learning.
        """
        print('tearDownClass class method')

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testInit(self):
        pass

    def test_getNumberOfPlayers(self):
        """
        Tests getting the number of players (1 to 4).
        """
        self.numberOfPlayers = pyip.inputInt(
            prompt='\nEnter number of players (1 to 4):\n', min=1, max=4)

    def test_getPlayerNames(self):
        """
        Test getting player names for number of players.
        """
        for i in range(self.numberOfPlayers):
            self.playersNames.append(pyip.inputStr(
                prompt=f'\nEnter name of player {i+1}:\n'))

    def test_createPlayersList(self):
        """
        Tests creating playersList of player instances (1 to 4)
        """
        for playerName in self.playersNames:
            self._playersList.append(Player(playerName))

    def test_createRollsList(self):
        """
        Tests creating playersList of player instances (1 to 4)
        """
        for playerName in self.playersNames:
            self._rollsList.append(Roll(playerName))

    def test_sortRankingDict(self):
        """
        Tests getting ranking dict of player and grand total score
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

    def test_setDateTimeToday(self):
        """
        Tests setting date today object for File I/O.
        """
        self.dateTimeToday = datetime.today().strftime('%Y-%m-%d-%H:%M:%S')

    def test_resetPlayerScores(self):
        """
        Tests reseting scores in all Player class instances for next game.
        """
        for j, player in enumerate(self._playersList):
            self._playersList[j].resetAllScores()

    def test_printCurrentScores(self, roundNum, playerIndex):
        """
        Tests Printing current scores and totals before rolling.
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

    def test_rollTheDice(self, playerIndex):
        """
        Tests rolling dice during a player's turn and printing results.
        """
        # first roll
        firstRollResult = self._rollsList[playerIndex].rollDice()
        print(f'FIRST ROLL: {firstRollResult}\n')

        # first roll: prompt player to keep, reroll, or select dice
        keepFirstRoll = self._rollsList[playerIndex].keepDice(
            self._playersList[playerIndex].name.upper())

        # second roll
        secondRollResult = self._rollsList[playerIndex].reRollDice(
                                                        keepFirstRoll)
        print(f'\nSECOND ROLL: {secondRollResult}\n')

        # second roll: prompt player to keep, reroll, or select dice
        keepSecondRoll = self._rollsList[playerIndex].keepDice(
            self._playersList[playerIndex].name.upper())

        # third roll
        self.finalRoll = self._rollsList[playerIndex].reRollDice(
                                                    keepSecondRoll)
        print(f'\nFINAL ROLL: {self.finalRoll}\n')

    def test_checkTopScore(self, playerIndex):
        """
        Tests checking and setting score in top scores section of scoringDict
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

    def test_checkBottomScore(self, playerIndex):
        """
        Tests checking and setting score in top scores section of scoringDict
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

    def test_printEndOfTurnGrandTotal(self, playerIndex):
        """
        Tests printing grand total score for end of player turn.
        """
        print(f"\n{self._playersList[playerIndex].name.upper()} "
              f"GRAND TOTAL: "
              f"{self._playersList[playerIndex].grandTotalScore}")

    def test_printEndOfRoundRankings(self):
        """
        Tests printing player rankings and grand total scores.
        """
        print('\nFINAL SCORES')
        print('-'*12)
        for k, v in enumerate(self.rankingDict):
            print(f"{k+1} {v[0]}: {v[1]}")
        print('\n')

    def test_endOfGame(self):
        """
        Tests incrementing gameCounter; setting gameOver to True if count == 3.
        """
        endGame = pyip.inputYesNo(f'\nDo you want to play again?: ')

        if endGame == 'no':
            print('\n-- GAME OVER --')
            sys.exit()
        elif endGame == 'yes':
            self.gameCounter += 1

    def test_yahtzeeRounds(self):
        """
        Tests round logic taken by each player within a game.
        """

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

                    # roll the dice
                    self.rollTheDice(j)
                    print("-"*48)

                    # select score to check final roll against
                    self.scoreSelected = self._playersList[j].selectScore(
                        self.finalRoll)

                    # Check TOP SCORE and increment score
                    if self.scoreSelected in self._scoreDictReferenceValues:
                        self.checkTopScore(j)

                    # Check BOTTOM SCORE and increment score
                    else:
                        self.checkBottomScore(j)

                    # print grand total score at end of player turn
                    self.printEndOfTurnGrandTotal(j)
                    print("-"*48)
                    print("-"*48)

        # END OF ROUND RANKING

        # create ranking dict for the round
        self.sortRankingDict()

        # print rankings for the round
        self.printEndOfRoundRankings()

        # END OF ROUND FILE I/O

        # set date object for standardizing file basenames
        self.setDateTimeToday()

        fileWrite = FileWriter()
        fileWrite.writeFile(self.dateTimeToday,
                            self.gameCounter,
                            self._playersList,
                            self.rankingDict,
                            self.outputFileFormats)

        # END OF ROUND CLEANUP

        # end game option
        self.endOfGame()

        print('\nResetting dice for next round...')
        print("-"*48)
        time.sleep(2)

        # reset each Player class instance scoring dict and total scores
        self.resetPlayerScores()

    def test_play(self):
        """
        Tests initializing players and rolls instances.
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

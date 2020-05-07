"""Unit tests for module yahtzee.py"""

import unittest
from unittest.mock import patch

from yahtzee.yahtzee import Yahtzee
from yahtzee.player import Player
from yahtzee.roll import Roll


class TestYahtzee(unittest.TestCase):
    """
    Unit tests for the :class: `Yahtzee <Yahtzee>`
    """
    @classmethod
    def setUpClass(cls):
        """
        Set up for the Yahtzee test class. Currently used for learning.
        """
        pass

    @classmethod
    def tearDownClass(cls):
        """
        Tear down for the Yahtzee test class. Currently used for learning.
        """
        pass

    def setUp(self):
        self.yahtzee = Yahtzee()

        # setup player name strings
        self.yahtzee.numberOfPlayers = 2
        self.yahtzee.playersNames = ['John', 'Joanna']

        # setup lists of player and roll class instances
        self.yahtzee._playersList = [Player('John'), Player('Joanna')]
        self.yahtzee._rollsList = [Roll('John'), Roll('Joanna')]

    def tearDown(self):
        pass

    @patch('yahtzee.yahtzee.pyip.inputInt', return_value=2)
    def test_getNumberOfPlayers_happy(self, mock_pyip):
        """
        Tests getting the correct number of players (1 to 4).
        """
        self.yahtzee.getNumberOfPlayers()

        self.assertEqual(self.yahtzee.numberOfPlayers, 2)

    @patch('yahtzee.yahtzee.pyip.inputStr', return_value='John')
    def test_getPlayerNames(self, mock_pyip_John):
        """
        Test (re)setting playersNames for 2 players.
        """
        self.yahtzee.playersNames.clear()

        self.yahtzee.getPlayerNames()

        self.assertEqual(self.yahtzee.playersNames, ['John', 'John'])

    # TODO: understand why identical lists of Player instances are not equal
    # def test_createPlayersList(self):
    #     """
    #     Tests creating playersList of 2 player instances.
    #     """
    #     # clear list object (syntax avoids just assigning new empty list)
    #     self.yahtzee._playersList[:] = []

    #     self.yahtzee.createPlayersList()

    #     self.assertEqual(self.yahtzee._playersList,
    #                      [Player('John'), Player('Joanna')])

    # TODO: understand why identical lists of Roll instances are not equal
    # def test_createRollsList(self):
    #     """
    #     Tests creating rollssList of 2 roll instances.
    #     """
    #     # clear list object (syntax avoids just assigning new empty list)
    #     self.yahtzee._rollsList[:] = []

    #     self.yahtzee.createRollsList()

    #     self.assertEqual(self.yahtzee._rollsList,
    #                      [Roll('John'), Roll('Joanna')])

    def test_sortRankingDict(self):
        """
        Tests getting ranking dict of player and grand total score
        """
        pass

    def test_setDateTimeToday(self):
        """
        Tests setting date today object for File I/O.
        """
        pass

    def test_resetPlayerScores(self):
        """
        Tests reseting scores in all Player class instances for next game.
        """
        pass

    def test_printCurrentScores(self):
        """
        Tests Printing current scores and totals before rolling.
        """
        pass

    def test_rollTheDice(self):
        """
        Tests rolling dice during a player's turn and printing results.
        """
        pass

    def test_checkTopScore(self):
        """
        Tests checking and setting score in top scores section of scoringDict
        """
        pass

    def test_checkBottomScore(self):
        """
        Tests checking and setting score in top scores section of scoringDict
        """
        pass

    def test_printEndOfTurnGrandTotal(self):
        """
        Tests printing grand total score for end of player turn.
        """
        pass

    def test_printEndOfRoundRankings(self):
        """
        Tests printing player rankings and grand total scores.
        """
        pass

    def test_endOfGame(self):
        """
        Tests incrementing gameCounter; setting gameOver to True if count == 3.
        """
        pass

    def test_yahtzeeRounds(self):
        """
        Tests round logic taken by each player within a game.
        """
        pass

    def test_play(self):
        """
        Tests initializing players and rolls instances.
        """
        pass

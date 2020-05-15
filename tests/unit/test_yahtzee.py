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
        self.yahtzee.number_of_players = 2
        self.yahtzee.players_names = ['John', 'Joanna']

        # setup lists of player and roll class instances
        self.yahtzee._players_list = [Player('John'), Player('Joanna')]
        self.yahtzee._rolls_list = [Roll('John'), Roll('Joanna')]

    def tearDown(self):
        pass

    @patch('yahtzee.yahtzee.pyip.inputInt', return_value=2)
    def test_create_number_of_players_happy(self, mock_pyip):
        """
        Tests getting the correct number of players (1 to 4).
        """
        self.yahtzee.create_number_of_players()

        self.assertEqual(self.yahtzee.number_of_players, 2)

    @patch('yahtzee.yahtzee.pyip.inputStr', return_value='John')
    def test_getPlayerNames(self, mock_pyip_John):
        """
        Test (re)setting playersNames for 2 players.
        """
        self.yahtzee.players_names.clear()

        self.yahtzee.create_players()

        self.assertEqual(self.yahtzee.players_names, ['John', 'John'])

    # TODO: below testing of yahtzee methods
    # def test_sort_ranking_dict(self):
    #     """
    #     Tests getting ranking dict of player and grand total score
    #     """
    #     pass

    # def test_set_datetime_today(self):
    #     """
    #     Tests setting date today object for File I/O.
    #     """
    #     pass

    # def test_reset_player_scores(self):
    #     """
    #     Tests reseting scores in all Player class instances for next game.
    #     """
    #     pass

    # def test_print_current_scores(self):
    #     """
    #     Tests Printing current scores and totals before rolling.
    #     """
    #     pass

    # def test_roll_the_dice(self):
    #     """
    #     Tests rolling dice during a player's turn and printing results.
    #     """
    #     pass

    # def test_check_top_score(self):
    #     """
    #     Tests checking & setting score in top scores section of scoring_dict.
    #     """
    #     pass

    # def test_check_bottom_score(self):
    #     """
    #     Tests checking & setting score in top scores section of scoring_dict.
    #     """
    #     pass

    # def test_print_end_of_turn_grand_total(self):
    #     """
    #     Tests printing grand total score for end of player turn.
    #     """
    #     pass

    # def test_print_end_of_round_rankings(self):
    #     """
    #     Tests printing player rankings and grand total scores.
    #     """
    #     pass

    # def test_end_of_game(self):
    #     """
    #     Tests increment game_counter; setting game_over True if count == 3.
    #     """
    #     pass

    # def test_yahtzee_rounds(self):
    #     """
    #     Tests round logic taken by each player within a game.
    #     """
    #     pass

    # def test_play(self):
    #     """
    #     Tests initializing players and rolls instances.
    #     """
    #     pass

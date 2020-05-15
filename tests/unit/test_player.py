"""Unit tests for player.py"""

import unittest
from unittest.mock import patch

from yahtzee.player import Player


class TestPlayer(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """
        Using setUpClass class method for visibility and practice utility.
        No real purpose beyond creating namespace and viewing print output.
        """
        pass

    @classmethod
    def tearDownClass(cls):
        """
        Using tearDownClass class method for visibility and practice utility.
        No real purpose beyond creating namespace and viewing print output.
        """
        pass

    def setUp(self):
        """
        Sets up class instances required for all testing methods.
        """
        # construct instance of Player
        self.player = Player('John Smith')

    def tearDown(self):
        """
        Using tearDown instance method here for visibility on utility.
        No real purpose beyond creating namespace and viewing print output.
        """
        pass

    def test_instance_attributes(self):
        """
        Test all instance attributes of class constructor __init__():
        """
        self.assertEqual(self.player.name, 'John Smith')
        self.assertEqual(self.player.score_dict, {
            'ones': False, 'twos': False, 'threes': False, 'fours': False,
            'fives': False, 'sixes': False, 'three of a kind': False,
            'four of a kind': False, 'full house': False,
            'small straight': False, 'large straight': False, 'yahtzee': False,
            'chance': False, 'yahtzee bonus': False,
            })
        self.assertEqual(self.player.top_score, 0)
        self.assertEqual(self.player.top_bonus_score, 0)
        self.assertEqual(self.player.top_bonus_score_delta, 0)
        self.assertEqual(self.player.total_top_score, 0)
        self.assertEqual(self.player.total_bottom_score, 0)
        self.assertEqual(self.player.grand_total_score, 0)

        self.assertEqual(self.player.score_options, [])

    def test_get_score_options(self):
        """
        Tests creation of score options list from not False dict item values.
        """
        self.player.score_dict = {
            'ones': 6, 'twos': False, 'threes': False, 'fours': False,
            'fives': 25, 'sixes': False, 'three of a kind': False,
            'four of a kind': 30, 'full house': False,
            'small straight': 30, 'large straight': False, 'yahtzee': False,
            'chance': 30, 'yahtzee bonus': False,
            }

        self.player.get_score_options()

        self.assertEqual(
            self.player.score_options, ['twos', 'threes', 'fours',
                                        'sixes', 'three of a kind',
                                        'full house',
                                        'large straight',
                                        'yahtzee',
                                        'yahtzee bonus',
                                        ])

    @patch('yahtzee.player.Player.confirm_select_score_option',
           spec=True, return_value='yes')
    @patch('yahtzee.player.Player.select_score_option',
           spec=True, return_value='sixes')
    @patch('yahtzee.player.Player.get_score_options',
           spec=True, return_value=['sixes', 'yahtzee', 'yahtzee bonus'])
    def test_select_score(self, mock_score_options, mock_select_score_option,
                          mock_confirm_select_score_option):
        """
        Tests the selection of a valid scoring option.
        """
        final_roll = [2, 3, 4, 5, 6]

        scoring_option = self.player.select_score(final_roll)

        self.assertEqual(scoring_option, 'sixes')

    @patch('yahtzee.player.Player.confirm_select_score_option',
           spec=True, return_value='yes')
    @patch('yahtzee.player.Player.select_score_option',
           spec=True, return_value='yahtzee bonus')
    @patch('yahtzee.player.Player.get_score_options',
           spec=True, return_value=['yahtzee bonus'])
    def test_select_score_yahtzee_Bonus(self, mock_score_options,
                                        mock_select_score_option,
                                        mock_confirm_select_score_option):
        """
        Tests selecting 'yahtzee bonus' as valid final scoring option.
        """
        # set 'yahtzee' as 50 to pass validation (yahtzee before yahtzee bonus)
        self.player.score_dict['yahtzee'] = 50
        final_roll = [2, 3, 4, 5, 6]

        scoring_option = self.player.select_score(final_roll)

        self.assertEqual(scoring_option, 'yahtzee bonus')

    def test_add_top_bonus_score_delta(self):
        """
        Tests adding top bonus and incrementing delta if top score > threshold.
        """
        self.player.top_score = 63
        self.player.top_bonus_score = 0

        self.player.add_top_bonus_score()

        self.assertEqual(self.player.top_bonus_score, 35)
        self.assertEqual(self.player.top_bonus_score_delta, 35)
        self.assertEqual(self.player.top_score, 63)

    def test_add_top_bonus_score_no_delta(self):
        """
        Tests not incrementing delta if top score > threshold and top bonus
        already obtained.
        """
        self.player.top_score = 63
        self.player.top_bonus_score = 35

        self.player.add_top_bonus_score()

        self.assertEqual(self.player.top_bonus_score, 35)
        self.assertEqual(self.player.top_bonus_score_delta, 0)
        self.assertEqual(self.player.top_score, 63)

    def test_reset_all_scores(self):
        """
        Tests clearing score_dict; setting top, bottom, grand total score to 0.
        """
        self.player.score_dict = {
            'ones': 5, 'twos': 10, 'threes': 15, 'fours': 20,
            'fives': 25, 'sixes': 30, 'three of a kind': 30,
            'four of a kind': 30, 'full house': 25,
            'small straight': 30, 'large straight': 30, 'yahtzee': 50,
            'chance': 30, 'yahtzee bonus': 50,
            }
        self.player.top_score = 100
        self.player.top_bonus_score = 100
        self.player.total_top_score = 100
        self.player.total_bottom_score = 100
        self.player.grand_total_score = 100

        self.player.reset_all_scores()

        self.assertEqual(self.player.score_dict, {
            'ones': False, 'twos': False, 'threes': False, 'fours': False,
            'fives': False, 'sixes': False, 'three of a kind': False,
            'four of a kind': False, 'full house': False,
            'small straight': False, 'large straight': False, 'yahtzee': False,
            'chance': False, 'yahtzee bonus': False,
            })
        self.assertEqual(self.player.top_score, 0)
        self.assertEqual(self.player.top_bonus_score, 0)
        self.assertEqual(self.player.total_top_score, 0)
        self.assertEqual(self.player.total_bottom_score, 0)
        self.assertEqual(self.player.grand_total_score, 0)


if __name__ == '__main__':
    unittest.main()

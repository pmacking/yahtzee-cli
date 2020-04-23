"""Unit tests for player.py"""

import unittest
from unittest.mock import patch

from player import Player


class TestPlayer(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """
        Using setUpClass class method for visibility and practice utility.
        No real purpose beyond creating namespace and viewing print output.
        """
        print('setUpClass class method')

    @classmethod
    def tearDownClass(cls):
        """
        Using tearDownClass class method for visibility and practice utility.
        No real purpose beyond creating namespace and viewing print output.
        """
        print('tearDownClass class method')

    def setUp(self):
        """
        Sets up class instances required for all testing methods.
        """
        print('setUp')

        # construct instance of Player
        self.player = Player('John Smith')

    def tearDown(self):
        """
        Using tearDown instance method here for visibility on utility.
        No real purpose beyond creating namespace and viewing print output.
        """
        print('tearDown')

    def test_instanceAttributes(self):
        """
        Test all instance attributes of class constructor __init__():
        """
        self.assertEqual(self.player.name, 'John Smith')
        self.assertEqual(self.player.scoreDict, {
            'ones': False, 'twos': False, 'threes': False, 'fours': False,
            'fives': False, 'sixes': False, 'three of a kind': False,
            'four of a kind': False, 'full house': False,
            'small straight': False, 'large straight': False, 'yahtzee': False,
            'chance': False, 'yahtzee bonus': False,
            })
        self.assertEqual(self.player.topScore, 0)
        self.assertEqual(self.player.topBonusScore, 0)
        self.assertEqual(self.player.topBonusScoreDelta, 0)
        self.assertEqual(self.player.totalTopScore, 0)
        self.assertEqual(self.player.totalBottomScore, 0)
        self.assertEqual(self.player.grandTotalScore, 0)

        self.assertEqual(self.player.scoreOptions, [])

    def test_getScoreOptions(self):
        """
        Tests creation of score options list from not False dict item values.
        """
        self.player.scoreDict = {
            'ones': 6, 'twos': False, 'threes': False, 'fours': False,
            'fives': 25, 'sixes': False, 'three of a kind': False,
            'four of a kind': 30, 'full house': False,
            'small straight': 30, 'large straight': False, 'yahtzee': False,
            'chance': 30, 'yahtzee bonus': False,
            }

        self.player.getScoreOptions()

        self.assertEqual(self.player.scoreOptions, ['twos', 'threes', 'fours',
                                                    'sixes', 'three of a kind',
                                                    'full house',
                                                    'large straight',
                                                    'yahtzee',
                                                    'yahtzee bonus',
                                                    ])

    @patch('player.Player.confirmSelectScoreOption',
           spec=True, return_value='yes')
    @patch('player.Player.selectScoreOption',
           spec=True, return_value='sixes')
    @patch('player.Player.getScoreOptions',
           spec=True, return_value=['sixes', 'yahtzee', 'yahtzee bonus'])
    def test_selectScore(self, mock_scoreOptions, mock_selectScoreOption,
                         mock_confirmSelectScoreOption):
        """
        Tests the selection of a valid scoring option.
        """
        finalRoll = [2, 3, 4, 5, 6]

        scoringOption = self.player.selectScore(finalRoll)

        self.assertEqual(scoringOption, 'sixes')

    @patch('player.Player.confirmSelectScoreOption',
           spec=True, return_value='yes')
    @patch('player.Player.selectScoreOption',
           spec=True, return_value='yahtzee bonus')
    @patch('player.Player.getScoreOptions',
           spec=True, return_value=['yahtzee bonus'])
    def test_selectScore_yahtzeeBonus(self, mock_scoreOptions,
                                      mock_selectScoreOption,
                                      mock_confirmSelectScoreOption):
        """
        Tests selecting 'yahtzee bonus' as valid final scoring option.
        """
        # set 'yahtzee' as 50 to pass validation (yahtzee before yahtzee bonus)
        self.player.scoreDict['yahtzee'] = 50
        finalRoll = [2, 3, 4, 5, 6]

        scoringOption = self.player.selectScore(finalRoll)

        self.assertEqual(scoringOption, 'yahtzee bonus')

    def test_addTopBonusScore_delta(self):
        """
        Tests adding top bonus and incrementing delta if top score > threshold.
        """
        self.player.topScore = 63
        self.player.topBonusScore = 0

        self.player.addTopBonusScore()

        self.assertEqual(self.player.topBonusScore, 35)
        self.assertEqual(self.player.topBonusScoreDelta, 35)
        self.assertEqual(self.player.topScore, 63)

    def test_addTopBonusScore_noDelta(self):
        """
        Tests not incrementing delta if top score > threshold and top bonus
        already obtained.
        """
        self.player.topScore = 63
        self.player.topBonusScore = 35

        self.player.addTopBonusScore()

        self.assertEqual(self.player.topBonusScore, 35)
        self.assertEqual(self.player.topBonusScoreDelta, 0)
        self.assertEqual(self.player.topScore, 63)

    def test_resetAllScores(self):
        """
        Tests clearing scoreDict; setting top, bottom, grand total score to 0.
        """
        self.player.scoreDict = {
            'ones': 5, 'twos': 10, 'threes': 15, 'fours': 20,
            'fives': 25, 'sixes': 30, 'three of a kind': 30,
            'four of a kind': 30, 'full house': 25,
            'small straight': 30, 'large straight': 30, 'yahtzee': 50,
            'chance': 30, 'yahtzee bonus': 50,
            }
        self.player.topScore = 100
        self.player.topBonusScore = 100
        self.player.totalTopScore = 100
        self.player.totalBottomScore = 100
        self.player.grandTotalScore = 100

        self.player.resetAllScores()

        self.assertEqual(self.player.scoreDict, {
            'ones': False, 'twos': False, 'threes': False, 'fours': False,
            'fives': False, 'sixes': False, 'three of a kind': False,
            'four of a kind': False, 'full house': False,
            'small straight': False, 'large straight': False, 'yahtzee': False,
            'chance': False, 'yahtzee bonus': False,
            })
        self.assertEqual(self.player.topScore, 0)
        self.assertEqual(self.player.topBonusScore, 0)
        self.assertEqual(self.player.totalTopScore, 0)
        self.assertEqual(self.player.totalBottomScore, 0)
        self.assertEqual(self.player.grandTotalScore, 0)


if __name__ == '__main__':
    unittest.main()

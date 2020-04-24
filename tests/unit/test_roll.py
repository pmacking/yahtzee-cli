"""Unit tests for roll.py"""

import unittest
from unittest.mock import patch

from yahtzee.roll import Roll


class TestRoll(unittest.TestCase):

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

        # construct instance of Roll
        self.roll = Roll('John Smith')

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
        self.assertEqual(self.roll.name, 'John Smith')
        self.assertEqual(self.roll._currentDiceList, [])
        self.assertEqual(self.roll._keeperDiceList, [])

    # TODO def test_getKeepDiceCheck (mock)
    # TODO def test_getKeepSomeCheck (mock)

    def test_rollDice(self):
        """
        Tests initial dice roll based on current dice and keeper dice lists.
        """
        # create partial current and keeper list to pass into rollDice
        self.roll._currentDiceList = [1, 2, 3]
        self.roll._keeperDiceList = [1, 2, 3]

        self.roll.rollDice()

        self.assertEqual(len(self.roll._currentDiceList), 5)
        self.assertEqual(len(self.roll._keeperDiceList), 0)

        for i, dice in enumerate(self.roll._currentDiceList):
            self.assertTrue(1 <= dice <= 6)

    # set getKeepDiceCheck to return 'yes' to keepAll during this test
    @patch('yahtzee.roll.getKeepDiceCheck', return_value='yes', spec=True)
    def test_keepDice_keepAll(self, mock_input):
        """
        Tests keeping all dice.
        """
        self.roll._currentDiceList = [1, 2, 3, 4, 5]
        self.roll._keeperDiceList = []

        self.roll.keepDice('JOHN SMITH')

        self.assertEqual(self.roll._currentDiceList, [])
        self.assertEqual(self.roll._keeperDiceList, [1, 2, 3, 4, 5])

    # set keepAll as 'no', reRollAll as 'yes' during this test
    @patch('yahtzee.roll.Roll.keepDice', spec=True,
           keepAll='no', reRollAll='yes')
    def test_keepDice_reRollAll(self, mock_keepDice):
        """
        Tests rerolling all dice.
        """
        self.roll._currentDiceList = [1, 2, 3, 4, 5]
        self.roll._keeperDiceList = []

        self.roll.keepDice('JOHN SMITH')

        self.assertEqual(self.roll._currentDiceList, [1, 2, 3, 4, 5])
        self.assertEqual(self.roll._keeperDiceList, [])
        self.assertEqual(len(self.roll._currentDiceList), 5)

    # TODO Mocking issue - can't create two unique MagicMocks from same function. Mocking issue - can't pass attribute strings directly as here.
    # # set keepAll as 'no', reRollAll as 'no', keepSome as '45' during this test
    # @patch('roll.getKeepSomeCheck', spec=True, return_value='45')
    # @patch('roll.Roll.keepDice', spec=True, keepAll='no', reRollAll='no')
    # def test_keepDice_keepSome(self, mock_keepDice, mock_input):
    #     """
    #     Tests keeping some dice.
    #     """
    #     self.roll._currentDiceList = [1, 2, 3, 4, 5]
    #     self.roll._keeperDiceList = []

    #     self.roll.keepDice('JOHN SMITH')

    #     self.assertEqual(self.roll._currentDiceList, [1, 2, 3])
    #     self.assertEqual(self.roll._keeperDiceList, [4, 5])
    #     self.assertTrue(len(self.roll._currentDiceList) == 3)

    def test_reRollDice(self):
        """
        Tests rolling the dice for the second turn.
        """
        self.roll._currentDiceList = [1, 2, 3, ]
        self.roll._keeperDiceList = [1, 2]

        self.roll.reRollDice(self.roll._currentDiceList)

        self.assertEqual(len(self.roll._currentDiceList), 5)
        self.assertEqual(len(self.roll._keeperDiceList), 0)
        self.assertEqual(self.roll._currentDiceList[3], 1)
        self.assertEqual(self.roll._currentDiceList[4], 2)

    # THIS SECTION tests checking score of final roll based on scoring option

    def test_checkSingles_true(self):
        """
        Tests score based on final roll and selecting a singles option.
        """
        referenceValue = 1
        self.roll._currentDiceList = [1, 1, 1, 1, 2]

        checkSinglesScore = self.roll.checkSingles(
                                self.roll._currentDiceList,
                                referenceValue
                                )

        self.assertEqual(checkSinglesScore, 4)
        self.assertNotEqual(checkSinglesScore, sum(self.roll._currentDiceList))

    def test_checkSingles_false(self):
        """
        Tests 0 score based on final roll and selecting a singles option.
        """
        referenceValue = 1
        self.roll._currentDiceList = [2, 3, 4, 5, 6]

        checkSinglesScore = self.roll.checkSingles(
                                self.roll._currentDiceList,
                                referenceValue
                                )

        self.assertEqual(checkSinglesScore, 0)
        self.assertNotEqual(checkSinglesScore, sum(self.roll._currentDiceList))

    def test_checkThreeOfAKind_true(self):
        """
        Tests score based on final roll and selecting three of a kind.
        """
        threeOfAKindFixtures = [[1, 1, 1, 1, 1],
                                [1, 1, 1, 1, 2],
                                [1, 1, 1, 2, 2],
                                [2, 1, 1, 1, 2],
                                [2, 2, 1, 1, 1],
                                [2, 1, 1, 1, 1],
                                ]

        for fixture in threeOfAKindFixtures:
            score = self.roll.checkThreeOfAKind(fixture)

            self.assertEqual(score, sum(fixture))
            self.assertEqual(len(fixture), 5)

    def test_checkThreeOfAKind_false(self):
        """
        Tests 0 score based on final roll and selecting three of a kind.
        """
        notThreeOfAKindFixtures = [[1, 2, 3, 4, 5],
                                   [1, 1, 2, 2, 3],
                                   [1, 1, 2, 3, 4]
                                   ]

        for fixture in notThreeOfAKindFixtures:
            score = self.roll.checkThreeOfAKind(fixture)

            self.assertNotEqual(score, sum(fixture))
            self.assertEqual(score, 0)
            self.assertEqual(len(fixture), 5)

    def test_checkFourOfAKind_true(self):
        """
        Tests score based on final roll and selecting four of a kind.
        """
        fourOfAKindFixtures = [[1, 1, 1, 1, 1],
                               [1, 1, 1, 1, 2],
                               [2, 1, 1, 1, 1],
                               ]

        for fixture in fourOfAKindFixtures:
            score = self.roll.checkFourOfAKind(fixture)

            self.assertEqual(score, sum(fixture))
            self.assertEqual(len(fixture), 5)

    def test_checkFourOfAKind_false(self):
        """
        Tests 0 score based on final roll and selecting four of a kind.
        """
        notFourOfAKindFixtures = [[1, 1, 1, 2, 2],
                                  [2, 1, 1, 1, 2],
                                  [2, 2, 1, 1, 1],
                                  [1, 2, 3, 4, 5],
                                  ]

        for fixture in notFourOfAKindFixtures:
            score = self.roll.checkFourOfAKind(fixture)

            self.assertNotEqual(score, sum(fixture))
            self.assertEqual(score, 0)
            self.assertEqual(len(fixture), 5)

    def test_checkFullHouse_true(self):
        """
        Tests score based on final roll and selecting full house.
        """
        fullHouseFixtures = [[1, 1, 2, 2, 2],
                             [1, 2, 2, 2, 1],
                             [1, 2, 1, 2, 2],
                             [1, 2, 2, 1, 2],
                             [2, 1, 2, 2, 1],
                             [2, 2, 1, 2, 1],
                             [2, 2, 2, 1, 1],
                             ]

        for fixture in fullHouseFixtures:
            score = self.roll.checkFullHouse(fixture)

            self.assertEqual(score, 25)
            self.assertEqual(len(fixture), 5)

    def test_checkFullHouse_false(self):
        """
        Tests 0 score based on final roll and selecting full house.
        """
        notFullHouseFixtures = [[1, 1, 1, 1, 2],
                                [2, 1, 1, 1, 1],
                                [1, 1, 2, 2, 3],
                                [1, 2, 3, 4, 5],
                                ]

        for fixture in notFullHouseFixtures:
            score = self.roll.checkFullHouse(fixture)

            self.assertNotEqual(score, 25)
            self.assertEqual(score, 0)
            self.assertEqual(len(fixture), 5)

    def test_checkSmallStraight_true(self):
        """
        Tests score based on final roll and selecting small straight.
        """
        smallStraightFixtures = [[1, 2, 3, 4, 5],
                                 [1, 2, 3, 4, 6],
                                 [1, 3, 4, 5, 6],
                                 [2, 3, 4, 5, 6],
                                 [1, 2, 3, 4, 4],
                                 [1, 2, 4, 3, 4],
                                 [1, 4, 2, 3, 5],
                                 ]

        for fixture in smallStraightFixtures:
            score = self.roll.checkSmallStraight(fixture)

            self.assertEqual(score, 30)
            self.assertEqual(len(fixture), 5)

    def test_checkSmallStraight_false(self):
        """
        Tests 0 score based on final roll and selecting small straight.
        """
        notSmallStraightFixtures = [[1, 2, 3, 5, 6],
                                    [1, 2, 4, 5, 6],
                                    [1, 2, 3, 5, 5],
                                    [1, 1, 3, 4, 5],
                                    [1, 2, 4, 5, 6],
                                    ]

        for fixture in notSmallStraightFixtures:
            score = self.roll.checkSmallStraight(fixture)

            self.assertEqual(score, 0)
            self.assertEqual(len(fixture), 5)

    def test_checkLargeStraight_true(self):
        """
        Tests score based on final roll and selecting large straight.
        """
        largeStraightFixtures = [[1, 2, 3, 4, 5],
                                 [2, 3, 4, 5, 6],
                                 ]

        for fixture in largeStraightFixtures:
            score = self.roll.checkLargeStraight(fixture)

            self.assertEqual(score, 35)
            self.assertEqual(len(fixture), 5)

    def test_checkLargeStraight_false(self):
        """
        Tests 0 score based on final roll and selecting large straight.
        """
        notLargeStraightFixtures = [[1, 2, 3, 4, 6],
                                    [1, 3, 4, 5, 6],
                                    ]

        for fixture in notLargeStraightFixtures:
            score = self.roll.checkLargeStraight(fixture)

            self.assertNotEqual(score, 35)
            self.assertEqual(score, 0)
            self.assertEqual(len(fixture), 5)

    def test_checkYahtzee_true(self):
        """
        Tests score based on final roll and selecting yahtzee.
        """
        yahtzeeFixtures = [[1, 1, 1, 1, 1],
                           [2, 2, 2, 2, 2],
                           [3, 3, 3, 3, 3],
                           [4, 4, 4, 4, 4],
                           [5, 5, 5, 5, 5],
                           [6, 6, 6, 6, 6],
                           ]

        for fixture in yahtzeeFixtures:
            score = self.roll.checkYahtzee(fixture)

            self.assertEqual(score, 50)
            self.assertEqual(len(fixture), 5)

    def test_checkYahtzee_false(self):
        """
        Tests 0 score based on final roll and selecting yahtzee.
        """
        notYahtzeeFixtures = [[1, 1, 1, 1, 2],
                              [1, 1, 1, 2, 1],
                              [1, 1, 2, 1, 1],
                              [1, 2, 1, 1, 1],
                              [2, 1, 1, 1, 1],
                              ]

        for fixture in notYahtzeeFixtures:
            score = self.roll.checkYahtzee(fixture)

            self.assertNotEqual(score, 50)
            self.assertEqual(score, 0)
            self.assertEqual(len(fixture), 5)

    def test_addChance(self):
        """
        Tests score based on final roll and selecting chance.
        """
        chanceFixtures = [[1, 2, 3, 4, 5],
                          [1, 1, 1, 1, 1],
                          [6, 6, 6, 6, 6],
                          [1, 1, 1, 1, 2],
                          [1, 1, 1, 3, 3],
                          [1, 2, 3, 4, 6],
                          ]

        for fixture in chanceFixtures:
            score = self.roll.addChance(fixture)

            self.assertEqual(score, sum(fixture))
            self.assertNotEqual(score, 0)
            self.assertEqual(len(fixture), 5)

    def test_checkYahtzeeBonus_true(self):
        """
        Tests score based on final roll and selecting yahtzee bonus.
        """

        yahtzeeBonusFixtures = [[1, 1, 1, 1, 1],
                                [2, 2, 2, 2, 2],
                                [3, 3, 3, 3, 3],
                                [4, 4, 4, 4, 4],
                                [5, 5, 5, 5, 5],
                                [6, 6, 6, 6, 6],
                                ]

        for fixture in yahtzeeBonusFixtures:
            score = self.roll.checkYahtzee(fixture)

            self.assertEqual(score, 50)
            self.assertEqual(len(fixture), 5)

    def test_checkYahtzeeBonus_false(self):
        """
        Tests 0 score based on final roll and selecting yahtzee bonus.
        """

        notYahtzeeBonusFixtures = [[1, 1, 1, 1, 2],
                                   [1, 1, 1, 2, 1],
                                   [1, 1, 2, 1, 1],
                                   [1, 2, 1, 1, 1],
                                   [2, 1, 1, 1, 1],
                                   ]

        for fixture in notYahtzeeBonusFixtures:
            score = self.roll.checkYahtzee(fixture)

            self.assertNotEqual(score, 50)
            self.assertEqual(score, 0)
            self.assertEqual(len(fixture), 5)


if __name__ == '__main__':
    unittest.main()

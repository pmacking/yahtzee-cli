"""Unit tests for yahtzee.py"""

import unittest
from unittest.mock import patch

from roll import Roll
from player import Player


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
        self.rollTest = Roll('rollTest')

        # construct instance of Player
        self.playerTest = Player('testPlayer')

    def tearDown(self):
        """
        Using tearDown instance method here for visibility on utility.
        No real purpose beyond creating namespace and viewing print output.
        """
        print('tearDown')

        # # teardown instance of Roll
        # self.rollTest.dispose()

        # # tear down instance of Player
        # self.playerTest.dispose()

    def test_instanceAttributes(self):
        """
        Test all instance attributes of class constructor __init__():
        """
        assert self.rollTest.name == 'rollTest'
        assert self.rollTest._currentDiceList == []
        assert self.rollTest._keeperDiceList == []

    def test_rollDice(self):
        """
        Tests initial dice roll based on current dice and keeper dice lists.
        """
        # create partial current and keeper list to pass into rollDice
        self.rollTest._currentDiceList = [1, 2, 3]
        self.rollTest._keeperDiceList = [1, 2, 3]

        self.rollTest.rollDice()

        assert len(self.rollTest._currentDiceList) == 5
        assert len(self.rollTest._keeperDiceList) == 0

        for i, dice in enumerate(self.rollTest._currentDiceList):
            assert 1 <= dice <= 6

    # set getKeepDiceCheck to return 'yes' to keepAll during this test
    @patch('roll.getKeepDiceCheck', return_value='yes', spec=True)
    def test_keepDice_keepAll(self, mock_input):
        """
        Tests keeping all dice.
        """
        self.rollTest._currentDiceList = [1, 2, 3, 4, 5]
        self.rollTest._keeperDiceList = []

        self.rollTest.keepDice('JOHN SMITH')

        assert self.rollTest._currentDiceList == []
        assert self.rollTest._keeperDiceList == [1, 2, 3, 4, 5]

    # set keepAll as 'no', reRollAll as 'yes' during this test
    @patch('roll.Roll.keepDice', spec=True, keepAll='no', reRollAll='yes')
    def test_keepDice_reRollAll(self, mock_keepDice):
        """
        Tests rerolling all dice.
        """
        self.rollTest._currentDiceList = [1, 2, 3, 4, 5]
        self.rollTest._keeperDiceList = []

        self.rollTest.keepDice('JOHN SMITH')

        assert self.rollTest._currentDiceList == [1, 2, 3, 4, 5]
        assert self.rollTest._keeperDiceList == []
        assert len(self.rollTest._currentDiceList) == 5

    # TODO Mocking issue - can't create two unique MagicMocks from same function. Mocking issue - can't pass attribute strings directly as here.
    # # set keepAll as 'no', reRollAll as 'no', keepSome as '45' during this test
    # @patch('roll.getKeepSomeCheck', spec=True, return_value='45')
    # @patch('roll.Roll.keepDice', spec=True, keepAll='no', reRollAll='no')
    # def test_keepDice_keepSome(self, mock_keepDice, mock_input):
    #     """
    #     Tests keeping some dice.
    #     """
    #     self.rollTest._currentDiceList = [1, 2, 3, 4, 5]
    #     self.rollTest._keeperDiceList = []

    #     self.rollTest.keepDice('JOHN SMITH')

    #     self.assertEqual(self.rollTest._currentDiceList, [1, 2, 3])
    #     self.assertEqual(self.rollTest._keeperDiceList, [4, 5])
    #     self.assertTrue(len(self.rollTest._currentDiceList) == 3)

    def test_reRollDice(self):
        """
        Tests rolling the dice for the second turn.
        """
        self.rollTest._currentDiceList = [1, 2, 3, ]
        self.rollTest._keeperDiceList = [1, 2]

        self.rollTest.reRollDice(self.rollTest._currentDiceList)

        assert len(self.rollTest._currentDiceList) == 5
        assert len(self.rollTest._keeperDiceList) == 0
        assert self.rollTest._currentDiceList[3] == 1
        assert self.rollTest._currentDiceList[4] == 2

    # THIS SECTION tests checking score of final roll based on scoring option

    def test_checkSingles(self):
        """
        Tests score based on final roll and selecting a singles option.
        """

        self.rollTest.checkSingles(self.rollTest._currentDiceList)

    def test_checkThreeOfAKind(self):
        """
        Tests score based on final roll and selecting three of a kind.
        """

        self.rollTest.checkThreeOfAKind(self.rollTest._currentDiceList)

    def test_checkFourOfAKind(self):
        """
        Tests score based on final roll and selecting four of a kind.
        """

        self.rollTest.checkFourOfAKind(self.rollTest._currentDiceList)

    def test_checkFullHouse(self):
        """
        Tests score based on final roll and selecting full house.
        """

        self.rollTest.checkFullHouse(self.rollTest._currentDiceList)

    def test_checkSmallStraight(self):
        """
        Tests score based on final roll and selecting small straight.
        """

        self.rollTest.checkSmallStraight(self.rollTest._currentDiceList)

    def test_checkLargeStraight(self):
        """
        Tests score based on final roll and selecting large straight.
        """

        self.rollTest.checkLargeStraight(self.rollTest._currentDiceList)

    def test_checkYahtzee(self):
        """
        Tests score based on final roll and selecting yahtzee.
        """

        self.rollTest.checkYahtzee(self.rollTest._currentDiceList)

    def test_addChance(self):
        """
        Tests score based on final roll and selecting chance.
        """

        self.rollTest.addChance(self.rollTest._currentDiceList)

    def test_checkYahtzeeBonus(self):
        """
        Tests score based on final roll and selecting yahtzee bonus.
        """

        self.rollTest.checkYahtzeeBonus(self.rollTest._currentDiceList)


if __name__ == '__main__':
    unittest.main()

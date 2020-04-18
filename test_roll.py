"""Unit tests for yahtzee.py"""

import unittest
from roll import Roll
from player import Player


class TestRoll(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """
        Using setUpClass class method for visibility and practice utility.
        No real purpose beyond creating namespace and viewing print output.
        """
        print('setUpClass :class: `Roll <Roll>`')

    @classmethod
    def tearDownClass(cls):
        """
        Using tearDownClass class method for visibility and practice utility.
        No real purpose beyond creating namespace and viewing print output.
        """
        print('tearDownClass :class: `Roll <Roll>`')

    def setUp(self):
        """
        Sets up class instances required for all testing methods.
        """
        print('setUp rollTest instance')

        # construct instance of Roll
        self.rollTest = Roll('rollTest')

        # construct instance of Player
        self.playerTest = Player('testPlayer')

    def tearDown(self):
        """
        Using tearDown instance method here for visibility on utility.
        No real purpose beyond creating namespace and viewing print output.
        """
        print('tearDown rollTest instance')

        # # teardown instance of Roll
        # self.rollTest.dispose()

        # # tear down instance of Player
        # self.playerTest.dispose()

    def test_instanceAttributes(self):
        """
        Test all instance attributes of class constructor __init__():
        """
        self.assertEqual(self.rollTest.name, 'rollTest')
        self.assertEqual(self.rollTest._currentDiceList, [])
        self.assertEqual(self.rollTest._keeperDiceList, [])

    def test_rollDice(self):
        """
        Tests initial dice roll based on current dice and keeper dice lists.
        """
        # create partial current and keeper list to pass into rollDice
        self.rollTest._currentDiceList = [1, 2, 3]
        self.rollTest._keeperDiceList = [1, 2, 3]

        self.rollTest.rollDice()

        self.assertEqual(len(self.rollTest._currentDiceList), 5)
        self.assertEqual(len(self.rollTest._keeperDiceList), 0)

        for i, dice in enumerate(self.rollTest._currentDiceList):
            self.assertTrue(1 <= dice <= 6)


if __name__ == '__main__':
    unittest.main()

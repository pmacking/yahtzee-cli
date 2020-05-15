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
        # construct instance of Roll
        self.roll = Roll('John Smith')

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
        self.assertEqual(self.roll.name, 'John Smith')
        self.assertEqual(self.roll.current_dice_list, [])
        self.assertEqual(self.roll.keeper_dice_list, [])

    # TODO def test_get_keep_dice_check (mock)
    # TODO def test_getKeepSomeCheck (mock)

    def test_roll_dice(self):
        """
        Tests initial dice roll based on current dice and keeper dice lists.
        """
        # create partial current and keeper list to pass into roll_dice
        self.roll.current_dice_list = [1, 2, 3]
        self.roll.keeper_dice_list = [1, 2, 3]

        self.roll.roll_dice()

        self.assertEqual(len(self.roll.current_dice_list), 5)
        self.assertEqual(len(self.roll.keeper_dice_list), 0)

        for i, dice in enumerate(self.roll.current_dice_list):
            self.assertTrue(1 <= dice <= 6)

    # set get_keep_dice_check to return 'yes' to keep_all during this test
    @patch('yahtzee.roll.get_keep_dice_check', return_value='yes', spec=True)
    def test_keep_dice_keep_all(self, mock_input):
        """
        Tests keeping all dice.
        """
        self.roll.current_dice_list = [1, 2, 3, 4, 5]
        self.roll.keeper_dice_list = []

        self.roll.keep_dice('JOHN SMITH')

        self.assertEqual(self.roll.current_dice_list, [])
        self.assertEqual(self.roll.keeper_dice_list, [1, 2, 3, 4, 5])

    # set keep_all as 'no', reroll_all as 'yes' during this test
    @patch('yahtzee.roll.Roll.keep_dice', spec=True,
           keep_all='no', reroll_all='yes')
    def test_keep_dice_reroll_all(self, mock_keep_dice):
        """
        Tests rerolling all dice.
        """
        self.roll.current_dice_list = [1, 2, 3, 4, 5]
        self.roll.keeper_dice_list = []

        self.roll.keep_dice('JOHN SMITH')

        self.assertEqual(self.roll.current_dice_list, [1, 2, 3, 4, 5])
        self.assertEqual(self.roll.keeper_dice_list, [])
        self.assertEqual(len(self.roll.current_dice_list), 5)

    # TODO Mocking issue - can't create two unique MagicMocks from same function. Mocking issue - can't pass attribute strings directly as here.
    # # set keep_all as 'no', reroll_all as 'no', keepSome as '45' during this test
    # @patch('roll.getKeepSomeCheck', spec=True, return_value='45')
    # @patch('roll.Roll.keep_dice', spec=True, keep_all='no', reroll_all='no')
    # def test_keep_dice_keepSome(self, mock_keep_dice, mock_input):
    #     """
    #     Tests keeping some dice.
    #     """
    #     self.roll.current_dice_list = [1, 2, 3, 4, 5]
    #     self.roll.keeper_dice_list = []

    #     self.roll.keep_dice('JOHN SMITH')

    #     self.assertEqual(self.roll.current_dice_list, [1, 2, 3])
    #     self.assertEqual(self.roll.keeper_dice_list, [4, 5])
    #     self.assertTrue(len(self.roll.current_dice_list) == 3)

    def test_reroll_dice(self):
        """
        Tests rolling the dice for the second turn.
        """
        self.roll.current_dice_list = [1, 2, 3, ]
        self.roll.keeper_dice_list = [1, 2]

        self.roll.reroll_dice(self.roll.current_dice_list)

        self.assertEqual(len(self.roll.current_dice_list), 5)
        self.assertEqual(len(self.roll.keeper_dice_list), 0)
        self.assertEqual(self.roll.current_dice_list[3], 1)
        self.assertEqual(self.roll.current_dice_list[4], 2)

    # THIS SECTION tests checking score of final roll based on scoring option

    def test_check_singles_true(self):
        """
        Tests score based on final roll and selecting a singles option.
        """
        reference_value = 1
        self.roll.current_dice_list = [1, 1, 1, 1, 2]

        check_singles_score = self.roll.check_singles(
                                self.roll.current_dice_list,
                                reference_value
                                )

        self.assertEqual(check_singles_score, 4)
        self.assertNotEqual(check_singles_score,
                            sum(self.roll.current_dice_list))

    def test_check_singles_false(self):
        """
        Tests 0 score based on final roll and selecting a singles option.
        """
        reference_value = 1
        self.roll.current_dice_list = [2, 3, 4, 5, 6]

        check_singles_score = self.roll.check_singles(
                                self.roll.current_dice_list,
                                reference_value
                                )

        self.assertEqual(check_singles_score, 0)
        self.assertNotEqual(check_singles_score,
                            sum(self.roll.current_dice_list))

    def test_check_three_of_a_kind_true(self):
        """
        Tests score based on final roll and selecting three of a kind.
        """
        three_of_a_kind_fixtures = [[1, 1, 1, 1, 1],
                                    [1, 1, 1, 1, 2],
                                    [1, 1, 1, 2, 2],
                                    [2, 1, 1, 1, 2],
                                    [2, 2, 1, 1, 1],
                                    [2, 1, 1, 1, 1],
                                    ]

        for fixture in three_of_a_kind_fixtures:
            score = self.roll.check_three_of_a_kind(fixture)

            self.assertEqual(score, sum(fixture))
            self.assertEqual(len(fixture), 5)

    def test_check_three_of_a_kind_false(self):
        """
        Tests 0 score based on final roll and selecting three of a kind.
        """
        not_three_of_a_kind_fixtures = [[1, 2, 3, 4, 5],
                                        [1, 1, 2, 2, 3],
                                        [1, 1, 2, 3, 4]
                                        ]

        for fixture in not_three_of_a_kind_fixtures:
            score = self.roll.check_three_of_a_kind(fixture)

            self.assertNotEqual(score, sum(fixture))
            self.assertEqual(score, 0)
            self.assertEqual(len(fixture), 5)

    def test_check_four_of_a_kind_true(self):
        """
        Tests score based on final roll and selecting four of a kind.
        """
        four_of_a_kind_fixtures = [[1, 1, 1, 1, 1],
                                   [1, 1, 1, 1, 2],
                                   [2, 1, 1, 1, 1],
                                   ]

        for fixture in four_of_a_kind_fixtures:
            score = self.roll.check_four_of_a_kind(fixture)

            self.assertEqual(score, sum(fixture))
            self.assertEqual(len(fixture), 5)

    def test_check_four_of_a_kindfalse(self):
        """
        Tests 0 score based on final roll and selecting four of a kind.
        """
        not_four_of_a_kind_fixtures = [[1, 1, 1, 2, 2],
                                       [2, 1, 1, 1, 2],
                                       [2, 2, 1, 1, 1],
                                       [1, 2, 3, 4, 5],
                                       ]

        for fixture in not_four_of_a_kind_fixtures:
            score = self.roll.check_four_of_a_kind(fixture)

            self.assertNotEqual(score, sum(fixture))
            self.assertEqual(score, 0)
            self.assertEqual(len(fixture), 5)

    def test_check_full_house_true(self):
        """
        Tests score based on final roll and selecting full house.
        """
        full_house_fixtures = [[1, 1, 2, 2, 2],
                               [1, 2, 2, 2, 1],
                               [1, 2, 1, 2, 2],
                               [1, 2, 2, 1, 2],
                               [2, 1, 2, 2, 1],
                               [2, 2, 1, 2, 1],
                               [2, 2, 2, 1, 1],
                               ]

        for fixture in full_house_fixtures:
            score = self.roll.check_full_house(fixture)

            self.assertEqual(score, 25)
            self.assertEqual(len(fixture), 5)

    def test_check_full_house_false(self):
        """
        Tests 0 score based on final roll and selecting full house.
        """
        not_full_house_fixtures = [[1, 1, 1, 1, 2],
                                   [2, 1, 1, 1, 1],
                                   [1, 1, 2, 2, 3],
                                   [1, 2, 3, 4, 5],
                                   ]

        for fixture in not_full_house_fixtures:
            score = self.roll.check_full_house(fixture)

            self.assertNotEqual(score, 25)
            self.assertEqual(score, 0)
            self.assertEqual(len(fixture), 5)

    def test_check_small_straight_true(self):
        """
        Tests score based on final roll and selecting small straight.
        """
        small_straight_fixtures = [[1, 2, 3, 4, 5],
                                   [1, 2, 3, 4, 6],
                                   [1, 3, 4, 5, 6],
                                   [2, 3, 4, 5, 6],
                                   [1, 2, 3, 4, 4],
                                   [1, 2, 4, 3, 4],
                                   [1, 4, 2, 3, 5],
                                   ]

        for fixture in small_straight_fixtures:
            score = self.roll.check_small_straight(fixture)

            self.assertEqual(score, 30)
            self.assertEqual(len(fixture), 5)

    def test_check_small_straight_false(self):
        """
        Tests 0 score based on final roll and selecting small straight.
        """
        not_small_straight_fixtures = [[1, 2, 3, 5, 6],
                                       [1, 2, 4, 5, 6],
                                       [1, 2, 3, 5, 5],
                                       [1, 1, 3, 4, 5],
                                       [1, 2, 4, 5, 6],
                                       ]

        for fixture in not_small_straight_fixtures:
            score = self.roll.check_small_straight(fixture)

            self.assertEqual(score, 0)
            self.assertEqual(len(fixture), 5)

    def test_check_large_straight_true(self):
        """
        Tests score based on final roll and selecting large straight.
        """
        large_straight_fixtures = [[1, 2, 3, 4, 5],
                                   [2, 3, 4, 5, 6],
                                   ]

        for fixture in large_straight_fixtures:
            score = self.roll.check_large_straight(fixture)

            self.assertEqual(score, 35)
            self.assertEqual(len(fixture), 5)

    def test_check_large_straight_false(self):
        """
        Tests 0 score based on final roll and selecting large straight.
        """
        not_large_straight_fixtures = [[1, 2, 3, 4, 6],
                                       [1, 3, 4, 5, 6],
                                       ]

        for fixture in not_large_straight_fixtures:
            score = self.roll.check_large_straight(fixture)

            self.assertNotEqual(score, 35)
            self.assertEqual(score, 0)
            self.assertEqual(len(fixture), 5)

    def test_check_yahtzee_true(self):
        """
        Tests score based on final roll and selecting yahtzee.
        """
        yahtzee_fixtures = [[1, 1, 1, 1, 1],
                            [2, 2, 2, 2, 2],
                            [3, 3, 3, 3, 3],
                            [4, 4, 4, 4, 4],
                            [5, 5, 5, 5, 5],
                            [6, 6, 6, 6, 6],
                            ]

        for fixture in yahtzee_fixtures:
            score = self.roll.check_yahtzee(fixture)

            self.assertEqual(score, 50)
            self.assertEqual(len(fixture), 5)

    def test_check_yahtzee_false(self):
        """
        Tests 0 score based on final roll and selecting yahtzee.
        """
        not_yahtzee_fixtures = [[1, 1, 1, 1, 2],
                                [1, 1, 1, 2, 1],
                                [1, 1, 2, 1, 1],
                                [1, 2, 1, 1, 1],
                                [2, 1, 1, 1, 1],
                                ]

        for fixture in not_yahtzee_fixtures:
            score = self.roll.check_yahtzee(fixture)

            self.assertNotEqual(score, 50)
            self.assertEqual(score, 0)
            self.assertEqual(len(fixture), 5)

    def test_add_chance(self):
        """
        Tests score based on final roll and selecting chance.
        """
        chance_fixtures = [[1, 2, 3, 4, 5],
                           [1, 1, 1, 1, 1],
                           [6, 6, 6, 6, 6],
                           [1, 1, 1, 1, 2],
                           [1, 1, 1, 3, 3],
                           [1, 2, 3, 4, 6],
                           ]

        for fixture in chance_fixtures:
            score = self.roll.add_chance(fixture)

            self.assertEqual(score, sum(fixture))
            self.assertNotEqual(score, 0)
            self.assertEqual(len(fixture), 5)

    def test_check_yahtzee_bonus_true(self):
        """
        Tests score based on final roll and selecting yahtzee bonus.
        """

        yahtzee_bonus_fixtures = [[1, 1, 1, 1, 1],
                                  [2, 2, 2, 2, 2],
                                  [3, 3, 3, 3, 3],
                                  [4, 4, 4, 4, 4],
                                  [5, 5, 5, 5, 5],
                                  [6, 6, 6, 6, 6],
                                  ]

        for fixture in yahtzee_bonus_fixtures:
            score = self.roll.check_yahtzee_bonus(fixture)

            self.assertEqual(score, 50)
            self.assertEqual(len(fixture), 5)

    def test_check_yahtzee_bonus_false(self):
        """
        Tests 0 score based on final roll and selecting yahtzee bonus.
        """

        not_yahtzee_bonus_fixtures = [[1, 1, 1, 1, 2],
                                      [1, 1, 1, 2, 1],
                                      [1, 1, 2, 1, 1],
                                      [1, 2, 1, 1, 1],
                                      [2, 1, 1, 1, 1],
                                      ]

        for fixture in not_yahtzee_bonus_fixtures:
            score = self.roll.check_yahtzee_bonus(fixture)

            self.assertNotEqual(score, 50)
            self.assertEqual(score, 0)
            self.assertEqual(len(fixture), 5)


if __name__ == '__main__':
    unittest.main()

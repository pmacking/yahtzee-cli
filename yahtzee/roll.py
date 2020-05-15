#! python3

"""
This module controls rolling and checking of scores.

github.com/pmacking/roll.py
"""

from random import randint
import pyinputplus as pyip


def get_keep_dice_check(input_prompt):
    """
    Enables returning a yes or no response to an input prompt.

    :param input_prompt: String yes no question.
    """
    return pyip.inputYesNo(prompt=input_prompt)


def get_keep_some_check(input_prompt):
    """
    Enables returning integer input, as well as a blank input.

    :param input_prompt: String prompt asking for integer of dice.
    """
    return pyip.inputInt(prompt=input_prompt, blank=True)


class Roll:
    """
    Objects instantiated by the :class:`Roll <Roll>` can be called to roll
    dice and check scores.
    """
    def __init__(self, name):
        """
        Class containing dice lists, and methods for rolling/keeping dice
        """
        self.name = name
        self.current_dice_list = []
        self.keeper_dice_list = []

    def __repr__(self):
        return (f"{self.__class__.__name__}("
                f"{self.current_dice_list!r}, {self.keeper_dice_list})")

    # This section outlines dice roll actions
    def roll_dice(self):
        """
        Method that determines the first dice roll
        :return: The first roll result.
        """
        # clear current and keeper lists from previous roll
        self.keeper_dice_list.clear()
        self.current_dice_list.clear()

        # set current dice list to five random int between 1 and 6
        self.current_dice_list = [randint(1, 6) for d in range(5)]

        return self.current_dice_list

    def keep_dice(self, player_name_caps):
        """
        Method that allows keeping all, rerolling all, or selecting dice

        :param player_name_caps: Capitalized player name.
        :return: Current dice list.
        """

        # ask if user wants to KEEP ALL the dice
        keep_all = get_keep_dice_check(f"{player_name_caps} do you want to "
                                       f"KEEP ALL dice?\n")
        if keep_all == 'no':

            # ask if the user wants to REROLL ALL the dice
            reroll_all = get_keep_dice_check(f"Do you want to REROLL ALL "
                                             f"dice?\n")
            if reroll_all == 'no':

                while True:

                    # ask the user what dice to KEEP
                    keep_some = get_keep_some_check(
                                    "Enter the dice you would "
                                    "like to KEEP (ex: 456):\n")
                    if keep_some == '':

                        # validate empty string and intent to REROLL ALL
                        keep_none_check = get_keep_dice_check(
                                            f"Are you sure you want to REROLL "
                                            f"ALL the dice?\n")

                        if keep_none_check == 'yes':
                            return self.current_dice_list

                        else:
                            continue

                    else:
                        # convert keep_some int to list of 'split' int
                        keep_some_list = [int(d) for d in str(keep_some)]

                        # if keeper in current dice, remove and add to keeper
                        for d in keep_some_list:
                            if d in self.current_dice_list:
                                self.current_dice_list.remove(d)
                                self.keeper_dice_list.append(d)

                        return self.current_dice_list

            else:
                return self.current_dice_list

        else:
            # make keeper dice list same as current dice list
            self.keeper_dice_list = [d for d in self.current_dice_list]

            # clear current dice
            self.current_dice_list.clear()

            return self.current_dice_list

    def reroll_dice(self, dice_list):
        """
        Method that rolls dice another time.

        :param dice_list: list of current dice from previous roll.
        :return: The second roll result.
        """
        # roll current dice from previous roll
        self.current_dice_list = [randint(1, 6) for d in range(
                                 0, (len(dice_list)))]

        # add the newly rolled current dice to keepers
        self.current_dice_list = self.current_dice_list + self.keeper_dice_list

        # clear keepers list
        self.keeper_dice_list.clear()

        return self.current_dice_list

    # This section checks scoring of final roll

    def check_singles(self, dice_list, reference_value):
        """
        Checks the value of selected singles and updates scoring dictionary

        :param dice_list: The final roll.
        :param reference_value: Ref value of the selected scoring option.
        :return: Score for the singles option selected.
        """
        check_singles_score = 0

        for d in dice_list:
            if d == reference_value:
                check_singles_score += d

        return check_singles_score

    def check_three_of_a_kind(self, dice_list):
        """
        Checks if there are three of a kind; if so sums all dice as score.

        :param dice_list: The final roll.
        :return: Score for three of a kind.
        """
        dice_list.sort()

        if dice_list[0] == dice_list[2] or dice_list[1] == dice_list[3] or \
           dice_list[2] == dice_list[4]:
            return sum(dice_list)
        return 0

    def check_four_of_a_kind(self, dice_list):
        """
        Checks if there are four of a kind; if so sums all dice as score.

        :param dice_list: The final roll.
        :return: Score for four of a kind.
        """
        dice_list.sort()

        if dice_list[0] == dice_list[3] or dice_list[1] == dice_list[4]:
            return sum(dice_list)
        return 0

    def check_full_house(self, dice_list):
        """
        Checks for full house; if so returns 25 as score.

        :param dice_list: The final roll.
        :return: Score for full house.
        """
        if (len(set(dice_list)) == 2 and
                len([d for d in dice_list if dice_list.count(d) == 3]) == 3):
            return 25

        return 0

    def check_small_straight(self, dice_list):
        """
        Checks for small straight (4 sequential); if True adds 30 as score.

        :param dice_list: The final roll.
        :return: Score for small straight.
        """

        dice_list.sort()
        dice_list_set = list(set(dice_list))

        # if 5 unique dice, valids against valid options
        if len(set(dice_list_set)) == 5:

            valid_options = [[1, 2, 3, 4, 5],
                             [1, 2, 3, 4, 6],
                             [1, 3, 4, 5, 6],
                             [2, 3, 4, 5, 6],
                             ]
            if dice_list_set in valid_options:
                return 30

            else:
                return 0

        # if four unique dice, checks they are sequential
        elif len(set(dice_list_set)) == 4:

            sequential = 0
            for i, d in enumerate(dice_list_set[:-1]):
                if dice_list_set[i + 1] == dice_list_set[i] + 1:
                    sequential += 1

            if sequential == 3:
                return 30

            else:
                return 0

        else:
            return 0

    def check_large_straight(self, dice_list):
        """
        Checks for large straight (5 sequential); if True adds 35 to score.

        :param dice_list: The final roll.
        :return: Score for large straight.
        """
        dice_list.sort()

        # checks for large straight 2 to 6
        if len(set(dice_list)) == 5 \
                and dice_list[0] == 2 and dice_list[4] == 6:
            return 35

        # checks for large straight 1 to 5
        elif len(set(dice_list)) == 5 \
                and dice_list[0] == 1 and dice_list[4] == 5:
            return 35

        else:
            return 0

    def check_yahtzee(self, dice_list):
        """
        Checks for yahtzee (five of a kind), and if True adds 50 to score.

        :param dice_list: The final roll.
        :return: Score for yahtzee.
        """
        if len(set(dice_list)) == 1:
            return 50

        return 0

    def add_chance(self, dice_list):
        """
        Sum the dice score for chance score.

        :param dice_list: The final roll.
        :return: Score for chance.
        """
        return sum(dice_list)

    def check_yahtzee_bonus(self, dice_list):
        """
        Checks for yahtzee (five of a kind), and if True adds 50 to score.

        :param dice_list: The final roll.
        :return: Score for yahtzee bonus.
        """
        if len(set(dice_list)) == 1:
            return 50

        return 0

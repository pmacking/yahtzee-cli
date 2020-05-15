#! python3

"""
This module controls player instantiation and score keeping.

github.com/pmacking/player.py
"""

import pyinputplus as pyip


class Player:
    """
    Objects instantiated by the :class:`Player <Player>` can be called to
    create players and influence scores.
    """
    def __init__(self, name):
        self.name = name
        self.score_dict = {
            'ones': False, 'twos': False, 'threes': False, 'fours': False,
            'fives': False, 'sixes': False, 'three of a kind': False,
            'four of a kind': False, 'full house': False,
            'small straight': False, 'large straight': False, 'yahtzee': False,
            'chance': False, 'yahtzee bonus': False,
            }
        self.top_score = 0
        self.top_bonus_score = 0
        self.top_bonus_score_delta = 0
        self.total_top_score = 0
        self.total_bottom_score = 0
        self.grand_total_score = 0

        self.score_options = []

    def __repr__(self):
        return (f"{self.__class__.__name__}("
                f"{self.name}, {self.score_dict!r}, "
                f"{self.top_score!r}, {self.top_bonus_score!r}, "
                f"{self.total_bottom_score!r}, {self.grand_total_score!r})")

    def get_score_options(self):
        """
        Gets list of non-False scoring options from score_dict.

        :returns: Score options list.
        """
        self.score_options = []

        # create score_options list
        for i, option in enumerate(self.score_dict):
            if self.score_dict[option] is False:
                self.score_options.append(option)

        return self.score_options

    def select_score_option(self, score_options):
        """
        Player inputs score_selected from input menu of score_options.

        :param score_options: List of remaining score options.
        :return: The score option selected from the menu.
        """
        # inputMenu can present sigle list item if keyword blank=True
        score_selected = pyip.inputMenu(score_options, numbered=True,
                                        blank=True)
        return score_selected

    def confirm_score_selected(self, score_selected):
        """
        Confirms the score_selected.

        :param score_selected: The score option string selected from the menu.
        :return: 'yes' or 'no' response.
        """
        confirm_score_selected = pyip.inputYesNo(
                    prompt=f"\n{self.name.upper()} are you sure you want to "
                           f"select {score_selected.upper()}?\n")
        return confirm_score_selected

    def select_score(self, final_roll):
        """
        Allows player to select the scoring option for final dice roll.

        :param final_roll: The final dice roll results.
        :return: The score_selected string.
        """

        double_check = False

        # get list of scoring options from player's scoring dictionary
        while double_check is False:

            # get scoring options
            self.score_options = self.get_score_options()

            check_yahtzee_bonus = False

            while check_yahtzee_bonus is False:

                # get score_selected from input menu offering score options
                score_selected = self.select_score_option(self.score_options)

                # validates user doesn't input blank
                if score_selected == '':
                    print('\nPlease select a valid score option:\n')

                # validating yahtzee bonus
                else:
                    # valid yahtzee bonus selected after yahtzee
                    if (score_selected == 'yahtzee bonus'
                            and self.score_dict['yahtzee'] is False):
                        print('\nYou must score yahtzee before yahtzee bonus. '
                              'Please select another option:\n')

                    # validate yahtzee bonus can't be used to stash 0 score
                    elif (score_selected == 'yahtzee bonus'
                          and len(self.score_options) != 1
                          and len(set(final_roll)) != 1):
                        print('\nYou cannot select yahtzee bonus to stash a 0 '
                              'score if other options are available. Please '
                              'select another option:\n')
                    else:
                        check_yahtzee_bonus = True

            # confirm option selection
            confirm_score_selected = self.confirm_score_selected(
                                        score_selected)

            if confirm_score_selected == 'yes':
                double_check = True

        return score_selected

    def add_top_bonus_score(self):
        """
        Checks the top score and if >= threshold of 63, adds bonus delta of 35.
        """
        bonus_threshold = 63

        # checks top score and threshold to apply top bonus
        if self.top_score >= bonus_threshold and self.top_bonus_score == 0:
            self.top_bonus_score = 35

            # Delta used to increment total bottom and grand total only once.
            self.top_bonus_score_delta = 35

        else:
            self.top_bonus_score_delta = 0

    def print_stacked_score_dict(self):
        """
        Prints the scoring dictionary for the player.
        """
        for key, value in self.score_dict.items():
            if value is False:
                print(f'{key.rjust(15)}: -')
            else:
                print(f'{key.rjust(15)}: {value*1}')

    def get_score_dict(self):
        """
        Returns the score dictionary.
        """
        return self.score_dict

    def get_top_score(self):
        """
        Returns the top score (before bonus).
        """
        return self.top_score

    def get_top_bonus_score(self):
        """
        Returns the top bonus score.
        """
        return self.top_bonus_score

    def get_total_top_score(self):
        """
        Returns the total top score for the player.
        """
        return self.total_top_score

    def get_total_bottom_score(self):
        """
        Returns the total top score for the player.
        """
        return self.total_bottom_score

    def get_grand_total_score(self):
        """
        Returns the total top score for the player.
        """
        return self.grand_total_score

    def get_name_and_grand_total_score(self):
        """
        Returns string player name and string grand total score.
        """
        return self.name, self.grand_total_score

    def reset_all_scores(self):
        """
        Clears the score_dict; sets top, bottom, and grand total score to 0.
        """
        # resets score_dict values to False
        for i, k in enumerate(self.score_dict):
            self.score_dict[k] = False

        # resets score attributes to 0
        self.top_score = 0
        self.top_bonus_score = 0
        self.total_top_score = 0
        self.total_bottom_score = 0
        self.grand_total_score = 0

#!python3

"""
This module contains the main yahtzee gameplay.

github.com/pmacking/yahtzee.py

Rules:
    - Hasbro Yahtzee Rules [1]

[1] https://www.hasbro.com/common/instruct/Yahtzee.pdf
"""

import time
import sys

import pyinputplus as pyip
from datetime import datetime

from .roll import Roll
from .player import Player
from .fileio import FileWriter


class Yahtzee:

    def __init__(self):

        # reference dicts for calculating scores
        self._score_dict_ref_values = {
                'ones': 1, 'twos': 2, 'threes': 3,
                'fours': 4, 'fives': 5, 'sixes': 6,
                }

        # player name strings
        self.number_of_players = 0
        self.players_names = []

        # lists of class instances
        self._players_list = []
        self._rolls_list = []

        # other objects
        self.game_counter = 0
        self.ranking_dict = {}
        self.score_selected = ''
        self.final_roll = []
        self.datetime_today = ''
        self.output_file_formats = ['txt', 'docx']

    def __repr__(self):
        return (f"{self.__class__.__name__}("
                f"{self.number_of_players}, {self.players_names}, "
                f"{self._players_list}, {self._rolls_list}, "
                f"{self.game_counter}, {self.output_file_formats})")

    def create_number_of_players(self):
        """
        Gets the number of players (1 to 4).
        """
        self.number_of_players = pyip.inputInt(
            prompt='\nEnter number of players (1 to 4):\n', min=1, max=4)

    def create_players(self):
        """
        Gets player names for number of players.
        """
        for i in range(self.number_of_players):
            self.players_names.append(pyip.inputStr(
                prompt=f'\nEnter name of player {i + 1}:\n'))

    def create_players_list(self):
        """
        Creates players_list of player instances (1 to 4)
        """
        for p in self.players_names:
            self._players_list.append(Player(p))

    def create_rolls_list(self):
        """
        Creates players_list of player instances (1 to 4)
        """
        for p in self.players_names:
            self._rolls_list.append(Roll(p))

    def sort_ranking_dict(self):
        """
        Gets ranking dict of player and grand total score
        """

        # reset self.ranking_dict to empty dict (if sorted tuple)
        self.ranking_dict = {}

        # create ranking dict with player and grand total score
        for j, player in enumerate(self._players_list):
            ranking_name, ranking_score = \
                self._players_list[j].get_name_and_grand_total_score()
            self.ranking_dict[ranking_name] = ranking_score

        # reverse sort ranking dict by grand total (returns list)
        self.ranking_dict = sorted(self.ranking_dict.items(),
                                   key=lambda x: x[1], reverse=True)

    def set_datetime_today(self):
        """
        Sets date today object for File I/O.
        """
        self.datetime_today = datetime.today().strftime('%Y-%m-%d-%H:%M:%S')

    def reset_player_scores(self):
        """
        Resets scores in all Player class instances for next game.
        """
        for j, player in enumerate(self._players_list):
            self._players_list[j].reset_all_scores()

    def print_current_scores(self, round_num, player_index):
        """
        Print current scores and totals before rolling.

        :param round_num: integer of the round
        :param player_index: player index in players_list
        """
        print(f'\n{self._players_list[player_index].name.upper()} '
              f'YOUR TURN. ROUND: {round_num + 1}')

        print('-'*21)
        print('ROLL SCORES'.rjust(16))
        self._players_list[player_index].print_stacked_score_dict()

        print('-'*21)
        print('TOP SCORE BONUS'.rjust(19))
        print(f"Top Score: {self._players_list[player_index].get_top_score()}")
        print(self._players_list[player_index].get_top_bonus_score())

        print('-'*21)
        print('TOTAL SCORES'.rjust(19))
        print(self._players_list[player_index].get_total_top_score())
        print(self._players_list[player_index].get_total_bottom_score())

        print('-'*21)
        print(f"{self._players_list[player_index].get_grand_total_score()}\n")

    def roll_the_dice(self, player_index):
        """
        Roll dice during a player's turn and print results.

        :param player_index: player index in players_list
        """
        # first roll
        first_roll_result = self._rolls_list[player_index].roll_dice()
        print(f'FIRST ROLL: {first_roll_result}\n')

        # first roll: prompt player to keep, reroll, or select dice
        keep_first_roll = self._rolls_list[player_index].keep_dice(
            self._players_list[player_index].name.upper())

        # second roll
        second_roll_result = self._rolls_list[player_index].reroll_dice(
                                                        keep_first_roll)
        print(f'\nSECOND ROLL: {second_roll_result}\n')

        # second roll: prompt player to keep, reroll, or select dice
        keep_second_roll = self._rolls_list[player_index].keep_dice(
            self._players_list[player_index].name.upper())

        # third roll
        self.final_roll = self._rolls_list[player_index].reroll_dice(
                                                    keep_second_roll)
        print(f'\nFINAL ROLL: {self.final_roll}\n')

    def check_top_score(self, player_index):
        """
        Checks / sets final roll score in top scores sec of scoring_dict

        :param player_index: Player index in players_list and rolls_list.
        """
        score = self._rolls_list[player_index].check_singles(
                            self.final_roll,
                            self._score_dict_ref_values[self.score_selected])

        # incremenet option, top score, top total, grand total
        self._players_list[player_index].score_dict[
            self.score_selected] += score
        self._players_list[player_index].top_score += score
        self._players_list[player_index].total_top_score += score
        self._players_list[player_index].grand_total_score += score

        # check top bonus
        self._players_list[player_index].add_top_bonus_score()

        # increment top total and grand total with delta bonus
        self._players_list[player_index].total_top_score += self._players_list[
            player_index].top_bonus_score_delta
        self._players_list[player_index].grand_total_score \
            += self._players_list[player_index].top_bonus_score_delta

    def check_bottom_score(self, player_index):
        """
        Checks / sets final roll score in bottom scores sec of scoring_dict

        :param player_index: Player index in players_list and rolls_list.
        """
        if self.score_selected == 'three of a kind':
            score = self._rolls_list[player_index].check_three_of_a_kind(
                    self.final_roll)

        elif self.score_selected == 'four of a kind':
            score = self._rolls_list[player_index].check_four_of_a_kind(
                    self.final_roll)

        elif self.score_selected == 'full house':
            score = self._rolls_list[player_index].check_full_house(
                    self.final_roll)

        elif self.score_selected == 'small straight':
            score = self._rolls_list[player_index].check_small_straight(
                    self.final_roll)

        elif self.score_selected == 'large straight':
            score = self._rolls_list[player_index].check_large_straight(
                    self.final_roll)

        elif self.score_selected == 'yahtzee':
            score = self._rolls_list[player_index].check_yahtzee(
                    self.final_roll)

        elif self.score_selected == 'chance':
            score = self._rolls_list[player_index].add_chance(
                    self.final_roll)

        elif self.score_selected == 'yahtzee bonus':
            score = self._rolls_list[player_index].check_yahtzee_bonus(
                    self.final_roll)

            # cannot score 50 for yahztee bonus if did not score 50 yahtzee
            if self._players_list[player_index].score_dict['yahtzee'] != 50:
                score = 0

        # increment round, total bottom, and grand total scores
        self._players_list[player_index].score_dict[self.score_selected] \
            += score
        self._players_list[player_index].total_bottom_score += score
        self._players_list[player_index].grand_total_score += score

    def print_end_of_turn_grand_total(self, player_index):
        """
        Print grand total score for end of player turn.

        :param player_index: player index in players_list
        """
        print(f"\n{self._players_list[player_index].name.upper()} "
              f"GRAND TOTAL: "
              f"{self._players_list[player_index].grand_total_score}")

    def print_end_of_round_rankings(self):
        """
        Prints player rankings and grand total scores at the end of the round.
        """
        print('\nFINAL SCORES')
        print('-'*12)
        for k, v in enumerate(self.ranking_dict):
            print(f"{k+1} {v[0]}: {v[1]}")
        print('\n')

    def end_of_game(self):
        """
        Increments game counter. Sets game over to True if count == 3.
        """
        end_game = pyip.inputYesNo(f'\nDo you want to play again?: ')

        if end_game == 'no':
            print('\n-- GAME OVER --')
            sys.exit()
        elif end_game == 'yes':
            self.game_counter += 1

    def yahtzee_rounds(self):
        """Round logic taken by each player within a game."""

        # round loop (arbitrarily refs len of first instance of Player)
        for i, k in enumerate(self._players_list[0].score_dict):

            # player turn loop (turn per player per round)
            for j, player in enumerate(self._players_list):

                # skip the final round if only yahtzee bonus and yahtzee != 50
                if (i == 13 and
                    self._players_list[j].score_dict['yahtzee bonus'] is False
                    and self._players_list[j].score_dict['yahtzee'] != 50):

                    # Since all conditions are true, we can frobnicate.
                    self._players_list[j].score_dict['yahtzee bonus'] = 0
                    print("\nAutomatically score 0 for 'yahtzee bonus'...")

                else:
                    self.print_current_scores(i, j)  # print scores b4 rolling
                    print("-"*48)

                    # roll the dice
                    self.roll_the_dice(j)
                    print("-"*48)

                    # select score to check final roll against
                    self.score_selected = self._players_list[j].select_score(
                        self.final_roll)

                    # Check TOP SCORE and increment score
                    if self.score_selected in self._score_dict_ref_values:
                        self.check_top_score(j)

                    # Check BOTTOM SCORE and increment score
                    else:
                        self.check_bottom_score(j)

                    # print grand total score at end of player turn
                    self.print_end_of_turn_grand_total(j)
                    print("-"*48)
                    print("-"*48)

        # END OF ROUND RANKING

        # create ranking dict for the round
        self.sort_ranking_dict()

        # print rankings for the round
        self.print_end_of_round_rankings()

        # END OF ROUND FILE I/O

        # set date object for standardizing file basenames
        self.set_datetime_today()

        file_write = FileWriter()
        file_write.write_file(self.datetime_today,
                              self.game_counter,
                              self._players_list,
                              self.ranking_dict,
                              self.output_file_formats)

        # END OF ROUND CLEANUP

        # end game option
        self.end_of_game()

        print('\nResetting dice for next round...')
        print("-"*48)
        time.sleep(2)

        # reset each Player class instance scoring dict and total scores
        self.reset_player_scores()

    def play(self):
        """
        Initializes players and rolls instances, and begins yahtzee games.
        """
        # create players, instances of Player and Roll
        print('\nWELCOME TO YAHTZEE!')
        self.create_number_of_players()
        self.create_players()
        self.create_players_list()
        self.create_rolls_list()
        print("-"*48)

        # starts games of rounds of player turns
        while True:

            print(f"\nLET'S PLAY! GAME {self.game_counter + 1}")

            self.yahtzee_rounds()
